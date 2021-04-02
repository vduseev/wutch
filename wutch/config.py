import ilexconf
import argparse

from loguru import logger


class Config(ilexconf.Config):
    defaults = ilexconf.Config(
        # Directories to watch for the file changes.
        dirs=["."],
        # Directories to ignore during watching for file changes.
        ignore_dirs=["_build", "build"],
        # File patterns to watch for changes.
        patterns=["*"],
        # File patterns to ignore.
        ignore_patterns=[],
        # Shell command to run each time files in the watched directories
        # get changed.
        command="sphinx-build",
        # In which directory HTML files built by shell command will appear.
        build="_build",
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
        wait=3,
        # Do not open browser after launch of wutch.
        no_browser=False,
        # Do not start a webserver.
        no_server=False,
    )

    def __init__(self):

        super().__init__(
            self.defaults,
            ilexconf.from_json("wutch.cfg", ignore_errors=False),
            ilexconf.from_env(prefix="WUTCH_"),
            ilexconf.from_argparse(self._parse_arguments()),
        )

        logger.debug(f"{self}")

    @staticmethod
    def _parse_arguments():

        parser = argparse.ArgumentParser(
            prog="wutch",
            description=(
                "Watches specified directories for the changes in files "
                "mathing given patterns and runs a shell command each time. "
                "Opens/refreshes the webpage after the command is done."
            ),
        )
        parser.add_argument(
            "-c",
            "--command",
            help=f"Shell command executed in response to file changes. Defaults to: {Config.defaults.command}.",
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
            help=f"Ignores file changes in these patterns (separated by ' '). Defaults to: {Config.defaults.ignore_patterns}.",
            nargs="*",
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
            "-D",
            "--ignore-dirs",
            help=f"Ignore file changes in these directories (separated by ' '). Defaults to: {Config.defaults.ignore_dirs}.",
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

        return parser.parse_args()
