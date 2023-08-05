from collections.abc import Callable
from typing import Any, Optional, NoReturn, Protocol, Union
import argparse
import functools
import os
import pprint
import shlex
import subprocess


Cmd = list[str]
CmdKwds = Any
# NoReturn is for the exec without forking case (keyword argument `nofork`)
Process = Union[subprocess.CompletedProcess[Any], subprocess.Popen[Any], NoReturn]


class Env(Protocol):
    def cmd(self, args: Cmd, **kwds: CmdKwds) -> Process:
        ...


Wrapper = Callable[[Env], Env]


class ReadableEnvProtocol(Env, Protocol):
    def read_cmd(self, args: Cmd, **kwds: CmdKwds) -> Process:
        ...


class ReadableEnv:
    """An env that supports .read_cmd

    If you run all commands that might have side effects using .cmd, and all
    other commands using .read_cmd, then --pretend (i.e. NullWrapper) will work
    correctly but you can still read information from the env even with
    --pretend in effect (e.g. use cat to read file contents).
    """

    def __init__(self, env: Env, read_env: Env):
        self._env = env
        self._read_env = read_env

    def cmd(self, args: Cmd, **kwds: CmdKwds) -> Process:
        return self._env.cmd(args, **kwds)

    def read_cmd(self, args: Cmd, **kwds: CmdKwds) -> Process:
        return self._read_env.cmd(args, **kwds)

    def wrap(self, wrapper: Wrapper) -> "ReadableEnv":
        """Return a ReadableEnv wrapped with given wrapper.
        """
        return type(self)(wrapper(self._env), wrapper(self._read_env))


class BasicEnv:
    """An environment in which to run a program.
    """

    def cmd(self, args: Cmd, **kwds: CmdKwds) -> Process:
        """Run a program.

        Arguments, return value and exceptions are like subprocess.run, except:

        The check and capture_output arguments default to True.

        If nowait is true: fork the process, without waiting.  Arguments,
        return value and exceptions are then like subprocess.Popen

        If nocommunicate is true: fork the process and wait, but don't
        .communicate().  Arguments, return value and exceptions are then like
        subprocess.Popen

        If nofork is true: don't fork the process, just exec.  No keyword
        arguments are allowed.
        """
        if kwds.get("nofork"):
            assert len(kwds) == 0, kwds
            os.execvp(args[0], args)

        if kwds.get("nowait"):
            kwds.pop("nowait")
            return subprocess.Popen(args, **kwds)

        if kwds.get("nocommunicate"):
            kwds.pop("nocommunicate")
            process = subprocess.Popen(args, **kwds)
            rc = process.wait()
            if rc != 0:
                raise subprocess.CalledProcessError(rc, args)
            else:
                return process

        kwds.setdefault("check", True)
        kwds.setdefault("capture_output", True)
        return subprocess.run(args, **kwds)

    @classmethod
    def make_readable(cls) -> ReadableEnv:
        env = cls()
        return ReadableEnv(env, env)


class PrefixCmdEnv:
    def __init__(self, prefix_cmd: Cmd, env: Env):
        self._prefix_cmd = prefix_cmd
        self._env = env

    def cmd(self, args: Cmd, **kwds: CmdKwds) -> Process:
        return self._env.cmd(self._prefix_cmd + args, **kwds)

    @classmethod
    def make_readable(cls, prefix_cmd: Cmd, readable_env: ReadableEnv) -> ReadableEnv:
        return readable_env.wrap(functools.partial(cls, prefix_cmd))


class VerboseWrapper:
    def __init__(self, env: Env):
        self._env = env

    def cmd(self, args: Cmd, **kwds: CmdKwds) -> Process:
        input = kwds.get("input")
        if input is not None:
            print("input:")
            print(input)
        pprint.pprint(args)
        return self._env.cmd(args, **kwds)

    @classmethod
    def make_readable(cls, readable_env: ReadableEnv) -> ReadableEnv:
        return readable_env.wrap(cls)


class NullWrapper:
    def __init__(self, env: Env):
        self._env = env

    def cmd(self, args: Cmd, **kwds: CmdKwds) -> Process:
        # this runs "true" rather than just doing nothing so that this can
        # return a Process
        return self._env.cmd(["true"], **kwds)

    @classmethod
    def make_readable(cls, readable_env: ReadableEnv) -> ReadableEnv:
        return ReadableEnv(env=NullWrapper(readable_env), read_env=readable_env)


def shell_escape(args: Cmd) -> str:
    return " ".join(shlex.quote(arg) for arg in args)


def add_basic_env_arguments(add_argument: Callable[..., argparse.Action]) -> None:
    """add_argument should be argparse.add_argument"""
    add_argument("-v", "--verbose", action="store_true", help="Print commands")
    add_argument(
        "-n", "--pretend", action="store_true", help="Don't actually run commands")


def get_env_from_arguments(arguments: Any) -> Env:
    env = BasicEnv.make_readable()
    if arguments.pretend:
        env = NullWrapper.make_readable(env)
    if arguments.verbose:
        env = VerboseWrapper.make_readable(env)
    return env


def in_dir(dir_path: str) -> Cmd:
    return ["sh", "-c", 'cd "$1" && shift && exec "$@"', "inline_cd", dir_path]


def write_file_cmd(filename: str, data: str) -> Cmd:
    return ["sh", "-c", 'echo -n "$1" >"$2"', "inline_script", data, filename]


def success(env: Env, args: Cmd) -> bool:
    try:
        env.cmd(args)
    except subprocess.CalledProcessError:
        return False
    else:
        return True
