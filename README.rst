Hopak 
######

Formerly project was ``formgear``.

.. image:: https://api.travis-ci.org/xen/hopak.png?branch=master
    :target: https://travis-ci.org/xen/hopak

Main idea behind ``hopak`` allow iteratively create data models in easy 
readable form and use them as part of your websites. At this moment only 
MongoDB is allowed. 

Imagine what happends when you plan to create new site (for yourself or 
client). You doing several steps and one important is make raw draft of what
content you will publish and relation between different types of content. 
Usually it implies you bootstrap your framework, step over several stages of
creating scaffold and only then write models code. In the worst case you write 
SQL. 

But we are living in 21 century, have decoded DNA, pushing frontier into 
space, digging into core of the atoms and listening dubstep! Why we must to 
write all that crap? Why computers cann't just do all this stuff?

So that is why we invent ``hopak``. Because we want computers to do that they
supposed to do. 

`hopak` is only part of this effort, but there are already some results. So,
example how to make simple model. We use `YAML` because it is very human 
readable. Minimal file::

    # user.yaml
    title: User
    description: >
      This is user model. 

    fields:
      - name: name
      - name: email
      - name: site
      - name: about

This file is enough to use it as model in your python code::

    # models.py
    from hopak.models import Model
    class User(Model):
        __yaml__ = 'user.yaml'

``hopak`` is only a library for bigger framework, if you decide to use the whole 
stack then you will get site with admin section including list, edit, add, 
search, delete sections for each models.

Changes
========

0.5:

- Python 3 support

0.4.2: 

- urgent fix for non saving model instances 

0.4.1:

- fix release, added ``hopak.ds`` to package

0.4:

- renamed from ``formgear`` to ``hopak``

0.3.5:

- added independed data sources, but atm still have only mongodb datasource

0.3.4: 

- Started this log.

More
======

Links:

* ``hopak`` page on PyPI: `http://pypi.python.org/pypi/hopak/ 
  <http://pypi.python.org/pypi/hopak/>`_
* Github page: `https://github.com/xen/hopak 
  <https://github.com/xen/hopak>`_

More documentation is approaching.


