import unittest

from test.modules.executors.bash import correct, errors
from modules.executors.basic.process import ProcessOutput
from modules.executors.languages.bash import BashExecutor


class TestBash(unittest.TestCase):
    def test_execute(self):
        module = BashExecutor()

        test_command = "ls -a"
        test_error_commands = (
            "exit 1",  # Will test for statuscode checking
            "/usr/bin/bash ls -a",  # Will test for "cannot execute binary file"
            "nobodywillnameacommandlikethisbtw",  # Will test for "command not found" check
            "set -u; $VAR; set +u",  # Will test for unbound variable catching
        )

        self.assertEqual(module.execute(test_command).error, False)

        for error_commands in test_error_commands:
            self.assertEqual(module.execute(error_commands).error, True)

    def test_execute_many(self):
        module = BashExecutor()

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

    def test_execute_files(self):
        module = BashExecutor()

        correct_scripts = correct.files
        error_scripts = errors.files

        for i in module.execute_many_files(correct_scripts):
            self.assertIsInstance(i, ProcessOutput)
            self.assertEqual(i.error, False)

        for i in module.execute_many_files(error_scripts):
            self.assertIsInstance(i, ProcessOutput)
            self.assertEqual(i.error, True)

    def test_args_parse(self):
        module = BashExecutor()

        test_commands = (("-i", "-d"), ("--no-windows", "--version"))
        # test_error_commands = (("exit", "1"),)  # TODO: find something without __str__

        for i in test_commands:
            self.assertIsInstance(module.args_merger(i), str)

        # for i in test_error_commands:
        #     self.assertRaises(ValueError, module.args_merger(i))


if __name__ == "__main__":
    unittest.main()
