# Divvy

Our *hack.summit()* submission is **divvy**, a content delivery platform. Content sources
can be added to a user's "buckets", and each of these buckets is configured with a
delivery schedule. Divvy will then deliver the content (either via email or SMS) to the
user on a set interval.

Content can come from a variety of sources. For the hackathon, we implemented two main
source types: *RSS* and *Reminder*. RSS will poll an RSS feed for content, while the
Reminder source type is used to send yourself a helpful reminder, such as to get out
of your chair and stretch every hour to combat fatigue and posture problems.

## Installation/Configuration

To install Divvy, you will need to first install its dependencies. We have included a
`packages.list` file to make this easier:

````
$ git clone https://github.com/cougarcoders/hackathon.git divvy
$ cd divvy
$ pip install -r divvy/packages.list
````

Next, you will need to initialize the database:

````
$ python manage.py initdb
````

## Starting Divvy

Divvy is made of two components: the web application and the scheduling engine. They each
exist in a separate process.

To launch the web application:

````
$ python manage.py runserver
````

To launch the scheduling engine:

````
$ python -m divvy.divvy_scheduler
````

## Beyond the hackathon

There are several features we wished we would have had time to implement in Divvy that
just didn't make the cut. If we were to continue this project, here are some of the things
that we would hope to add:

- "Random <thing>" content source (i.e., random Wikipedia page)
- The ability to configure delivery methods per-bucket, and not just per-account
- User-provided cell carrier information, rather the current brute-force delivery approach
- More robust exception handling for a resilient system
- Have the `runserver` Manager task invoke both the web application **and** the scheduling engine
- A more pleasing user interface
- Quiet hours for the delivery schedules (e.g., don't bother me while I'm sleeping!)

That being said, we are proud of what we were able to accomplish, and had a blast doing it!
