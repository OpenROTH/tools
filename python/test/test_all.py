import sys
import os
import unittest
import argparse
import hashlib

sys.path.append(os.path.abspath(__file__ + "\..\.."))

def make_suite(testcase_class, path):
    testloader = unittest.TestLoader()
    testnames = testloader.getTestCaseNames(testcase_class)
    suite = unittest.TestSuite()
    for name in testnames:
        suite.addTest(testcase_class(name, path=path))
    return suite

def get_hash_file(filename):
    m = hashlib.sha1()
    m.update(open(filename, "rb").read())
    return m.hexdigest()
    
def get_hash_buf(buf):
    m = hashlib.sha1()
    m.update(buf)
    return m.hexdigest()
    
class AllFileTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest', path=""):
        super(AllFileTestCase, self).__init__(methodName)
        self.path = path

    def test_parse_build(self):
        from all.all_parser import AllFile
        from all.all_parser import all_file_s as all_file_struct
        file_path = os.path.join(self.path, "DATA", "ICONS.ALL")
        hfile = get_hash_file(file_path)
        allf = AllFile(file_path)
        buf = all_file_struct.build(allf.all_file_c)
        hbuf = get_hash_buf(buf)
        self.assertEqual(hfile, hbuf)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test launch options')
    parser.add_argument('roth_path', action='store', default='', help='roth path')
    args = parser.parse_args()

    alltests = unittest.TestSuite()
    alltests.addTest(make_suite(AllFileTestCase, args.roth_path))
    result = unittest.TextTestRunner(verbosity=2).run(alltests)
    sys.exit(not result.wasSuccessful())