Formgear
#########

.. image:: https://secure.travis-ci.org/xen/formgear.png
    :target: https://travis-ci.org/#!/xen/formgear

Main idea behind ``formgear`` allow iteratively create data models in easy 
readeable form and use them as part of your websites. At this moment only 
MongoDB is allowed. 

Imagine what happends when you plan to create new site (for yourself or 
client). You doing several steps and one important is make row draft of what
content you will publish and retation between different types of content. 
Usually it implies you bootstrap your framework, step over several stages of
creating scaffold and only then write models code. In the worst case you write 
SQL. 

But we are living in 21 century, have decoded DNA, pushing frontier into 
space, diging into core of the atoms and listening dubstep! Why we must to 
write all that crap? Why computers cann't just do all this stuff?

So that is why we invent ``formgear``. Because we want computers to do that they
supposed to do. 

`formgear` is only part of this effort, but here is already some results. So,
example how to make simple model. We use `YAML` because it is very human 
readeable. Minimal file::

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
    from formgear.models import Model
    class User(Model):
        __yaml__ = 'user.yaml'

``formgear`` is only a library for bigger framework, if you deside to use whole 
stack then you will get site with admin section including list, edit, add, 
search, delete sections for each models.

Changes
========

0.3.4: 

- Started this log.

More
======

Links:

* ``formgear`` page on PyPI: `http://pypi.python.org/pypi/formgear/ 
  <http://pypi.python.org/pypi/formgear/>`_
* Github page: `https://github.com/xen/formgear 
  <https://github.com/xen/formgear>`_

More documentation is approaching.


