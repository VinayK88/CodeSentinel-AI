import unittest
from codesentinel.rules import scan_diff
from codesentinel.validator import validate

class TestRules(unittest.TestCase):
    def test_detects_security_changes(self):
        diff = (
            '+api_key = "abcdefghijklmnop"\n'
            '+requests.get(url, verify=False)\n'
            '+subprocess.run(cmd, shell=True)\n'
        )
        ids={f.rule_id for f in validate(scan_diff(diff))}
        self.assertTrue({"SECRET","TLS","SHELL"}.issubset(ids))

    def test_ignores_context_lines(self):
        self.assertEqual(scan_diff(' api_key = "abcdefghijklmnop"'), [])

if __name__ == '__main__': unittest.main()
