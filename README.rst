.. image:: https://travis-ci.org/collective/collective.recipe.zopeinstancemultiplier.svg?branch=master
   :target: https://travis-ci.org/collective/collective.recipe.zopeinstancemultiplier
   :alt: Build status

Overview
========

This recipe makes it easier to configure multiple Zope instances.


Example usage
=============

We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = instance instance-multiplier
    ...
    ... [instance]
    ... recipe = collective.recipe.zopeinstancemultiplier:printer
    ... http-address = 8080
    ... option-foo = value-foo
    ... option-bar = value-bar
    ...
    ... [instance-multiplier]
    ... recipe = collective.recipe.zopeinstancemultiplier
    ... instance-part = instance
    ... count = 2
    ... """)


The ``instance-multiplier`` part is configured to generate two additional parts,
using the ``instance`` part as a model. Two new parts will be created: ``instance-1`` and
``instance-2``. These parts will be exact clones of the model part, except for the
``http-address`` option, which will be incremented for each part. As a result we we'll have:

* ``instance`` with ``http-address`` equals ``8080``.
* ``instance-1`` with ``http-address`` equals ``8081``.
* ``instance-2`` with ``http-address`` equals ``8082``.

The ``:printer`` recipe just prints out the part options at install time. We don't want to
generate real Zope instances just to test. In real life you would use
`plone.recipe.zope2instance`_.

Running the buildout gives us::

    >>> print 'start', system(buildout)
    start...
    Installing instance.
    option-bar = value-bar
    http-address = 8080
    option-foo = value-foo
    Installing instance-1.
    option-bar = value-bar
    http-address = 8081
    option-foo = value-foo
    Installing instance-2.
    option-bar = value-bar
    http-address = 8082
    option-foo = value-foo
    ...


Support for "ip:port" syntax
============================

The "ip:port" syntax in the ``http-address`` option is also supported::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = my-instance my-instance-multiplier
    ...
    ... [my-instance]
    ... recipe = collective.recipe.zopeinstancemultiplier:printer
    ... http-address = 127.0.0.1:1234
    ...
    ... [my-instance-multiplier]
    ... recipe = collective.recipe.zopeinstancemultiplier
    ... instance-part = my-instance
    ... count = 2
    ... """)

Running the buildout gives us::

    >>> print 'start', system(buildout)
    start...
    Installing my-instance.
    http-address = 127.0.0.1:1234
    Installing my-instance-1.
    http-address = 127.0.0.1:1235
    Installing my-instance-2.
    http-address = 127.0.0.1:1236
    ...


Adding a custom instance
========================

Sometimes you want to have a custom instance in your cluster. To make configuration easier
the "multiplier" part provides an special option containing the next port to be used. You can
use this option like this::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = instance instance-multiplier instance-custom
    ...
    ... [instance]
    ... recipe = collective.recipe.zopeinstancemultiplier:printer
    ... http-address = 8080
    ...
    ... [instance-multiplier]
    ... recipe = collective.recipe.zopeinstancemultiplier
    ... instance-part = instance
    ... count = 2
    ...
    ... [instance-custom]
    ... <= instance
    ... http-address = ${instance-multiplier:next-http-address}
    ... custom-option = custom-value
    ... """)

Running the buildout gives us::

    >>> print 'start', system(buildout)
    start ...
    Installing instance.
    http-address = 8080
    Installing instance-1.
    http-address = 8081
    Installing instance-2.
    http-address = 8082
    ...
    Installing instance-custom.
    custom-option = custom-value
    http-address = 8083

.. References:
.. _`plone.recipe.zope2instance`: https://pypi.python.org/pypi/plone.recipe.zope2instance
