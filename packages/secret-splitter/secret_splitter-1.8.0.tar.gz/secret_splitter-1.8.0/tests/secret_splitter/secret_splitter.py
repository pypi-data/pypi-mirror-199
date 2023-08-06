"""tests for src/secret_splitter.py
"""

import src.secret_splitter.secret_splitter as package
from tests.secret_splitter.suite import run_on

if __name__ == '__main__':
    package.NAME = 'block-wise SSS'
    run_on(package, algorithm='block-wise SSS', block_size=2)
