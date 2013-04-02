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
	"a":{"queue":{"broker":{"broker_key":"a","broker_exchange":""}},"conditions":{"1":"re:a"}},
	"ab":{"queue":{"broker":{"broker_key":"ab","broker_exchange":""}},"conditions":{"1":"re:a","2":"re:b"}},
	"abc":{"queue":{"broker":{"broker_key":"abc","broker_exchange":""}},"conditions":{"1":"re:a","2":"re:b","3":"re:c"}},
	"abcd":{"queue":{"broker":{"broker_key":"abcd","broker_exchange":""}},"conditions":{"1":"re:a","2":"re:b","3":"re:c","4":"re:d"}},
	"abcde":{"queue":{"broker":{"broker_key":"abcde","broker_exchange":""}},"conditions":{"1":"re:a","2":"re:b","3":"re:c","4":"re:d","5":"re:e"}}
	}
::

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
*!re* for positive and negative regular expressions respectively. Keep in mind
that the regular expressions **always** try to match from the beginning of the
string.

examples:

*"re:qwerty"*
Matches if the string is equal to "qwerty".

*"re:qwerty.*"*
Matches if the string starts with "qwerty".

*"re:.*?qwerty.*"*
Matches if the string has "querty" somewhere in the middle.

*"!re:qwerty"*
Matches if the string is NOT equal to "qwerty".


Usage:
------

https://github.com/smetj/experiments/tree/master/pyseps/MapMatch

	$ pyseps debug --config mapmatch.json


Disclaimer:
-----------

**Install the latest Wishbone module from GitHub
https://github.com/smetj/wishbone since this module requires queue auto-
creation.**
