#!/bin/bash

set +e

(
    set -e
    cp $1 .
    docker build -t img .
    docker run img echo "BUILDS OK"
    docker run img python -c "import civis"
    docker run img ipython -c "%load_ext civis_jupyter_ext"
    docker run img ipython -c "import funny; print(funny.printstr())"
)

SUCCESS=$?
if [ $SUCCESS -ne 0 ]; then
    exit 1;
fi
