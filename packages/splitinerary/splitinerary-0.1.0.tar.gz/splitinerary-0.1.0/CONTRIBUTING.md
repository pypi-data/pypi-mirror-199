# Contributing

Thank you for your interest in contributing to splitinerary!

## Prerequisites

- Python3

## Setting up a development environment

It is recommended that you:

- Fork the repository on Github
- Clone your fork to your computer
- Create a virtual environment and enter it
- Run the following commands inside the cloned repository:
  - `make develop` - This will install the Python package in development
    mode.

## Opening a PR
- Make the changes you consider necessary
- Run the tests to ensure that your changes does not break anything
- If you add new code, preferably write one or more tests for checking that your code works as expected.
- Before opening a PR, run the following commands:
  - `make lint` - This command will run the Python linter.
  - `make format` - This command will run the Python formatter.
  - `make coverage` - This command will run the Python tests and emit code coverage information.
- Commit your changes and publish the branch to your github repo.
- Open a pull-request (PR) back to the main repo on Github.