TailingCursor
=============

Using MongoDB to filter a document stream.
------------------------------------------

By creating a tailing cursor containing a MongoDB query and by applying that
cursor to a capped collection which constantly receives new documents,  we
have a quite powerful filtering mechanism to extract from a constant the
documents we want.

Each cursor is "mapped" to a RabbitMQ queue. Every time a cursor returns,
documents they are submitted to the RabbitMQ queue the query is mapped to.
It's up to another process or application to take action on the documents
arriving in the queue mapped to the query.

A TailingCursor based PySeps setup consists out of 2 parts:

Shipper
~~~~~~~

Strictly speaking it is outside the scope of PySeps but one way or the other
we need to get the events we want to process in MongoDB.  PySeps comes with a
shipper functionality which consumes the documents from RabbitMQ and writes
them into MongoBD.  You are not obliged to use this.  There are other ways to
get the JSON events into MongoDB, your mileage may vary.

TailingCursor engine
~~~~~~~~~~~~~~~~~~~~

The TailingCursor engine is what it's all about. So the documents arrive in a
MongoDB capped collection.  That means each newly inserted document is matched
against all active tailing cursors. PySeps receives the queries it should
evaluate by consuming a dedicated queue. Adding queries is a matter of
submitting them to the *pyseps:queries* queue. Once a tailing cursor returns a
document, the document is forwarded to the corresponding RabbitMQ queue.


Motivation
----------

The reason to use MongoDB is because we can take advantage of the document
query language which comes with MongoDB, so no need to invent something new.
The MongoDB document query syntax also have support for multi level documents.


Documentation
-------------

.. image:: ../../docs/diagram.png


Usage
-----

Setup a shipper using the rabbitmq.json bootstrap file: https://github.com/sme
tj/experiments/blob/master/pyseps/FeedMongoDB/rabbitmq.json

    $ pyseps debug --config rabbitmq.json --pid rabbitmq.pid


Setup a processing engine using the "tailingcursor.json" bootstrap file
https://github.com/smetj/experiments/blob/master/pyseps/tailingcursor.json


    $ pyseps debug --config tailingcursor.json --pid pyseps.pid


In tailingcursor.json we have defined a queue called "pyseps:queries".
Submit following queries to the *pyseps:queries* queue as separate documents:

    {"id":"07fb983f-ca15-4e38-a3b7-b1e544dc64ca","name":"Important messages","
    {"exchange":"","key":"pyseps:important","query":{"@fields.priority":{"$in"
    {":["1","2","3","4"]}}}

    {"id":"07fb983f-ca15-4e38-a3b7-b1e544dc64ca","name":"Unimportant messages"
    {","exchange":"","key":"pyseps:unimportant","query":{"@fields.priority":{"
    {"$nin":["1","2","3","4"]}}}

    {"id":"07fb983f-ca15-4e38-a3b7-b1e544dc64ca","name":"abcd","exchange":"alp
    {"habet","key":"abcd","query":{"0":{"$regex":"^a.*"},"1":{"$regex":"^b.*"}
    {","2":{"$regex":"^c.*"},"3":{"$regex":"^d.*"}}}


Breakdown of the query:

id
~~

A unique UUID which identifies the batch of queries.  When the ID changes all
loaded and active queries are purged and replaced with the newly arriving
queries each sharing the same ID.

name
~~~~
A name describing the query.

exchange
~~~~~~~~
The broker exchange to which matching documents have to be submitted.

key
~~~
The broker routing key used to submit matching documents.

query
~~~~~
The MongoDB query which needs to be evaluated against all newly added
documents.

ToDo
----

* Instead of submitting documents only to RabbitMQ submit then to a WishBone
queue of choice just like the MapMatch engine.