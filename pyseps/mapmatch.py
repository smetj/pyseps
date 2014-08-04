#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  mapmatch.py
#
#  Copyright 2014 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
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
from gevent import spawn, sleep
from pyseps.matchrules import MatchRules
from pyseps.readrules import ReadRulesDisk


class MapMatch(Actor):

    '''** A Wishbone module to evaluate match rules against a document stream. **

    The MapMatch module matches documents against a set of user provided rules
    and submits the matching documents to a Wishbone queue of choice.

    The ruleset is broken down into each individual condition and placed into
    a weighted map. The field which has to evaluated the most has the highest
    weight and will be evaluated first.  If the number of matching conditions
    matches the number of required conditions for a rule that rule wins.

    As a consequence, when multiple identical rules exist in the total
    ruleset, the one which has the conditions which are requested the most
    will win.

    If you have a very large ruleset rules will be evaluated quicker since a
    winner is elected faster.

    Rules on disk are in YAML format and consist out of 2 parts:

        condition
        ---------

        The condition part contains the individual conditions which have to
        match for the complete rule to match.

        queue
        -----

        The queue section contains a list of dictionaries/maps each containing
        1 key with another dictionary/map as a value.  These key/value pairs
        are added to the *header section* of the event and stored under the
        queue name key.

    Example:
    --------

        condition:
            "check_command": re:check:host.alive
            "hostproblemid": re:\d*
            "hostgroupnames": in:tag:development

        queue:
            - email:
                from: monitoring@yourdomain.com
                to:
                    - oncall@yourdomain.com
                subject: UMI - Host  {{ hostname }} is  {{ hoststate }}.
                template: host_email_alert


    Parameters:

        - name (str):       The instance name when initiated.

        - location (str):   The directory containing the rules.
                            Default: rules/

    Queues:

        - inbox:    Incoming events to evaluate.

    Matching events will be submitted to the queue defined in the rules.

    '''

    def __init__(self, name, location='rules/'):
        Actor.__init__(self, name)
        self.location = location
        self.match = MatchRules()
        self.queuepool.inbox.putLock()

    def preHook(self):
        spawn(self.getRules)

    def getRules(self):

        while self.loop():
            try:
                while self.loop():
                    self.read = ReadRulesDisk(self.location)
                    self.rules = self.read.readDirectory()
                    self.map = self.generateMap(self.rules)
                    self.queuepool.inbox.putUnlock()
                    break

                while self.loop():
                    self.rules = self.read.get()
                    self.generateMap(self.rules)

            except Exception as err:
                self.logging.warning(
                    "Problem reading rule directory.  Reason: %s" % (err))
                sleep(1)

    def generateMap(self, rules):
        '''The function converts the rules into a weighted map containing all
        conditions.'''

        self.logging.info('A new set of rules received.')
        optimized = {}
        for rule in rules:
            for condition in rules[rule]["condition"]:
                if condition in optimized:
                    if rules[rule]["condition"][condition] in optimized[condition]:
                        optimized[condition][rules[rule]["condition"][condition]].append(
                            (rule, len(rules[rule]["condition"])))
                    else:
                        optimized[condition][rules[rule]["condition"][condition]] = [
                            (rule, len(rules[rule]["condition"]))]
                else:
                    optimized[condition] = {
                        rules[rule]["condition"][condition]: [(rule, len(rules[rule]["condition"]))]}

        for item in optimized:
            optimized[item] = sorted([(key, optimized[item][key]) for key in optimized[
                                     item]], key=lambda value: len(value[1]), reverse=True)

        optimized = sorted(optimized.iteritems(), key=lambda value: sum(
            len(v[1]) for v in value[1]), reverse=True)
        return optimized

    def executeMatch(self, rulenames, map, data):
        '''
        Matches the record
        '''

        state = {}
        # state={x:0 for x in rulenames}
        for x in rulenames:
            state[x] = 0
        for field in map:
            if field[0] in data:
                for match in field[1]:
                    try:
                        if self.match.do(match[0], data[field[0]]):
                            for rule in match[1]:
                                state[rule[0]] += 1
                                if rule[1] == state[rule[0]] and state[rule[0]] <= len(data):
                                    return rule[0]
                    except Exception as err:
                        self.logging.warn(
                            "Failed to evaluate condition. Purged  Reason: %s" % (err))
                        return False
        return False

    def consume(self, event):
        '''Submits matching documents to the defined queue along with
        the defined header.'''

        result = self.executeMatch(self.rules.keys(), self.map, event["data"])
        if result is not False:
            self.logging.debug("rule %s matches %s" % (result, event["data"]))
            event["header"].update({self.name: {"rule": result}})
            for queue in self.rules[result]["queue"]:
                for name in queue:
                    event["header"][self.name].update(queue[name])
                    getattr(self.queuepool, name).put(event)
        else:
            self.logging.debug("No match for event: %s" % (event["data"]))
