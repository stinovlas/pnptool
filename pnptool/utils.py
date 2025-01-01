from functools import wraps
from typing import Callable, ParamSpec, TypeVar

import click
import cloup
from cloup import Context
from cloup.constraints import mutually_exclusive
from rich.console import Console

from .settings import Verbosity

T = TypeVar("T")
P = ParamSpec("P")


class IntTupleType(click.ParamType):
    name = "integer list"

    def convert(self, value: str, param: str, ctx: Context):
        try:
            # Add -1 shift because lists are 0-indexed
            pages = tuple(int(v) - 1 for v in value.split(","))
            if any(p < 0 for p in pages):
                raise ValueError
            return pages
        except ValueError:
            self.fail(
                f"{value!r} is not a valid comma separated positive integer list",
                param,
                ctx,
            )


def common_options(func: Callable[P, T]) -> Callable[P, T]:
    """Common CLI options."""

    @cloup.option_group(
        "Verbosity options",
        cloup.option("-v", "--verbose", is_flag=True, help="Enable verbose output."),
        cloup.option("-q", "--quiet", is_flag=True, help="Silence all output."),
        constraint=mutually_exclusive,
    )
    @cloup.pass_context
    @wraps(func)
    def _wrapper(
        ctx: Context, *args: P.args, quiet: bool, verbose: bool, **kwargs: P.kwargs
    ) -> T:
        if quiet:
            ctx.obj["verbosity"] = Verbosity.SILENT
        elif verbose:
            ctx.obj["verbosity"] = Verbosity.VERBOSE
        else:
            ctx.obj["verbosity"] = Verbosity.INFO
        return func(*args, **kwargs)

    return _wrapper


_CONSOLE = Console(highlight=False)

print = _CONSOLE.print
status = _CONSOLE.status
