# Contributing

Contributions are welcome and greatly appreciated. Every little bit helps, and
credit is always given.

You can contribute in many ways:

## Types of Contributions

**Report Bugs**

Report bugs at [GitHub Issues](https://github.com/pawangeek/indiapins/issues).

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

**Fix Bugs**

Look through issues tagged with `bug` and `help wanted`.

**Implement Features**

Look through issues tagged with `enhancement` and `help wanted`.

**Write Documentation**

`indiapins` could always use more documentation, whether as part of the
official docs, in docstrings, or in blog posts and articles.

**Submit Feedback**

The best way to send feedback is to file an issue at
[GitHub Issues](https://github.com/pawangeek/indiapins/issues).

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember this is a volunteer-driven project.

**Get Started!**

Ready to contribute? Here's how to set up `indiapins` for local development.

1. Fork the `indiapins` repo on GitHub.
2. Clone your fork locally:
    ```
    $ git clone git@github.com:your_name_here/indiapins.git
    ```
3. Install dependencies using uv:
    ```
    $ cd indiapins/
    $ uv sync
    ```
4. Create a branch for local development:
    ```
    $ git checkout -b name-of-your-bugfix-or-feature
    ```
   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests:
    ```
    $ uv run flake8 indiapins tests
    $ uv run pytest
    ```
   To run tests across all supported Python versions:
    ```
    $ make test-all
    ```

6. Commit your changes and push your branch to GitHub:
    ```
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```
7. Submit a pull request through the GitHub website.

**Pull Request Guidelines**
## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.10, 3.11, 3.12, 3.13, 3.14 and for PyPy.

## Tips

To run a subset of tests:
```
$ uv run pytest tests/test_indiapins.py
```

## Deploying

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run:
```
$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags
```

GitHub Actions will then deploy to PyPI if tests pass.
