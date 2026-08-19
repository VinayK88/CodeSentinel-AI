import unittest
from codesentinel.lifecycle import FindingLifecycle

class TestLifecycle(unittest.TestCase):
    def test_verified_requires_remediation(self):
        f=FindingLifecycle('F-1')
        f.accept(); f.remediate('abc123'); f.verify()
        self.assertEqual(f.state, 'verified')
        self.assertTrue(f.verified)

    def test_cannot_verify_without_fix(self):
        with self.assertRaises(ValueError):
            FindingLifecycle('F-2').verify()

if __name__ == '__main__': unittest.main()
