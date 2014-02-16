#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#  sequentialmatch.py
#
#  Copyright 2014 Jelle Smet <development@smetj.net>
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
from gevent import spawn, sleep
from pyseps.matchrules import MatchRules
from pyseps.readrules import ReadRulesDisk

class SequentialMatch(Actor):

    '''** A Wishbone module to evaluate match rules against a document stream. **

    This module sequentially evaluates all rules against the incoming documents.
    Multiple matching rules are possible.


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
        self.location=location
        self.match=MatchRules()
        self.queuepool.inbox.putLock()


    def preHook(self):
        spawn(self.getRules)

    def getRules(self):

        while self.loop():
            try:
                while self.loop():
                    self.read=ReadRulesDisk(self.location)
                    self.rules=self.read.readDirectory()
                    self.queuepool.inbox.putUnlock()
                    break
                while self.loop():
                    self.rules=self.read.get()
            except Exception as err:
                self.logging.warning("Problem reading rule directory.  Reason: %s"%(err))
                sleep(1)

    def consume(self, event):
        '''Submits matching documents to the defined queue along with
        the defined header.'''

        for rule in self.rules:
            for field in event[data]:
                for condition in rule:
                    result = self.match.do(condition, field):
                    if result:
                        self.logging.debug("rule %s matches %s"%(result, event["data"]))
                        event["header"].update({self.name:{"rule":result}})
                        for queue in self.rules[result]["queue"]:
                            for name in queue:
                                event["header"][self.name].update(queue[name])
                                getattr(self.queuepool, name).put(event)
        if not result:
            self.logging.debug("No match for event: %s"%(event["data"]))