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

   $ wutch

   2021-04-02 23:47:06.216 | DEBUG    | wutch.config:__init__:48 - Config{'dirs': ['docs'], 'ignore_dirs': [], 'patterns': ['*.rst', '*.py'], 'ignore_patterns': [], 'command': 'make -C docs rebuild', 'build': 'docs/_build/html', 'inject_patterns': ['*.html'], 'index': 'index.html', 'host': 'localhost', 'port': 5010, 'wait': 3, 'no_browser': False, 'no_server': False}
   2021-04-02 23:47:06.217 | DEBUG    | wutch.watcher:start:24 - Starting observer thread
   2021-04-02 23:47:06.219 | DEBUG    | wutch.watcher:start:26 - Observer thred started
   2021-04-02 23:47:06.220 | DEBUG    | wutch.server:start:44 - Server thread started
   2021-04-02 23:47:06.220 | DEBUG    | wutch.server:_open_browser:133 - Opening browser at: http://localhost:5010/index.html

Stop wutch by pressing Ctrl+C key sequence.

.. code-block:: bash

   ^C2021-04-02 23:47:25.283 | DEBUG    | wutch.threaded:run:28 - Stopping all threads on KeyboardInterrupt
   2021-04-02 23:47:25.283 | DEBUG    | wutch.watcher:stop:30 - Stopping observer thread
   2021-04-02 23:47:26.260 | DEBUG    | wutch.watcher:stop:33 - Observer thread stopped
   2021-04-02 23:47:26.260 | DEBUG    | wutch.server:stop:58 - Server thread stopped

Configuration
-------------

Parameters
~~~~~~~~~~

.. code-block:: bash

   -h, --help            show this help message and exit
   -c COMMAND, --command COMMAND
                           Shell command executed in response to file changes. Defaults to: sphinx-build.
   -p [PATTERNS ...], --patterns [PATTERNS ...]
                           Matches paths with these patterns (separated by ' '). Defaults to: ['*'].
   -P [IGNORE_PATTERNS ...], --ignore-patterns [IGNORE_PATTERNS ...]
                           Ignores file changes in these patterns (separated by ' '). Defaults to: [].
   -d [DIRS ...], --dirs [DIRS ...]
                           Directories to watch (separated by ' '). Defaults to: ['.'].
   -D [IGNORE_DIRS ...], --ignore-dirs [IGNORE_DIRS ...]
                           Ignore file changes in these directories (separated by ' '). Defaults to: ['_build', 'build'].
   -w WAIT, --wait WAIT  Wait N seconds after the command is finished before refreshing the web page. Defaults to: 3.
   -b BUILD, --build BUILD
                           Build directory containing files to render in the browser. Defaults to: _build.
   -I [INJECT_PATTERNS ...], --inject-patterns [INJECT_PATTERNS ...]
                           Patterns of files to inject with JS code that refreshes them on rebuild (separated by ' '). Defaults to: ['*.htm*'].
   -i INDEX, --index INDEX
                           File that will be opened in the browser with the start of the watcher. Defaults to: index.html.
   --host HOST           Host to bind internal HTTP server to. Defaults to: localhost.
   --port PORT           TCP port to bind internal HTTP server to. Defaults to: 5010.
   -B NO_BROWSER, --no-browser NO_BROWSER
                           Do not open browser at wutch launch. Defaults to: False.
   -S NO_SERVER, --no-server NO_SERVER
                           Do not start the webserver, just launch the shell command. Defaults to: False.


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
      "ignore_dirs": [],
      "patterns": ["*.rst", "*.py"],
      "ignore_patterns": [],
      "command": "make -C docs rebuild",
      "build": "docs/_build/html",
      "inject_patterns": ["*.html"],
      "index": "index.html",
      "host": "localhost",
      "port": 5010
   }


.. _Sphinx: https://www.sphinx-doc.org/
.. _ilexconf: https://github.com/ilexconf/ilexconf