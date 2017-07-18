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
    http-address = 8080
    option-bar = value-bar
    option-foo = value-foo
    Installing instance-1.
    http-address = 8081
    option-bar = value-bar
    option-foo = value-foo
    Installing instance-2.
    http-address = 8082
    option-bar = value-bar
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


Depending on the name of the part (``${:_buildout_section_name}`` support)
==========================================================================

Sometimes an option value must include the name of the part. Buildout supports this use case by
providing the special value ``_buildout_section_name_``.

The following example shows how this special value is used is commonly used in the multiple Zope
instances scenario, without using this recipe::

    [instance]
    ...
    http-address = 8080
    special-log-path = /path/to/the/logs/${:_buildout_section_name}.log

    [instance-1]
    <= instance
    http-address = 8081

    [instance-2]
    <= instance
    http-address = 8082

An attempt to adapt the previous example to work with this recipe would look like this::

    [instance]
    ...
    http-address = 8080
    special-log-path = /path/to/the/logs/${:_buildout_section_name}.log

    [instance-multiplier]
    recipe = collective.recipe.zopeinstancemultiplier
    instance-part = instance
    count = 2

This, however, would *fail*. Because the way Buildout works, at the time the recipe has access
to the ``instance`` part to multiply it, the variable substitution would already have occurred.

To make it work a simple adaptation is needed. Simply include an extra dollar sign in order to
escape the variable. Here's an example::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = instance instance-multiplier
    ...
    ... [instance]
    ... recipe = collective.recipe.zopeinstancemultiplier:printer
    ... http-address = 8080
    ... special-log-path = /path/to/the/logs/$${:_buildout_section_name_}.log
    ...
    ... [instance-multiplier]
    ... recipe = collective.recipe.zopeinstancemultiplier
    ... instance-part = instance
    ... count = 2
    ... """)

Running the buildout gives us::

    >>> print 'start', system(buildout)
    start ...
    Installing instance.
    http-address = 8080
    special-log-path = /path/to/the/logs/instance.log
    Installing instance-1.
    http-address = 8081
    special-log-path = /path/to/the/logs/instance-1.log
    Installing instance-2.
    http-address = 8082
    special-log-path = /path/to/the/logs/instance-2.log
    ...

.. References:
.. _`plone.recipe.zope2instance`: https://pypi.python.org/pypi/plone.recipe.zope2instance
