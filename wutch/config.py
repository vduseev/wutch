import ilexconf
import argparse

from loguru import logger


class Config(ilexconf.Config):
    defaults = ilexconf.Config(
        # Directories to watch for the file changes.
        dirs=["."],
        # Directories to ignore during watching for file changes.
        ignore_dirs=[],
        # File patterns to watch for changes.
        patterns=["*"],
        # File patterns to ignore.
        ignore_patterns=[],
        # Shell command to run each time files in the watched directories
        # get changed.
        command="sphinx-build",
        # In which directory HTML files built by shell command will appear.
        build_dirs=["."],
        # File patterns which should be injected with page refreshing
        # javascript.
        inject_patterns=["*.html"],
        # The file to be opened in the browser after program start.
        file=None,
        # Which host and port to bind the internal HTTP server to.
        host="localhost",
        port=5010,
        # In which directory to put the special page refreshing
        # javascript file.
        js_dir=".",
        # How many seconds to wait after the shell command before telling
        # the webpage to refresh.
        wait=1,
        # Which action to run in the CLI app.
        # "run" all together, "inject" to inject rendered HTML files with
        # page refreshing javascript, "watch", and "serve".
        action="run",
        actions=["run", "watch", "serve", "inject"],
        # Cooldown periods after which the command does not run again and ignores events
        # that trigger it.
        injector_cooldown=1,
        watcher_cooldown=3,
    )

    def __init__(self):

        super().__init__(
            self.defaults,
            ilexconf.from_json("wutch.cfg", ignore_errors=False),
            ilexconf.from_env(prefix="WUTCH", separator="_"),
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
            "action",
            help=f"Action to perform. Defaults to: {Config.defaults.action}.",
            nargs="?",
            type=str,
            choices=Config.defaults.actions,
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
            "--build-dirs",
            help=f"Build directories containing files to render in the browser (separated by ' '). Defaults to: {Config.defaults.build_dirs}.",
            nargs="*",
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
            "-j",
            "--js-dir",
            help=f"Directory where server pooling JS script will be placed. Defaults to: '{Config.defaults.js_dir}'.",
            type=str,
        )
        parser.add_argument(
            "-f",
            "--file",
            help=f"The HTML file provided with this flag will be opened in the browser with the start of the watcher. Defaults to: {Config.defaults.file}.",
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

        return parser.parse_args()
