# Example Docker Image for Civis Platform Jupyter Notebooks

## Requirements

In order to run the example, you need to have:

1. Docker installed and running. See their [documentation](https://docs.docker.com/engine/installation/).
2. Your Civis Platform API key in your environment as `${CIVIS_API_KEY}`.
3. The ID of notebook in the Civis Platform to test against. This ID is the number that appears at the end 
   of the URL for the notebook, `https://platform.civisanalytics.com/#/notebooks/<NOTEBOOK ID>`.

## Usage

To run the example:

1. Clone this repo and then change to this directory: `cd civis-jupyter-notebook/example`.
2. Build the image using [build.sh](build.sh): `./build.sh`.
3. Change `<NOTEBOOK ID>` in [run.sh](run.sh) to the ID of your notebook from step 3 above.
4. Run the Jupyter notebook server using [run.sh](run.sh): `./run.sh`.
5. Connect to the notebook. If you are running Docker locally via `docker run`, then 
   [http://localhost:8888/notebooks/notebook.ipynb](http://localhost:8888/notebooks/notebook.ipynb)
   should work. Other setups require the Docker host IP in the URL, 
   `http://<docker-host-ip>:8888notebooks/notebook.ipynb`.
