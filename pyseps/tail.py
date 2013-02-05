#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tail.py
#  
#  Copyright 2013 Jelle Smet development@smetj.net
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

import logging
from wishbone.toolkit import QueueFunctions, Block, TimeFunctions
from gevent import Greenlet, spawn, sleep, joinall
import pymongo
import json
from gevent import monkey;monkey.patch_all()

class Tail(Greenlet, QueueFunctions, Block, TimeFunctions):
    '''**A Pyseps modules which tails the capped collection for hits.**
            
    Parameters:        

        - name (str):           The instance name when initiated.
        - host (str):           The name or IP of MongoDB.
        - db (str):             The name of the database.
        - collection (str):     The name of the collection.

    Queues:
        
        - inbox:                Documents which got a hit.
        - queries:              The queries to perform coming from the broker.
        - acknowledge           The query acknowledgements coming from broker.
    '''
    
    def __init__(self, name, host, db, collection):
        Greenlet.__init__(self)
        Block.__init__(self)
        QueueFunctions.__init__(self)
        self.name=name
        self.logging = logging.getLogger( self.name )
        self.logging.info('Initiated')
        self.host=host
        self.db=db
        self.collection=collection
        self.mongo=None
        self.createQueue("queries")
        self.createQueue("acknowledge")
        self.query_threads=[]
        self.query_reload=False
        self.query_batch_id=None
        Greenlet.spawn(self._loadQueries)

    def __setup(self):
        '''Creates the MongoDB connection.'''

        try:
            connection = pymongo.MongoClient(self.host)
            collection = connection[self.db][self.collection]
            self.mongo = collection
        except Exception as err:
            self.logging.warn('Failed to connect to MongoDB. Reason: %s'%(err))
            sleep(1)
    
    def _loadQueries(self):
        '''Loads the queries from the broker.'''
        
        while self.block()==True:
            if self.queries.qsize() > 0:
                self.logging.info('New queries received.')                
                while self.block() == True:
                    try:
                        query = self.queries.get(False)
                        self._checkBatchID(query["data"]["id"])
                        self.query_threads.append(Greenlet.spawn(self.query,query["data"]["name"],query["data"]["query"],query["data"]["key"]))
                        self.sendRaw(query["header"]["broker_tag"],"acknowledge")
                    except:
                        self.logging.debug('Query queue is empty.')
                        self.query_reload=False
                        break
            else:
                sleep(1)
    
    def _checkBatchID(self, id):
        '''When the current batch_id differs from the previous batch_id we interrupt and wipe the current cursors.'''
        
        if self.query_batch_id == id:
            self.logging.debug('Batch ID is the same. Adding cursor.')
            return True
        else:
            self.logging.debug('New batch ID received.')
            self._stopRunningQueries()
            self.query_batch_id = id
            return False 
    
    def _stopRunningQueries(self):
        self.logging.debug('Stopping and wiping the running cursors.')
        self.query_reload=True
        joinall(self.query_threads)
                                
    def _run(self):
        '''
        '''
        self.__setup()
        self.logging.info('Started')
        while self.block() == True:
            sleep(1)
    
    def query(self,name,query,key):
        skip=self.mongo.count()
        self.logging.info("Cursor spawned with name: %s. Skipping until record #%s."%(name,skip))
        cursor = self.mongo.find(query,tailable=True,skip=skip,timeout=False)
        while self.block() == True:
            try:
                for document in self.getDocuments(cursor):
                    self.logging.debug("%s got a hit."%(name))
                    self.sendData({"header":{"broker_exchange":"","broker_key":key},"data":document},"inbox")
            except:
                pass
            if self.query_reload == True:
                self.logging.info("Stopped running cursor %s"%(name))
                break
            sleep(0.5)
        self.logging.info("Cursor %s has exit."%(name))
    
    @TimeFunctions.do
    def getDocuments(self, cursor):
        for document in cursor:
            yield document
    
    def shutdown(self):
        pass
