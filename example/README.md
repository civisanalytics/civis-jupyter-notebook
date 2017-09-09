# Example Docker Image for Civis Platform Jupyter Notebooks

In order to run the example you need to have Docker installed and
running. See their [documentation](https://docs.docker.com/engine/installation/).

To run the example:

1. Clone this repo and then change to this directory: ``cd civis-jupyter-notebook/example``
1. Build the image using [build.sh](build.sh): ``./build.sh``
2. Run the Jupyter notebook server using [run.sh](run.sh): ``./run.sh``
3. Connect to the notebook at [http://localhost:8888/notebooks/notebook.ipynb](http://localhost:8888/notebooks/notebook.ipynb)
