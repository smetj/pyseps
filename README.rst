PySeps
======

What?
-----
A Python based Simple Event Processing Server framework. Consume a stream of
documents and forward matching documents to another destination using
different types of query engines.

How?
----
PySeps is build on the Wishbone framework which allows you to build coroutine
based event pipelines.  PySeps delivers a set of modules which can be plugged
into the Wishbone framework.  Each module acts as a different engine to
perform the document matching.

Engines:
--------

MapMatch:
~~~~~~~~~
pyseps.mapmatch

The MapMatch engine converts a sequence of evaluation rules into a map to
process the most requested evaluations first in an attempt to have a
statistical advantage over dumb sequential evaluation of all rules until a
match is found. If a match occurs the document is forwarded to the Wishbone
queue associated with the matching rule.

SequentialMatch:
~~~~~~~~~~~~~~~
pyseps.sequentialmatch

Sequentially matches rules against all incoming events.


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

Examples
--------

See https://github.com/smetj/experiments/tree/master/pyseps

