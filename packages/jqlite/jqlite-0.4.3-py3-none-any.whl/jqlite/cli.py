import json
import os
import sys
import typer
from termcolor import cprint
from typing import Optional

from jqlite.core import json_ops
from jqlite.core.filters import Identity, Value
from jqlite.core.parser import parse
from . import __version__


def main():
    typer.run(run)


def version_callback(value: bool):
    if value:
        typer.echo(f"jqlite version {__version__}")
        raise typer.Exit()


def run(
    expr: Optional[str] = typer.Argument(None),
    null_stdin: bool = typer.Option(
        False, "--null-stdin", "-n", help="Do not read from stdin, using null as input."
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Output jqlite version and exit.",
    ),
):
    f = parse(expr) if expr else Identity()
    if null_stdin:
        json_obj = None
    else:
        json_str = sys.stdin.read()
        json_obj = json.loads(json_str)
    for v in f.input(json_obj):
        if os.isatty(sys.stdout.fileno()):
            json_print(v)
            print()
        else:
            print(json.dumps(v, indent=2))


def json_print(obj: Value, indent=2, level=0):
    if obj is None:
        cprint(json_ops.to_string(obj), "cyan", end="")
    elif isinstance(obj, bool):
        cprint(json_ops.to_string(obj), "yellow", end="")
    elif isinstance(obj, (int, float)):
        cprint(json_ops.to_string(obj), "yellow", end="")
    elif isinstance(obj, str):
        cprint(f'"{json_ops.to_string(obj)}"', "green", end="")
    elif isinstance(obj, list) and not obj:
        cprint("[]", end="")
    elif isinstance(obj, list):
        print("[")
        level += 1
        for i, v in enumerate(obj):
            if i > 0:
                cprint(",")
            print(" " * level * indent, end="")
            json_print(v, indent, level)
        level -= 1
        print()
        print(" " * level * indent, end="")
        cprint("]", end="")
    elif isinstance(obj, dict) and not obj:
        cprint("{}", end="")
    elif isinstance(obj, dict):
        print("{")
        level += 1
        for i, (k, v) in enumerate(obj.items()):
            if i > 0:
                cprint(",")
            print(" " * level * indent, end="")
            cprint(f'"{k}": ', "blue", end="")
            json_print(v, indent, level)
        level -= 1
        print()
        print(" " * level * indent, end="")
        cprint("}", end="")


if __name__ == "__main__":
    main()
