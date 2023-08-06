from typing import TYPE_CHECKING, Optional

from astroid import nodes, ClassDef, Call, Name, Keyword, Const
from pylint.checkers import BaseChecker

COMMAND_ARG_IS_NO_TYPE = "tango-command-arg-is-no-type"

HAS_NO_TYPE_ANNOTATION = "tango-command-arg-has-no-type-annotation"

NO_RETURN_TYPE = "tango-no-return-type"

NOT_MATCH_RETURN_TYPE = "tango-dtype-out-does-not-match-return-type"

DTYPE_OUT_MISSING = "tango-function-returns-but-dtype-out-missing"

GIVEN_BUT_IS_NONE = "tango-dtype-out-given-but-is-none"

MATCH_ARGUMENT_TYPE = "tango-dtype-in-does-not-match-argument-type"

NO_DTYPE_IN_BUT_ARGUMENT = "tango-no-dtype-in-but-argument"

DTYPE_IN_BUT_NO_ARGUMENT = "tango-dtype-in-but-no-argument"

COMMAND_RETURN_TYPE_IS_INVALID = "command-return-type-invalid"

DTYPE_OUT_INVALID = "dtype-out-invalid"

if TYPE_CHECKING:
    from pylint.lint import PyLinter

# Enable this for debugging
# logging.basicConfig(level=logging.INFO)


class TangoCommandDtype(BaseChecker):
    name = "tango-command-dtype"
    msgs = {
        "W5401": (
            'Tango @command with "dtype_in", but without a single argument (except self)',
            DTYPE_IN_BUT_NO_ARGUMENT,
            "",
        ),
        "W5402": (
            'Tango @command without "dtype_in", but with an argument (except self)',
            NO_DTYPE_IN_BUT_ARGUMENT,
            "",
        ),
        "W5403": (
            '"dtype_in" type does not match type annotation',
            MATCH_ARGUMENT_TYPE,
            "",
        ),
        "W5404": (
            'Tango @command with "dtype_out", but the function returns "None"',
            GIVEN_BUT_IS_NONE,
            "",
        ),
        "W5405": (
            'Tango @command with return value, but "dtype_out" missing',
            DTYPE_OUT_MISSING,
            "",
        ),
        "W5406": (
            "Return type annotation does not match dtype_out",
            NOT_MATCH_RETURN_TYPE,
            "",
        ),
        "W5407": (
            "Tango @command has no return type annotation",
            NO_RETURN_TYPE,
            "",
        ),
        "W5408": (
            "Tango @command argument has no type annotation",
            HAS_NO_TYPE_ANNOTATION,
            "",
        ),
        "W5409": (
            'Tango @command has "dtype_in" which is not a proper type annotation',
            COMMAND_ARG_IS_NO_TYPE,
            "",
        ),
        "W5410": (
            'Tango @command has an invalid return type annotation (superfluous " maybe?)',
            COMMAND_RETURN_TYPE_IS_INVALID,
            "",
        ),
        "W5411": (
            'Tango @command "dtype_out" is invalid',
            DTYPE_OUT_INVALID,
            "",
        ),
    }

    def __init__(self, linter: Optional["PyLinter"] = None) -> None:
        super().__init__(linter)

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        # These would be freestanding functions, and we don't care about those.
        if not isinstance(node.parent, ClassDef):
            return
        parent: ClassDef = node.parent
        # Here we check if the parent class is called "Device". This doesn't check if it's a tango.server.Device,
        # because I don't know how to do that. But if the plugin is only used in Tango projects, this should have low
        # probability of false positives
        if not any(x.name == "Device" for x in parent.bases):
            return
        # Find the decorator called "command". Again, doesn't check if it's tango.server.command, see above.
        command_decorator = next(
            iter(
                x
                for x in node.decorators.nodes
                if isinstance(x, Call)
                and x.func is not None
                and isinstance(x.func, Name)
                and x.func.name == "command"
            ),
            None,
        )
        if command_decorator is None:
            return

        def find_decorator_keyword(kw_arg: str) -> Optional[Keyword]:
            return next(
                iter(kw.value for kw in command_decorator.keywords if kw.arg == kw_arg),
                None,
            )

        dtype_in_value = find_decorator_keyword("dtype_in")
        # Argument length 2 means we have "self" (hopefully) and a single argument
        if dtype_in_value is not None and len(node.args.args) != 2:
            self.add_message(DTYPE_IN_BUT_NO_ARGUMENT, node=node)
            return
        # Without dtype_in, only 1 (i.e. only self as argument) is allowed.
        if dtype_in_value is None and len(node.args.args) != 1:
            self.add_message(NO_DTYPE_IN_BUT_ARGUMENT, node=node)
            return
        first_arg = node.args.annotations[1]
        if first_arg is None:
            self.add_message(HAS_NO_TYPE_ANNOTATION, node=node)
            return
        # This can happen with: def foo(bar: "baz"), so using a string as annotation.
        if not isinstance(first_arg, Name):
            self.add_message(COMMAND_ARG_IS_NO_TYPE, node=node)
            return
        first_arg_type = first_arg.name
        # For dtype_in, we allow both strings, as in 'dtype_in="str"' as well as 'dtype_in=str'.
        # For the former, the type is a Name, for the latter, it's Const(str) with a value that's a string.
        if dtype_in_value is not None and (
            isinstance(dtype_in_value, Name)
            and dtype_in_value.name != first_arg_type
            or (
                isinstance(dtype_in_value, Const)
                and dtype_in_value.value != first_arg_type
            )
        ):
            self.add_message(MATCH_ARGUMENT_TYPE, node=node)
            return

        return_type = node.returns
        if return_type is None:
            self.add_message(NO_RETURN_TYPE, node=node)
            return
        dtype_out = find_decorator_keyword("dtype_out")
        if isinstance(return_type, Const) and return_type.value is None:
            if dtype_out is not None:
                self.add_message(GIVEN_BUT_IS_NONE, node=node)
            return
        if dtype_out is None:
            self.add_message(DTYPE_OUT_MISSING, node=node)
            return
        # The return type could be a string
        if not isinstance(return_type, Name):
            self.add_message(COMMAND_RETURN_TYPE_IS_INVALID, node=node)
            return
        if not isinstance(dtype_out, Name) and not isinstance(dtype_out, Const):
            self.add_message(DTYPE_OUT_INVALID, node=node)
            return
        if (isinstance(dtype_out, Name) and dtype_out.name != return_type.name) or (
            isinstance(dtype_out, Const) and dtype_out.value != return_type.name
        ):
            self.add_message(NOT_MATCH_RETURN_TYPE, node=node)
            return


def register(linter: "PyLinter") -> None:
    """This required method auto registers the checker during initialization.

    :param linter: The linter to register the checker to.
    """
    linter.register_checker(TangoCommandDtype(linter))
