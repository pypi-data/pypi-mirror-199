"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_debts
  $ python setup.py test -s tests.DocsTests.test_docs
"""
from unipath import Path

ROOTDIR = Path(__file__).parent.parent

SETUP_INFO = {}

# load SETUP_INFO:
fn = ROOTDIR.child('lino_tera', 'setup_info.py')
with open(fn, "rb") as fd:
    exec(compile(fd.read(), fn, 'exec'))

from lino.utils.pythontest import TestCase

class PackagesTests(TestCase):

    def test_packages(self):
        self.run_packages_test(SETUP_INFO['packages'])




