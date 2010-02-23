
.. _schuduling_tasks:

================
Scheduling Tasks
================

On Posix systems, using cron is a perfectly valid way to schedule
tasks for your application.  See :ref:`cli_script` for an example of
script that can access all of the application model and internals and
that is therefore an ideal target for a cron job.

However, it sometimes happen that you need to interact intimately with
the runtime environment of your application, that you need to schedule
jobs dynamically, or that your hosting service does not provide access
to cron.  In those cases, you can schedule jobs with the `TGScheduler`
module.

Installation
------------

`TGScheduler` is registered on PyPI and therefore can be installed
with `easy_install`:

.. code-block:: bash

    $ easy_install tgschuduler


Setup
-----

`TGScheduler` is not started by default.  To allow your tasks to run,
simply start the scheduler when your application is loaded.  You can
do that in `lib/app_globals.py`:

.. code-block:: python

    import tgscheduler

    class Globals(object):
        def __init__(self):
	    tgscheduler.start_scheduler()


Scheduling Tasks
----------------

To you have four ways to schudule tasks:

* `add_interval_task()`;
* `add_monthly_task()`;
* `add_single_task()`;
* `add_weekday_task()`.

Each of those receive a callable and a time specifier that defines
when to run a function.  As an example, if you want to update the
stock prices in your database every 15 minutes, you would do something
like the following:

.. code-block:: python

    def update_stocks():
        url = 'http://example.com/stock_prices.xml'
        data = urllib2.urlopen(url).read()
	etree = lxml.etree.fromtsring(data)
	for el in etree.xpath("//stock"):
	    price = model.StockPrice(el.get("name"), int(el.get("price")))
	    model.DBSession.add(price)

    class Globals(object):
        def __init__(self):
	    tgscheduler.start_scheduler()
	    tgscheduler.add_interval_task(60*15, update_stocks)


