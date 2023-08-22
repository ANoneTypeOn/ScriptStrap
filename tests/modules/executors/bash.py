import unittest

from modules.dataclasses.process import ProcessOutput
from modules.executors.files.bash import BashModule


class TestBash(unittest.TestCase):
    def test_execute(self):
        module = BashModule()

        test_command = "ls -a"
        test_error_command = "exit 1"  # TODO: find a real one to test

        self.assertEqual(module.execute(test_command).error, False)
        self.assertEqual(module.execute(test_error_command).error, True)

    def test_execute_many(self):
        module = BashModule()

        test_commands = ("ls -a", ("ls", "-a"), "sh --version", ("sh", "--version"))
        test_error_commands = ("exit 1", ("exit", "1"))  # TODO: find a real one to test

        results = module.execute_many(test_commands)
        self.assertIsInstance(results, tuple)

        for i in results:
            self.assertIsInstance(i, ProcessOutput)
            self.assertEqual(i.error, False)

        results_error = module.execute_many(test_error_commands)
        self.assertIsInstance(results_error, tuple)

        for i in results_error:
            self.assertIsInstance(i, ProcessOutput)
            self.assertEqual(i.error, True)

    def test_args_parse(self):
        module = BashModule()

        test_commands = (("-i", "-d"), ("--no-windows", "--version"))
        test_error_commands = (("exit", "1"),)  # TODO: find smth without __str__

        for i in test_commands:
            self.assertIsInstance(module.args_merger(i), str)

        for i in test_error_commands:
            self.assertRaises(ValueError, module.args_merger(i))


if __name__ == "__main__":
    unittest.main()
