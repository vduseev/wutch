Wutch
=====

``wutch`` watches for changes in the directories and runs a shell command for
every change. It can also open a browser a display whatever is in the build
directory, just like Live Server.

Common use case for Wutch involves writing docs with `Sphinx`_. Wutch will
watch for the changes in all ``*.rst`` files and automatically rebuild documentation.
It will also open a browser window pointing to the build directory and inject
every built webpage with a code that will auto-refresh that page after each
rebuild.

.. raw:: html

   <p>
      <a href="https://pypi.org/project/wutch/"><img alt="PyPI" src="https://img.shields.io/pypi/v/wutch?color=blue&logo=pypi"></a>
      <a href='https://wutch.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/wutch/badge/?version=latest' alt='Documentation Status' /></a>
   </p>

.. image:: https://github.com/vduseev/wutch/raw/master/docs/_static/wutch-demo.gif

Installation
------------

.. code-block:: bash

   pip install wutch

Usage
-----

Just run wutch in the directory where you want to watch for the changes.
By default, ``wutch`` will:

* Watch for every change in the current directory.
* Ignore changes in the ``_build/`` and ``build`` directories.
* Run ``sphinx-build`` shell command for every change in the files.
* Open a browser pointing to ``index.html`` in the ``_build`` directory.
* Automatically refresh that page every time you change the files
  and shell command runs.

.. code-block:: bash

   $ wutch -vvv

   2021-04-10 12:33:16.367 | DEBUG    | wutch.watcher:start:25 - Starting observer thread
   2021-04-10 12:33:16.368 | DEBUG    | wutch.watcher:on_any_event:58 - Processing event <FileModifiedEvent: event_type=modified, src_path='docs', is_directory=False>.
   rm -rf "_build"
   #@poetry run sphinx-build -M build "." "_build"
   Running Sphinx v3.5.3
   loading translations [en]... done
   making output directory... done
   building [mo]: targets for 0 po files that are out of date
   building [html]: targets for 1 source files that are out of date
   updating environment: [new config] 1 added, 0 changed, 0 removed
   reading sources... [100%] index
   looking for now-outdated files... none found
   pickling environment... done
   checking consistency... done
   preparing documents... done
   writing output... [100%] index
   generating indices... genindex done
   writing additional pages... search done
   copying static files... done
   copying extra files... done
   dumping search index in English (code: en)... done
   dumping object inventory... done
   build succeeded.

   The HTML pages are in _build/html.
   2021-04-10 12:33:17.627 | DEBUG    | wutch.watcher:on_any_event:71 - Shell command executed with result: None.
   2021-04-10 12:33:17.627 | DEBUG    | wutch.events:report:15 - New Event.ShellCommandFinished event has been reported.
   2021-04-10 12:33:17.627 | DEBUG    | wutch.watcher:start:28 - Observer thred started
   2021-04-10 12:33:17.628 | DEBUG    | wutch.server:start:44 - Server thread started
   2021-04-10 12:33:17.628 | DEBUG    | wutch.server:open_browser:137 - Opening browser at: http://localhost:5010/index.html

Stop wutch by pressing Ctrl+C key sequence.

.. code-block:: bash

   ^C2021-04-10 12:33:28.396 | DEBUG    | wutch.threaded:run:28 - Stopping all threads on KeyboardInterrupt
   2021-04-10 12:33:28.397 | DEBUG    | wutch.watcher:stop:32 - Stopping observer thread
   2021-04-10 12:33:28.560 | DEBUG    | wutch.watcher:stop:35 - Observer thread stopped
   2021-04-10 12:33:28.560 | DEBUG    | wutch.server:stop:58 - Server thread stopped

Configuration
-------------

Parameters
~~~~~~~~~~

.. code-block:: bash

   -h, --help            show this help message and exit
   -c COMMAND, --command COMMAND
                     Shell command executed in response to file changes. Defaults to: sphinx-build.
   -C CONFIG, --config CONFIG
                     Path to the wutch config file. Defaults to: wutch.cfg.
   -d [DIRS ...], --dirs [DIRS ...]
                     Directories to watch (separated by ' '). Defaults to: ['.'].
   -p [PATTERNS ...], --patterns [PATTERNS ...]
                     Matches paths with these patterns (separated by ' '). Defaults to: ['*'].
   -P [IGNORE_PATTERNS ...], --ignore-patterns [IGNORE_PATTERNS ...]
                     Ignores changes in files that match these patterns (separated by ' '). Defaults to: ['_build/', 'build/'].
   -w WAIT, --wait WAIT  Wait N seconds after the command is finished before refreshing the web page. Defaults to: 1.
   -b BUILD, --build BUILD
                     Build directory containing files to render in the browser. Defaults to: _build/html.
   -I [INJECT_PATTERNS ...], --inject-patterns [INJECT_PATTERNS ...]
                     Patterns of files to inject with JS code that refreshes them on rebuild (separated by ' '). Defaults to: ['*.htm*'].
   -i INDEX, --index INDEX
                     File that will be opened in the browser with the start of the watcher. Defaults to: index.html.
   --host HOST           Host to bind internal HTTP server to. Defaults to: localhost.
   --port PORT           TCP port to bind internal HTTP server to. Defaults to: 5010.
   -B, --no-browser      Do not open browser at wutch launch. Defaults to: False.
   -S, --no-server       Do not start the webserver, just launch the shell command. Defaults to: False.
   -v, --verbose         Log verbosity. Has four levels: error, wargning, info, and debug. Can be stacked: -v (for warning) or -vvv (for debug).
   -V, --version         Display version of the wutch.


Loading order
~~~~~~~~~~~~~

Wutch loads configuration settings in the following priority:

1. Command line arguments
2. Environment variables starting with ``WUTCH_``
3. Configuration file ``wutch.cfg``
4. Default variables

Every variable can be specified in any of the sources above, thanks to
`ilexconf`_ configuration management library.

For example, ``dirs`` variable that lists directories to watch can be
specified in several ways:

**Command line:**

.. code-block:: bash

   wutch --dirs . ../other_dir

**Environment variables starting with WUTCH_:**

.. code-block:: bash

   export WUTCH_DIRS=". ../other_dir"

**Configuration file wutch.cfg:**

.. code-block:: json

   {
      "dirs": [".", "../other_dir"]
   }

Wutch's documentation is built using ``wutch``
----------------------------------------------

Take a look at the ``wutch.cfg`` file at the root of the repository. This
serves as a somewhat common configuration for Sphinx dependent documentation.

Wutch documentation is developed using ``wutch`` and this config below.

.. code-block:: json

   {
      "dirs": ["docs"],
      "patterns": ["*.rst", "*.py"],
      "ignore_patterns": ["docs/_build/"],
      "command": "make -C docs rebuild",
      "build": "docs/_build/html",
      "inject_patterns": ["*.html"],
      "index": "index.html",
      "host": "localhost",
      "port": 5010
   }


.. _Sphinx: https://www.sphinx-doc.org/
.. _ilexconf: https://github.com/ilexconf/ilexconf