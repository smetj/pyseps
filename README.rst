PySeps
========

Disclaimer: PySeps is currently a proof of concept and incomplete.

What?
-----
A Python based Simple Event Processing Server framework.
Consume or accept JSON documents from a source and forward them real time to a 
specific AMQP queue using MongoDB query syntax.

Euh?
----
Ever had to extract and forward matches out of a constant stream of JSON documents
using complex conditionals?

How?
----
Create tailing cursors out of MongoDB queries and apply them to a capped
collection.  Each cursor is "mapped" to a RabbitMQ queue. Each time a cursor
returns documents they are submitted to the RabbitMQ queue the query is mapped to.
It's up to another process or application to take action on the documents arriving
in the queue mapped to the query.

A PySeps setup consists out of 2 parts:

Shipper
~~~~~~~
Strictly speaking it is outside the scope of PySeps but one way or the other we
need to get the events we want to process in MongoDB.  PySeps comes with a shipper
functionality which consumes the documents from RabbitMQ and writes them into
MongoBD.  You are not obliged to use this.  There are other ways to get the JSON
events into MongoDB, your mileage may vary.

Processing engine
~~~~~~~~~~~~~~~~~
The processing engine is what it's all about.
So the documents arrive in a MongoDB capped collection.  That means each newly 
inserted document is matched against all active tailing cursors.
PySeps receives the queries it should evaluate by consuming a dedicated queue.
Adding queries is a matter of submitting them to the *pyseps:queries* queue.
Once a tailing cursor returns a document, the document is forwarded to the
corresponding RabbitMQ queue.


Motivation
----------
The reason to use MongoDB is because we can take advantage of some its unique
features which really fit our scenario of document stream processing such as:

- a document query language
- capped collections
- tailing cursors


Documentation
-------------
PySeps is still a POC and subject to change.  I'll wait writing documentation
when it becomes more definite.

.. image:: docs/diagram.png

Setup
-----

1. Install WishBone v0.3 from https://github.com/smetj/wishbone/tree/0.3
2. Install wb_broker https://github.com/smetj/wishboneModules/tree/master/iomodules/wb_broker
3. Install PySeps from https://github.com/smetj/pyseps
4. Get and modify if required some PySeps bootstrap files from https://github.com/smetj/experiments/tree/master/pyseps

*Install will become simpler once WishBone 0.3 is released.*

Setup a shipper using the rabbitmq.json bootstrap file:

    $ pyseps debug --config rabbitmq.json --pid rabbitmq.pid

Setup a processing engine using the  pyseps.json bootstrap file:
    
    $ pyseps debug --config pyseps.json --pid pyseps.pid

Usage
-----

In pyseps.json we have defined a queue called "pyseps:queries".
Submit following queries to the *pyseps:queries* queue as separate documents:

    {"id":"07fb983f-ca15-4e38-a3b7-b1e544dc64ca","name":"Important messages","exchange":"","key":"pyseps:important","query":{"@fields.priority":{"$in":["1","2","3","4"]}}}
    
    {"id":"07fb983f-ca15-4e38-a3b7-b1e544dc64ca","name":"Unimportant messages","exchange":"","key":"pyseps:unimportant","query":{"@fields.priority":{"$nin":["1","2","3","4"]}}}
    
    {"id":"07fb983f-ca15-4e38-a3b7-b1e544dc64ca","name":"abcd","exchange":"alphabet","key":"abcd","query":{"0":{"$regex":"^a.*"},"1":{"$regex":"^b.*"},"2":{"$regex":"^c.*"},"3":{"$regex":"^d.*"}}}


Breakdown of the query:

id
~~
A unique UUID which identifies the batch of queries.  When the ID changes all
loaded and active queries are purged and replaced with the newly arriving queries
each sharing the same ID.

name
~~~~
A name describing the query.

key
~~~
The broker routing key to which the matching record has to be be submitted.

query
~~~~~
The MongoDB query which needs to be evaluated against all newly added documents.


ToDo
----

- Also allow exchange definition in query to queue mapping.
- Figure out a way to autocreate queues when the message is non routable.
- Provide API and CLI to control pyseps setup.
- Federate searches in a tree structure over different nodes to scale out. (hmm)
- Tests
- ...
