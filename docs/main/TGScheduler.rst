
TurboGears2 Scheduled Tasks
==============================

:Status: Work in progress

.. contents:: Table of Contents
    :depth: 2

TGScheduler is an implementation of the TG1 Scheduler for TG2

Installing Stuff
----------------------

  easy_install TGScheduler

Creating A Scheduler
----------------------------

In order to add scheduled tasks to your project you will need to create a launcher.

Ex: myproj/config/cron.py::

    from TGScheduler import start_scheduler
    from TGScheduler.scheduler import add_interval_task, add_weekday_task

    def myTask():
        print "running my scheduled task"


    def schedule():
        start_scheduler() # start the scheduler thread

        add_interval_task(action=myTask, initialdelay=10, interval=60) # run this once an hour

        add_weekday_task(action=myTask, weekdays=range(1-8), timeonday=(19, 0)) # run at 7 pm everyday


Adding Your Scheduler to your project
--------------------------------------

Add to end of myproj/config/app_cfg.py::

  from myproj.config.cron import schedule
  base_config.call_on_startup = [schedule]


More Information
-----------------

More Usage Examples can be found on http://docs.turbogears.org/1.0/Scheduler

