#!/bin/bash

set +e

(
    set -e
    cp $1 .
    docker build -t img .
    docker run img echo "BUILDS OK"
    docker run img python -c "import civis"
    docker run img ipython /root/civis-jupyter-notebooks/tests/test_ext.py
    # TODO - figure out how to test this without needing an API key
    # docker run img ipython -c "import funny; print(funny.printstr())"
)

exit $?
