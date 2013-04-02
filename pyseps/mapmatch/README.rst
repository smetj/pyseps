MapMatch
========

The MapMatch engine converts a sequence of evaluation rules into a map to
match the most requested evaluations first in an attempt to have a statistical
advantage over dumb sequential evaluation of all rules until a match is found.
If a match occurs the document is forwarded to the WishBone queue associated
with the matching rule.

Matching rules:
---------------

Format:
~~~~~~~

The file containing the matching rules must be valid JSON and should have
following structure:

::
	{
	"rule0":{"queue":{"broker":{"broker_key":"rule0","broker_exchange":""}},"conditions":{"1":"re:a"}},
	"rule1":{"queue":{"broker":{"broker_key":"rule1","broker_exchange":""}},"conditions":{"1":"re:b","2":"re:c"}},
	"rule2":{"queue":{"broker":{"broker_key":"rule2","broker_exchange":""}},"conditions":{"1":"re:d","2":"re:e","3":"re:f"}},
	"rule3":{"queue":{"broker":{"broker_key":"rule3","broker_exchange":""}},"conditions":{"1":"re:g","2":"re:h","3":"re:i","4":"re:j"}},
	"rule4":{"queue":{"broker":{"broker_key":"rule4","broker_exchange":""}},"conditions":{"1":"re:k","2":"re:l","3":"re:m","4":"re:n","5":"re:o"}}
	}::

Breakdown of a rule:
~~~~~~~~~~~~~~~~~~~~

A rule consists out of one or more conditions.  Each individual condition
within a rule should match before the complete rule is considered to be a
match.

The type of condition is embedded in the condition definition.  currently
there is support for regexes.  Other condition types might be added in the
future when the need arises.

regex:
~~~~~~

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


Usage:
------

https://github.com/smetj/experiments/tree/master/pyseps/MapMatch

	$ pyseps debug --config mapmatch.json


Disclaimer:
-----------

*Install the latest Wishbone module from GitHub
https://github.com/smetj/wishbone since this module requires queue auto-
creation.*
