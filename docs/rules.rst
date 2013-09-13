=====
Rules
=====

Rules are written in YAML format on disk.  Each rule which consists out of one
or more conditions is stored in 1 file. A directory contains a collection of
rules. Only files with extension .yml are processed.  MapMatch monitors the
directory for changes and automatically reloads the rules when required. The
directory can be set using the *ruledir* variable.

Format
------

A rule should be valid YAML format and should have a similar structure:

::

    ---
    condition:
        "hostnotificationid": re:\d*
        "check_command": re:check:host.alive
        "hostgroupnames": re:.*?development.*

    queue:
        - amqp:
            broker_exchange: ""
            broker_key: ""
    ...


Breakdown of a rule
-------------------

A rule consists out of 2 main parts: condition and queue.

The condition part is a dictionary containing the conditions to evaluate
against the desired document fields.  The individual conditions relate with a
logical AND to each other.

The queue part consists out of a list of WishBone queues to which matching
documents should be submitted.  Non existing queues are automatically created.
You should make sure there is a Wishbone module connected to the defined
MapMatch modules, otherwise matching documents will just pile up there.  Each
defined Wishbone queue contains a dictionary which will be added to the header
section of the document submitted to the said queue.

The type of condition is embedded in the condition definition.  currently
there is support for regexes.  Other condition types might be added in the
future when the need arises.

regex
-----

Condition which have to be regular expressions should start with *re:* or
*!re* for positive and negative regular expressions respectively.

examples:

*"re:qwerty"*
Matches if the string contains "qwerty".

*"re:^qwerty.*"*
Matches if the string starts with "qwerty".

*"!re:^qwerty"*
Matches if the string is NOT equal to "qwerty".

*"!re:qwerty"*
Matches if the string does NOT contain"qwerty".