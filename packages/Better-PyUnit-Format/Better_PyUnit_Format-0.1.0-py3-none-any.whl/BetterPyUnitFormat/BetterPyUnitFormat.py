import unittest
from math import ceil


class BetterPyunitFormatResult(unittest.TestResult):
    class Colors:
        RED = u"\u001b[31m"
        GREEN = u"\u001b[32m"
        YELLOW = u"\u001b[33m"
        RESET = u"\u001b[0m"

    RUN = {
        'color': Colors.GREEN,
        'text': "RUN"
    }
    OK = {
        'color': Colors.GREEN,
        'text': "OK"
    }
    FAIL = {
        'color': Colors.RED,
        'text': "FAIL"
    }
    PASSED = {
        'color': Colors.GREEN,
        'text': "PASSED"
    }
    FAILED = {
        'color': Colors.RED,
        'text': "FAILED"
    }

    SKIP = {
        'color': Colors.YELLOW,
        'text': "SKIP"
    }
    ERROR = {
        'color': Colors.RED,
        'text': "ERROR"
    }

    MAX_CONTENT = 8

    @classmethod
    def printStatus(cls, _statusMessage, _alignment: str):
        if len(_statusMessage['text']) > cls.MAX_CONTENT:
            raise AttributeError(f"Status message too large. {len(_statusMessage['text'])}")

        space = ""
        if _alignment == "LEFT":
            space = f"{_statusMessage['text']: <{cls.MAX_CONTENT}}"

        elif _alignment == "RIGHT":
            space = f"{_statusMessage['text']: >{cls.MAX_CONTENT}}"

        elif _alignment == "CENTER":
            space = f"{_statusMessage['text']: ^{cls.MAX_CONTENT}}"

        print(f"{_statusMessage['color']}[ {space} ]{cls.Colors.RESET}", end=" ")

    def startTestRun(self) -> None:
        super().startTestRun()
        print("=" * 20)

    def startTest(self, test: unittest.case.TestCase) -> None:
        super().startTest(test)
        print("-" * 20)
        self.printStatus(self.RUN, "LEFT")
        print(f"{test.shortDescription()} ({test.id()})")

    def addError(self, test: unittest.case.TestCase, err) -> None:
        super().addError(test, err)
        self.printStatus(self.ERROR, "RIGHT")
        print(test.shortDescription())
        print(f"{self.Colors.RED}A(n) {err[0].__qualname__} occurred:")
        print(f"[{err[0].__qualname__}] {err[1]}")
        print(self.Colors.RESET)

    def addFailure(self, test: unittest.case.TestCase, err) -> None:
        super().addFailure(test, err)
        self.printStatus(self.FAIL, "RIGHT")
        print(test.shortDescription())
        print(f"{self.Colors.RED}Failure reason:")
        print(err[1])
        print(self.Colors.RESET)

    def addSkip(self, test: unittest.case.TestCase, reason: str) -> None:
        super().addSkip(test, reason)
        self.printStatus(self.SKIP, "RIGHT")
        print(test.shortDescription())
        print(f"{self.Colors.YELLOW}Skip Reason: {reason}{self.Colors.RESET}")

    def addSuccess(self, test: unittest.case.TestCase) -> None:
        super().addSuccess(test)
        self.printStatus(self.OK, "RIGHT")
        print(test.shortDescription())

    def stopTest(self, test: unittest.case.TestCase) -> None:
        super().stopTest(test)
        print("-" * 20, "\n")

    def stopTestRun(self) -> None:
        print("=" * 20)
        if not self.wasSuccessful():
            self.printStatus(self.FAILED, "CENTER")
            print()
        else:
            self.printStatus(self.PASSED, "CENTER")
            print()

        successes = self.testsRun - len(self.failures) - len(self.errors) - len(self.skipped)
        print(f"{successes} tests passed.\n"
              f"{len(self.failures)} tests failed.\n"
              f"{len(self.errors)} tests errored.\n"
              f"{len(self.skipped)} tests skipped.")

        print(f"{successes} / {self.testsRun}")

        print("=" * 20)

