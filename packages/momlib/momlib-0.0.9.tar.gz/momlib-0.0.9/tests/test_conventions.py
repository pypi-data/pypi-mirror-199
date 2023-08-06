# type: ignore

# This file should be removed at some point (because it's quite
# terrible), but for the time being it is useful to make sure everything
# passes.

import unittest
import re
from types import FunctionType
from inspect import signature, Signature, _empty as inspect_empty

import momlib


class TestConventions(unittest.TestCase):
    def test_function_signatures(self):
        def test_sig(func_name: str, sig: Signature, collection: str):

            # check parameter annotations (required for all but
            # self)
            for pk in sig.parameters.keys():
                param = sig.parameters[pk]
                for c in param.name:
                    if c not in "abcdefghijklmnopqrstuvwxyz_":
                        self.fail(
                            f"Parameter `{param.name}` of function "
                            f"<{func_name}> "
                            f"in '{collection}' has illegal character \"{c}\""
                        )
                if param.annotation == inspect_empty:
                    if param.name != "self":
                        self.fail(
                            f"Function <{func_name}> in '{collection}' "
                            "does not have type annotation on parameter "
                            f"`{param.name}`"
                        )

            # check return type annotation (required)
            if sig.return_annotation == inspect_empty:
                self.fail(
                    f"Function <{func_name}> in '{collection}' "
                    "does not have return type annotation"
                )

            # whitelist check for characters in function name
            for c in func_name:
                if c not in "abcdefghijklmnopqrstuvwxyz_":
                    self.fail(
                        f"Function <{func_name}> "
                        f"in '{collection}' has illegal character \"{c}\""
                    )

        for name, item in momlib.Matrix.__dict__.items():
            if isinstance(item, FunctionType) and name != "overload":
                test_sig(
                    name,
                    signature(item),
                    "momlib/_matrix.py",
                )
        for name, item in momlib.Vector.__dict__.items():
            if isinstance(item, FunctionType) and name != "overload":
                test_sig(
                    name,
                    signature(item),
                    "momlib/_vector.py",
                )
        for name, item in momlib._linalg.__dict__.items():
            if isinstance(item, FunctionType) and name != "overload":
                test_sig(
                    name,
                    signature(item),
                    "momlib/_linalg.py",
                )

    def test_function_docstrings(self):

        word_chr_re = r"[a-zA-Z0-9'_-]"
        punctuation_re = r"""[~`@#$%\^&*()_\-\+=\{\}\[\]\\|:;'"<>,\./]"""
        indent_re = r"(\ {4})*"
        varname_re = r"(\*{0,2}[a-z_]+)"
        err_name_re = r"([A-Z][a-zA-Z]+)"
        break_re = rf"( |\n{indent_re})"
        cap_word_re = rf"([A-Z0-9]{word_chr_re}*)"
        sentence_re = (
            rf"({cap_word_re}{punctuation_re}*"
            rf"({break_re}{punctuation_re}*{word_chr_re}+{punctuation_re}*)*"
            r"(\.|!|\?|\.\.\.))"
        )
        text_block_re = rf"{sentence_re}({break_re}{sentence_re})*"
        docstr_re = (
            r"^"
            rf"\n{indent_re}{text_block_re}\n"
            rf"(\n{indent_re}Arguments\n"
            rf"({indent_re}-\ {varname_re}:\ {text_block_re}\n)+)?"
            rf"(\n{indent_re}Possible\ Errors\n"
            rf"({indent_re}-\ {err_name_re}:\ {text_block_re}\n)+)?"
            rf"(\n{indent_re}Notes\n"
            rf"({indent_re}-\ {text_block_re}\n)+)?"
            rf"{indent_re}$"
        )
        docstr_pattern = re.compile(docstr_re)

        def test_doc(func_name: str, doc_str: str, collection: str):
            if doc_str is not None:
                self.assertIsNotNone(
                    docstr_pattern.match(doc_str),
                    f"Function <{func_name}> "
                    f"in '{collection}' has a malformed docstring.",
                )
                for line in doc_str.split("\n"):
                    if len(line) > 72:
                        self.fail(
                            f"Function <{func_name}> "
                            f"in '{collection}' has a docstring that "
                            "overruns the allowed 72 character "
                            "horizontal space.",
                        )
            else:
                self.fail(
                    f"Function <{func_name}> "
                    f"in '{collection}' has no docstring.",
                )

        for name, item in momlib.Matrix.__dict__.items():
            if isinstance(item, FunctionType) and name != "overload":
                test_doc(
                    name,
                    item.__doc__,
                    "momlib/_matrix.py",
                )
        for name, item in momlib.Vector.__dict__.items():
            if isinstance(item, FunctionType) and name != "overload":
                test_doc(
                    name,
                    item.__doc__,
                    "momlib/_vector.py",
                )
        for name, item in momlib._linalg.__dict__.items():
            if isinstance(item, FunctionType) and name != "overload":
                test_doc(
                    name,
                    item.__doc__,
                    "momlib/_linalg.py",
                )


if __name__ == "__main__":
    unittest.main()
