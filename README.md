PySeps
======

What?
-----

A set of Wishbone flow modules to execute pattern matching on a JSON document
stream.

How?
----

The module expects JSON documents coming into the "inbox" queue.  These
documents are then evaluated against one or more conditions.  When all
conditions are fulfilled it will be submitted to the outgoing queue as defined
by the condition.

Conditions are stored into YAML files.  1 YAML file is 1 condition:

::

    ---
    condition:
        "check_command": re:check:host.alive
        "hostgroupnames": in:tag:development

    queue:
        - email:
            from: monitoring@yourdomain.com
            to:
                - oncall@yourdomain.com
            subject: UMI - Host  {{ hostname }} is  {{ hoststate }}.
            template: host_email_alert
    ...


The above example rule will submit the event to the module's queue named
"email" if all defined conditions are met.  The key/values defined under the
"email" section will be added to the event's header.  It's up to the user to
connect another module to the "email" queue to enable further processing of
the event.

These alert conditions are automatically read from disk. The rules directory
is monitored for changes.  The moment the ruleset changes, they are reloaded.


The mapmatch or sequentialmatch modules have to be bootstrapped in a Wishbone
setup:

::

    ---
    modules:

        incoming_events:
            module: wishbone.input.tcp

        json:
            module: wishbone.decode.json

        match_engine:
            module: wishbone.contrib.flow.sequentialmatch

        template:
            module: wishbone.function.template
            arguments:
                key: match_engine
                location: templates/
                header_templates: ["subject"]

        stdout:
            module: wishbone.output.stdout
            arguments:
                complete: true

    routingtable:
      - incoming_events.outbox      -> json.inbox
      - json.outbox                 -> match_engine.inbox
      - match_engine.email          -> template.inbox
      - template.outbox             -> stdout.inbox
    ...



    $ wishbone debug --config example.yaml

Installation
------------

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

