# -*- coding: UTF-8 -*-
# Copyright 2017-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# $ python setup.py test -s tests.PackagesTests.test_packages

SETUP_INFO = dict(
    name='lino-tera',
    version='23.3.0',
    install_requires=['lino-xl'],
    # tests_require=['pytest', 'mock'],
    test_suite='tests',
    description=("A Lino for managing therapeutic centres"),
    long_description="""\

Lino Tera is a customizable management system for therapeutic centres.

- Project homepage: https://gitlab.com/lino-framework/tera

- Documentation:
  https://lino-framework.gitlab.io/tera/

- Functional specification see
  https://www.lino-framework.org/specs/tera

- There is also a User's Manual in German: `online using Sphinx
  <https://tera.lino-framework.org/de>`__ (work in progress) and `PDF
  using LibreOffice
  <https://gitlab.com/lino-framework/tera/raw/master/docs/dl/Handbuch_Lino_Tera.pdf>`__
  (not maintained).

- For *introductions* and *commercial information* about Lino Tera
  please see `www.saffre-rumma.net
  <https://www.saffre-rumma.net>`__.



""",
    author='Rumma & Ko Ltd',
    author_email='info@lino-framework.org',
    url="https://gitlab.com/lino-framework/tera",
    license_files=['COPYING'],
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 4 - Beta
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
Intended Audience :: Information Technology
Intended Audience :: Customer Service
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: OS Independent
""".splitlines())

SETUP_INFO.update(packages=[str(n) for n in """
lino_tera
lino_tera.lib
lino_tera.lib.contacts
lino_tera.lib.contacts.fixtures
lino_tera.lib.cal
lino_tera.lib.cal.fixtures
lino_tera.lib.coachings
lino_tera.lib.coachings.fixtures
lino_tera.lib.courses
lino_tera.lib.courses.fixtures
lino_tera.lib.households
lino_tera.lib.households.fixtures
lino_tera.lib.lists
lino_tera.lib.lists.fixtures
lino_tera.lib.notes
lino_tera.lib.notes.fixtures
lino_tera.lib.sales
lino_tera.lib.sales.fixtures
lino_tera.lib.products
lino_tera.lib.teams
lino_tera.lib.teams.fixtures
lino_tera.lib.tera
lino_tera.lib.tera.fixtures
lino_tera.lib.users
lino_tera.lib.users.fixtures
lino_tera.lib.invoicing
lino_tera.lib.invoicing.fixtures
""".splitlines() if n])

SETUP_INFO.update(message_extractors={
    'lino_tera': [
        ('**/cache/**',          'ignore', None),
        ('**.py',                'python', None),
        ('**.js',                'javascript', None),
        ('**/config/**.html', 'jinja2', None),
    ],
})

SETUP_INFO.update(include_package_data=True, zip_safe=False)
# SETUP_INFO.update(package_data=dict())


# def add_package_data(package, *patterns):
#     l = SETUP_INFO['package_data'].setdefault(package, [])
#     l.extend(patterns)
#     return l

# l = add_package_data('lino_noi.lib.noi')
# for lng in 'de fr'.split():
#     l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
