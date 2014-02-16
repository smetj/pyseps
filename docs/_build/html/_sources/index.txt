.. PySeps documentation master file, created by
   sphinx-quickstart on Fri Sep 13 20:21:02 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PySeps
======

A Wishbone module to match json documents in transit.


How
---

The PySeps module is a JSON document matching engine which can be plugged into
a Wishbone setup.  Incoming JSON events are evaluated against a user provided
set of matching rules.  Matching documents are then forwarded to the queue of
choice from which matching documents can flow to other modules.

Modes
-----

The engine can be initiated in different modes each with their own features.

MapMatch
~~~~~~~~

This mode converts a sequence of evaluation rules into a map to process the
most requested evaluations first in an attempt to have a statistical advantage
over sequential evaluation of all rules until a match is found. If a match
occurs the event is forwarded to the Wishbone queue associated with the
matching rule.  The moment a first match occurs, no further rule processing is
done.

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

