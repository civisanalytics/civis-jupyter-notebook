#!/bin/bash

set -e

cp $1 .
docker build -t img .
docker run img echo "BUILDS OK"
docker run img python -c "import civis"
docker run img ipython -c "%load_ext civis_jupyter_ext"
docker run img ipython -c "import funny; funny.printstr()"
