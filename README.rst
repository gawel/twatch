Twitter watch
================================================

Watch and print search query on twitter.

Install it::

    $ pip install -e git+git@github.com:gawel/twatch.git#egg=twatch

You'll need a config file like::


    [twitter]
    key=yourkey
    secret=yoursecret
    token=yourtoken
    token_secret=yourtokensecret

    [twatches]
    search1=python OR afpy
    me=from:gawel_

Then run twatch::

    $ twatch

Get a small help with::

    $ twatch -h
