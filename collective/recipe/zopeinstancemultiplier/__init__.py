# -*- coding: utf-8 -*-
"""Recipe environment."""


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        instance_part_name = options['instance-part']
        count = int(options['count'])
        instance_part = buildout[instance_part_name]
        base_http_address = instance_part['http-address']
        if ':' in base_http_address:
            (base_ip, base_port) = base_http_address.split(':')
        else:
            (base_ip, base_port) = None, base_http_address
        base_port = int(base_port)

        for new_instance_number in xrange(1, count + 1):
            new_instance_part = dict(instance_part)
            new_port = base_port + new_instance_number
            new_instance_part['http-address'] = self._format_http_address(base_ip, new_port)
            new_instance_name = '{}-{}'.format(instance_part_name, new_instance_number)
            self._replace_part_name(new_instance_part, new_instance_name)
            buildout[new_instance_name] = new_instance_part

        self._replace_part_name(instance_part, instance_part_name)

        options['next-http-address'] = self._format_http_address(base_ip, base_port + count + 1)

    def _format_http_address(self, ip, port):
        return '{}:{}'.format(ip, port) if ip else str(port)

    def _replace_part_name(self, part, part_name):
        for (k, v) in part.iteritems():
            part[k] = v.replace('$${:_buildout_section_name_}', part_name)

    def install(self):
        return ()

    update = install


class PrinterRecipe(object):
    """Recipe to print its options.

    Useful for testing.
    """

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.options = options

    def install(self):
        print '\n'.join(
            '{} = {}'.format(k, v)
            for (k, v) in sorted(self.options.iteritems())
            if k != 'recipe'
        )
        return ()
