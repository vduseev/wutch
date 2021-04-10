import argparse

import ilexconf
from loguru import logger

from .version import __version__


class Config(ilexconf.Config):
    defaults = ilexconf.Config(
        # Directories to watch for the file changes.
        dirs=["."],
        # File patterns to watch for changes.
        patterns=["*"],
        # File patterns to ignore.
        ignore_patterns=["_build/", "build/"],
        # Ignore changes of directories themselves
        ignore_directories=False,
        # Shell command to run each time files in the watched directories
        # get changed.
        command="sphinx-build",
        # Path to the wutch config file
        config="wutch.cfg",
        # In which directory HTML files built by shell command will appear.
        build="_build/html",
        # File patterns which should be injected with page refreshing
        # javascript.
        inject_patterns=["*.htm*"],
        # Path to file to be opened by webbrowser relative to build.
        index="index.html",
        # Which host and port to bind the internal HTTP server to.
        host="localhost",
        port=5010,
        # Cooldown period after which the command does not run again and ignores events
        # that trigger it.
        wait=1,
        # Do not open browser after launch of wutch.
        no_browser=False,
        # Do not start a webserver.
        no_server=False,
        # Log verbosity
        verbose=0,
        # Log levels
        verbosity={
            0: "ERROR",
            1: "WARNING",
            2: "INFO",
            3: "DEBUG",
        }
    )

    def __init__(self):

        super().__init__(
            self.defaults,
            ilexconf.from_json(Config.defaults.config, ignore_errors=True),
            ilexconf.from_env(prefix="WUTCH_"),
            ilexconf.from_argparse(self._parse_arguments()),
        )

    @staticmethod
    def _parse_arguments():

        parser = argparse.ArgumentParser(
            prog="wutch",
            description=(
                f"wutch ({__version__}) watches directories for "
                "the changes in files matching given patterns and runs a "
                "shell command on each change. It also opens/refreshes a "
                "webpage after the command is executed."
            ),
        )
        parser.add_argument(
            "-c",
            "--command",
            help=f"Shell command executed in response to file changes. Defaults to: {Config.defaults.command}.",
            type=str,
        )
        parser.add_argument(
            "-C",
            "--config",
            help=f"Path to the wutch config file. Defaults to: {Config.defaults.config}.",
            type=str,
        )
        parser.add_argument(
            "-d",
            "--dirs",
            help=f"Directories to watch (separated by ' '). Defaults to: {Config.defaults.dirs}.",
            nargs="*",
            type=str,
        )
        parser.add_argument(
            "-p",
            "--patterns",
            help=f"Matches paths with these patterns (separated by ' '). Defaults to: {Config.defaults.patterns}.",
            nargs="*",
            type=str,
        )
        parser.add_argument(
            "-P",
            "--ignore-patterns",
            help=f"Ignores changes in files that match these patterns (separated by ' '). Defaults to: {Config.defaults.ignore_patterns}.",
            nargs="*",
            type=str,
        )
        parser.add_argument(
            "-w",
            "--wait",
            help=f"Wait N seconds after the command is finished before refreshing the web page. Defaults to: {Config.defaults.wait}.",
            type=int,
        )
        parser.add_argument(
            "-b",
            "--build",
            help=f"Build directory containing files to render in the browser. Defaults to: {Config.defaults.build}.",
            type=str,
        )
        parser.add_argument(
            "-I",
            "--inject-patterns",
            help=f"Patterns of files to inject with JS code that refreshes them on rebuild (separated by ' '). Defaults to: {Config.defaults.inject_patterns}.",
            nargs="*",
            type=str,
        )
        parser.add_argument(
            "-i",
            "--index",
            help=f"File that will be opened in the browser with the start of the watcher. Defaults to: {Config.defaults.index}.",
            type=str,
        )
        parser.add_argument(
            "--host",
            help=f"Host to bind internal HTTP server to. Defaults to: {Config.defaults.host}.",
            type=str,
        )
        parser.add_argument(
            "--port",
            help=f"TCP port to bind internal HTTP server to. Defaults to: {Config.defaults.port}.",
            type=int,
        )
        parser.add_argument(
            "-B",
            "--no-browser",
            help=f"Do not open browser at wutch launch. Defaults to: {Config.defaults.no_browser}.",
            action="store_true"
        )
        parser.add_argument(
            "-S",
            "--no-server",
            help=f"Do not start the webserver, just launch the shell command. Defaults to: {Config.defaults.no_server}.",
            action="store_true"
        )
        parser.add_argument(
            "-v",
            "--verbose",
            help=f"Log verbosity. Has four levels: error, wargning, info, and debug. Can be stacked: -v (for warning) or -vvv (for debug).",
            action="count",
        )
        parser.add_argument(
            "-V",
            "--version",
            help="Display version of the wutch.",
            action="version",
            version=f"{__version__}",
        )

        return parser.parse_args()
