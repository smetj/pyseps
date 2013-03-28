PySeps
======

Disclaimer: PySeps is currently a proof of concept and incomplete.

What?
-----
A Python based Simple Event Processing Server framework.
Consume or accept JSON documents from a source and forward them real time to
another destination using different types of query engines.

Euh?
----
Ever had to extract and forward matches out of a constant stream of JSON
documents using complex conditionals?

How?
----
PySeps has different "engines" which take care of the matching.

TailingCursor:
~~~~~~~~~~~~~~

Create tailing cursors out of MongoDB queries and apply them to a capped
collection.  Each cursor is "mapped" to a RabbitMQ queue. Each time a cursor
returns documents they are submitted to the RabbitMQ queue the query is mapped
to.  It's up to another process or application to take action on the documents
arriving in the queue mapped to the query.

.. image:: docs/diagram.png

The pyseps module called TailingCursor does exactly that.  For more
information have a look at:

https://github.com/smetj/pyseps/tree/master/pyseps/tailingcursor

MapMatch:
~~~~~~~~~

n/a

SequentialMatch:
~~~~~~~~~~~~~~~~

n/a


Setup
-----

Pypi
~~~~

	$ easy_install pyseps

GitHub
~~~~~~

	$ git clone https://github.com/smetj/pyseps.git

	$ cd pyseps

	$ python setup.py install