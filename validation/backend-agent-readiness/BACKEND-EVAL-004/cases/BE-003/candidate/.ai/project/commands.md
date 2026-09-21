# Commands and boundaries
Working directory: /private/tmp/digital-factory-run002-zct1ohhz/app. Use absolute python3 launcher with preflight/run.py; it fixes PHP path, clears inherited environment and excludes host ini. Do not invoke plain composer setup/test/dev, artisan serve, queue workers, migrations, config cache or direct unwrapped PHP execution.
- python3 preflight/run.py inspect: boots inspected scaffold, outputs allowlisted config, reads empty in-memory SQLite metadata; preflight allowed.
- python3 preflight/run.py test-list: PHPUnit discovery only; preflight allowed; no test execution.
- python3 preflight/run.py routes: registered-route inspection; preflight allowed.
- python3 preflight/run.py test: local synthetic automated tests; future implementation phase only, inspect new tests/boot hooks first. No test results claimed in preflight.
- python3 preflight/run.py format-check: Pint --test, future phase only; no source formatting performed now.
- git status, git diff, git log, and local file reads: permitted within sandbox.
Dependencies already installed offline with --no-scripts --no-plugins. No network use authorized for Session A. Test target/effects must be rechecked after configuration or boot-hook changes; arbitrary command execution not granted.
