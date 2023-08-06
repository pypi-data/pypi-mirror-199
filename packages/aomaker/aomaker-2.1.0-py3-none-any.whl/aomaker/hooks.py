# --coding:utf-8--
import functools

import click

from aomaker.cli import main, OptionHandler


class HookManager:
    def __init__(self):
        self._callbacks = {}

    def register(self, func, name):
        """
        注册回调函数。
        """
        self._callbacks[name] = func

    # def unregister(self, func):
    #     """
    #     取消注册回调函数。
    #     """
    #     if func in self._callbacks:
    #         self._callbacks.remove(func)

    def run(self, ctx, custom_kwargs):
        """
        运行所有已注册的回调函数。
        """
        for param, value in custom_kwargs.items():
            if value is not None:
                self._callbacks[param](ctx)


def command(name, **out_kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cmd = main.get_command(None, 'run')
            option_handler = OptionHandler()
            option_handler.add_option(name, **out_kwargs)
            cmd.params.append(click.Option(option_handler.options.pop("name"), **option_handler.options))
            new_name = name.replace("-", "")
            _cli_hook.register(func, new_name)

        return wrapper

    return decorator


def session_hook(func):
    @functools.wraps(func)
    def wrapper():
        _session_hook.register(func)

    return wrapper


_cli_hook = HookManager()
_session_hook = HookManager()
