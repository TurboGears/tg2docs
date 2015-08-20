
.. _schuduling_tasks:

================
Scheduling Tasks
================

On Posix systems, using cron is a perfectly valid way to schedule
tasks for your application.

However, it sometimes happen that you need to interact intimately with
the runtime environment of your application, that you need to schedule
jobs dynamically, or that your hosting service does not provide access
to cron.  In those cases, you can schedule jobs with the `TGScheduler`
module.

Installation
------------

`TGScheduler` is registered on PyPI and therefore can be installed
with `pip install`:

.. code-block:: bash

    $ pip install tgscheduler


Setup
-----

`TGScheduler` is not started by default.  To allow your tasks to run,
simply start the scheduler when your application is loaded configured.

You can do that in ``config/app_cfg.py``:

.. code-block:: python

    def start_tgscheduler():
        import tgscheduler
        tgscheduler.start_scheduler()

    from tg.configuration import milestones
    milestones.config_ready.register(start_tgscheduler)

Using a :ref:`config_milestones` ensures that our scheduler is not
started twice, it is also suggested to register tasks inside
the ``start_tgscheduler`` function so that they are not
scheduled twice.

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

    def start_tgscheduler():
        import tgscheduler
        tgscheduler.start_scheduler()
        tgscheduler.add_interval_task(60*15, update_stocks)

    from tg.configuration import milestones
    milestones.config_ready.register(start_tgscheduler)

.. note::

    Inside the scheduled tasks you won't have TurboGears automatically
    flushing and committing transactions for you, so remember to add
    a ``transaction.commit()`` call a the end of your tasks if your
    application is relying on the transaction manager.