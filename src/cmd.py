import inspect
import shlex
from dataclasses import dataclass
from functools import wraps

from typing import Callable, TYPE_CHECKING


from .abc import Messageable, User
if TYPE_CHECKING:
    from .bot import Bot


@dataclass
class Context(Messageable):
    bot: "Bot"
    backend: str
    author: "User"
    channel: Messageable

    def send(self, content: str, *args, **kwargs):
        self.channel.send(content, *args, **kwargs)


# Modified from https://github.com/div72/grcbountybot/blob/c1b78f8848bf80132ee6f6f0c4fc025870751f9d/grcbountybot/shell.py.


def on_prefix(prefix: str) -> Callable[[str], list[str]]:
    def parser(msg: str) -> list[str]:
        if not msg.startswith(prefix):
            return []

        return shlex.split(msg[len(prefix):])

    return parser


class CommandParser:
    commands = {"default": (lambda *args, **kwargs: None)}

    def __init__(self, parse_fn: Callable[[str], list[str]]):
        self.parse_fn = parse_fn

    def command(self, name: str = None):
        def _command(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            self.commands[name or func.__qualname__.split('.')[-1]] = func
            return wrapper

        return _command

    @staticmethod
    def _get_arg_types(func) -> list:
        arg_types = []
        sig = inspect.signature(func)
        for param in sig.parameters.values():
            if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):
                if (_type := param.annotation) == inspect._empty:
                    arg_types.append(str)
                else:
                    arg_types.append(_type)
        return arg_types

    def parse_command(self, ctx: Context, cmd: str):
        args = self.parse_fn(cmd)
        if args:
            func = self.commands.get(args[0], self.commands["default"])
            args = args[1:]
            if arg_types := self._get_arg_types(func):
                _args = []
                for arg, _type in zip(args, arg_types):
                    _args.append(_type(arg))
                func(ctx, *_args)
            else:
                func(ctx, *args)
