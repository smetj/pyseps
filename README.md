pyseps
======

version: 0.3.1

** A Wishbone module to evaluate match rules against a document stream. **

The MapMatch module matches documents against a user provided ruleset
and submits the matching documents to a Wishbone queue of choice.

The set of rules is converted in such a way that the fields which will most
likely match the most are evaluated first.  This to speed up evaluation.
Keep in mind, once a rule matched, further matching stops.

Parameters:

    - name (str):       The instance name when initiated.

    - location (str):   The directory containing the rules.
                        Default: rules/

Queues:

    - inbox:    Incoming events to evaluate.

Matching events will be submitted to the queue defined in the rules.
