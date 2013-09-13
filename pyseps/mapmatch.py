#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  mapmatch.py
#
#  Copyright 2013 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from wishbone import Actor
from gevent import spawn
from glob import glob
from os import path
import gevent_inotifyx as inotify
import json
import yaml
import re


class MapMatch(Actor):
    '''** A Wishbone module to evaluate match rules against a document stream. **

    The MapMatch module matches documents against a user provided ruleset
    and submits the matching documents to a Wishbone queue of choice.

    The set of rules is converted in such a way that the fields which will most
    likely match the most are evaluated first.  This to speed up evaluation.
    Keep in mind, once a rule matched, further matching stops.

    Parameters:

        - name (str):       The instance name when initiated.

        - ruledir (str):    The directory containing the rules.
                            Default: ./

    Queues:

        - inbox:    Incoming events to evaluate.

    Matching events will be submitted to the queue defined in the rules.

    '''

    def __init__(self, name, ruledir='./'):
        Actor.__init__(self, name)
        self.ruledir=ruledir
        (self.map,self.rules) = self.readDirectory(ruledir)


    def preHook(self):
        spawn(self.monitorDirectory, self.ruledir)

    def monitorDirectory(self, directory):
        '''Monitors the given directory for changes.'''

        self.logging.info('Monitoring %s'%(directory))
        fd = inotify.init()
        wb = inotify.add_watch(fd, directory, inotify.IN_CLOSE_WRITE+inotify.IN_DELETE)
        while self.loop() == True:
            events = inotify.get_events(fd)
            (self.map,self.rules) = self.readDirectory(directory)

    def readDirectory(self, directory):
        '''Reads the content of the given directory and creates a dict
        containing the rules.'''
        self.logging.info('Loading rules from directory %s'%(directory))
        rules={}
        for filename in glob("%s/*.yaml"%(directory)):
            f=open (filename,'r')
            rules[path.basename(filename).rstrip(".yaml")]=yaml.load("\n".join(f.readlines()))
            f.close()
        return self.generateMap(rules)

    def generateMap(self, rules):

        ''' This function is called upon each
        document arriving in the self.rules queue. One document is expected to
        contain all matching rules.  Upon receiving a new set of rules, the
        previous one is discarded. Converts data into a Map which gives us
        statistical advantage in finding matches.

        The outgoing map has following structure:
        '''

        self.logging.info('A new set of rules received.')
        optimized={}
        for rule in rules:
            for condition in rules[rule]["condition"]:
                if optimized.has_key(condition):
                    if optimized[condition].has_key(rules[rule]["condition"][condition]):
                        optimized[condition][rules[rule]["condition"][condition]].append((rule, len(rules[rule]["condition"])))
                    else:
                        optimized[condition][rules[rule]["condition"][condition]]=[(rule, len(rules[rule]["condition"]))]
                else:
                    optimized[condition]={rules[rule]["condition"][condition]:[(rule, len(rules[rule]["condition"]))]}

        for item in optimized:
            optimized[item] = sorted([ (key,optimized[item][key]) for key in optimized[item] ], key=lambda value: len(value[1]), reverse=True)

        optimized = sorted(optimized.iteritems(), key=lambda value: sum(len(v[1]) for v in value[1]), reverse=True)
        return (optimized, rules)

    def match(self, rulenames, map, data):
        '''
        Matches the record
        '''
        state={}
        #state={x:0 for x in rulenames}
        for x in rulenames:
            state[x]=0
        for field in map:
            if field[0] in data:
                for match in field[1]:
                    if self.__typeMatch(match[0], data[field[0]]):
                        for rule in match[1]:
                            state[rule[0]]+=1
                            if rule[1] == state[rule[0]] and state[rule[0]] <= len(data):
                                return rule[0]
        return False

    def __typeMatch(self, rule, data):
        '''
        Executes different forms of matching.
        '''

        if rule.startswith('re:'):
            if re.search(rule[3:],str(data)):
                return True
        elif rule.startswith('!re:'):
            if not re.search(rule[4:],str(data)):
                return True
        else:
            self.logging.warn("%s is an invalid match rule."%(rule))
            return False

        return False

    def consume(self, event):
        '''Submits matching documents to the defined queue along with
        the defined header.'''

        result = self.match(self.rules.keys(), self.map, event["data"])
        if result != False:
            event["header"].update({self.name:{"rule":result}})
            for queue in self.rules[result]["queue"]:
                for name in queue:
                    event["header"][self.name].update(queue[name])
                    getattr(self.queuepool, name).put(event)