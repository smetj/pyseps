PySeps
========

Disclaimer: PySeps is currently a proof of concept and incomplete.

What?
-----
A Python based Simple Event Processing Server framework.

How?
----
A pyseps setup consists out of 2 parts:

A shipper:
Events in the form of JSON documents are consumed (or received) from a source such as an AMQP broker and written into 
a MongoDB capped collection.

A processing engine:
For each query the engine has to process a tailing cursor is made.  The moment a document is inserted into the
MongoDB capped collection it is evaluated against the all active cursors.


The motivation for using MongoDB is bacause we could take advantage of the MongoDB query language for document matching.
The MongoDB capped collection is ideal for this since it lives in memory and it has a fixed size.

The idea is matching records will but submitted to to their own AMQP queue.  That queue is determined by the "key" value in the 
query.


Documentation
-------------
None Yet.  Since PySeps runs on top of the Wishbone module you should have a look at that documention first.

Setup
-----
Fork from github and run setup.py

Setup a shipper using the rabbitmq2mongodb.json bootstrap file

    $ pyseps debug --config rabbitmq2mongodb.json --pid rabbitmq2mongodb.pid

Setup a processing engine using the  pyseps.json bootstrap file
    
    $ pyseps debug --config pyseps.json --pid pyseps.pid


In pyseps.json we have defined a queue called "pyseps:queries".  When this queue doesn't exist it should be created.
Submit to this queue following queries (as separate documents):

{"id":"07fb983f-ca15-4e38-a3b7-b1e544dc64ce","name":"NonInformational","key":"broker_key","query":{"@fields.priority":{"$in":["1","2","3","4"]}}}

{"id":"07fb983f-ca15-4e38-a3b7-b1e544dc64ce","name":"Informational","key":"broker_key","query":{"@fields.priority":{"$in":["5","6","7"]}}}


Breakdown of the query:

id: A unique UUID which identifies the batch of queries.  When the ID changes all loaded and active queries are purged and replaced with the newly
    arriving queries each sharing the same ID.

name:   A name describing the query.

key:    The broker routing key to which the matching record has to be be submitted.

query:  The MongoDB query which needs to be evaluated against all newly added documents.
