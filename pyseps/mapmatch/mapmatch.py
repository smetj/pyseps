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

from wishbone.toolkit import PrimitiveActor
import json
import re

class MapMatch(PrimitiveActor):
    '''**The MapMatch module converts a set of rules into an optimized map and
    uses this map to match incoming dictionaries.**

    Optimized in this context means the keys which have to be evaluated the most
    are evaluated first.  Once a rule has all conditions fullfilled, no further
    evaluation is done.

    This module is part of the PySeps project.

    Parameters:

        - name (str):    The instance name when initiated.

    Queues:

        - inbox:    Incoming events.
        - outbox:   Outgoing events.
    '''

    def __init__(self, name, ruledb="rules.txt"):
        PrimitiveActor.__init__(self, name)
        (self.map, self.rules)=self.generateMap(ruledb)

    def generateMap(self, rules):
    	'''Takes a list of dictionaries and converts them to a matchmap.
    	'''

        f = open (rules, 'r')
        rules=json.loads("\n".join(f.readlines()))
        f.close()

        optimized={}
        for rule in rules:
            for condition in rules[rule]["conditions"]:
                if optimized.has_key(condition):
                    if optimized[condition].has_key(rules[rule]["conditions"][condition]):
                        optimized[condition][rules[rule]["conditions"][condition]].append((rule, len(rules[rule]["conditions"])))
                    else:
                        optimized[condition][rules[rule]["conditions"][condition]]=[(rule, len(rules[rule]["conditions"]))]
                else:
                    optimized[condition]={rules[rule]["conditions"][condition]:[(rule, len(rules[rule]["conditions"]))]}

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
                    if re.match(match[0], data[field[0]]):
                        for rule in match[1]:
                            state[rule[0]]+=1
                            if rule[1] == state[rule[0]] and state[rule[0]] <= len(data):
                                return rule[0]
        return False

    def consume(self,doc):

        result = self.match(self.rules.keys(), self.map, doc["data"])
        if result != False:
            for queue in self.rules[result]["queue"]:
                doc["header"].update(self.rules[result]["queue"][queue])
                self.putData(doc,queue)

    def shutdown(self):
        self.logging.info('Shutdown')