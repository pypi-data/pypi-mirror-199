# Prerequisites

Python. You can install python using the following command: $ pip install python3

# Before contributing

1. git clone the project into your local

2. Run the following commands to install dependencies:

make develop

make build

make install

3. Before opening a Pull Request, run the following commands:

make lint

make test

make coverage (if coverage is below 50%, add tests in pynixconfig/tests/test_all.py)
