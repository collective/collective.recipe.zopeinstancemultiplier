# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1.0'

long_description = '\n'.join([
    read('README.rst'),
    read('docs', 'HISTORY.rst')
])

tests_require = [
    'zc.buildout[test]',
    'zope.testing',
]


setup(
    name='collective.recipe.zopeinstancemultiplier',
    version=version,
    description='Makes it easier to configure multiple Zope instances.',
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        'Framework :: Buildout :: Recipe',
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Build Tools',
    ],
    keywords='zc.buildout buildout recipe supervisor',
    author='Rafael Oliveira',
    author_email='rafaelbco@gmail.com',
    url='https://github.com/collective/collective.recipe.zopeinstancemultiplier',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.recipe'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zc.buildout',
    ],
    tests_require=tests_require,
    extras_require={'tests': tests_require},
    test_suite='collective.recipe.zopeinstancemultiplier.tests.test_docs.test_suite',
    entry_points={
        'zc.buildout': [
            'default = collective.recipe.zopeinstancemultiplier:Recipe',
            'printer = collective.recipe.zopeinstancemultiplier:PrinterRecipe',
        ]},
)
