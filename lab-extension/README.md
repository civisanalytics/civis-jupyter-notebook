# civis_jupyter_notebook_extensions

[![Github Actions Status](/workflows/Build/badge.svg)](/actions/workflows/build.yml)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh//main?urlpath=lab)


Extensions for use in Jupyter Notebook in Civis Platform.
## Setting up your local development environment
Development of Civis Jupyter Notebook extensions can be done using a conda environment and the Jupyter labextension tools. The steps below are based on [JupyterLab's Extension Tutorial](https://jupyterlab.readthedocs.io/en/stable/extension/extension_tutorial.html). [JupyterLab Extensions](https://github.com/jupyterlab/extension-examples) by Examples is also a helpful resource for getting started building funcitonality into JupyterLab and Jupyter Notebook. 

- Ensure you're running Python 3.12. The instructions below are applicable to Linux and MacOS users.
- Install conda or miniconda for use as a virtual environment
- Create your conda environment with JupyterLab, NodeJS. git, copier, and jinja2-time may be necessary if starting from scratch. 
    ```
    conda create -n jupyterlab-ext --override-channels --strict-channel-priority -c conda-forge -c nodefaults jupyterlab=4 nodejs=20 git copier=9 jinja2-time
    ```
- Activate your conda environment: 
    ```
    conda activate jupyterlab-ext
    ```
    - [See JupyterLab's Initialize the project from the template] (https://jupyterlab.readthedocs.io/en/stable/extension/extension_tutorial.html#initialize-the-project-from-the-template) if starting from scratch. 
- From the project root folder, install dependencies: 
    ```
    pip install -ve .
    ```
- Run the labextension command below to create a symbolic link from JupyterLab to extension source directory to make changes automatically available in JupyterLab. 
    ``` 
    jupyter labextension develop --overwrite .
    ```
- To start JupyterLab with the extension run the command below. The JupyterLab server should start at [http://localhost:8888](http://localhost:8888).
    ```
    jupyter lab
    ```
    or 
    ```
    jupyter-lab --LabApp.default_url='/doc'
    ```
- After making changes, you can run ```jlpm run build``` to rebuild the extension and see the new changes in the running JupyterLab.
    ```
    jlpm run build
    ```
    - The command below will monitor index.ts and other files for changes, and run the build command automatically. Note changes made to the ```plugin.json``` and ```package.json```files will not be picked up with the watch command.
    ```
    jlpm run watch
    ```
- Dependencies can be added with ```jlpm add @lumino/widgets``` where _@lumino/widgets_ represents the dependency to add.

## Building the extension
You can build the extension for testing in civis-jupyter-notebook. 
- With your conda environment ```jupyterlab-ext``` running install the build package. 
```
pip install build
```
- Run the build command below. The ```-w``` flag will limit the build output to a wheel. The ```-o``` flag will detrmine the output directory for the build. 

```
python -m build -w -o ../src/civis_jupyter_notebooks/assets/extensions
```


## Requirements

- JupyterLab >= 4.0.0

## Install

To install the extension, execute:

```bash
pip install civis_jupyter_notebook_extensions
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall civis_jupyter_notebook_extensions
```

## Contributing

### Development install

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the civis_jupyter_notebook_extensions directory
# Install package in development mode
pip install -e "."
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Rebuild extension Typescript source after making changes
jlpm build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development uninstall

```bash
pip uninstall civis_jupyter_notebook_extensions
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `civis-jupyter-notebook-extensions` within that folder.

### Testing the extension

#### Frontend tests

This extension is using [Jest](https://jestjs.io/) for JavaScript code testing.

To execute them, execute:

```sh
jlpm
jlpm test
```

#### Integration tests

This extension uses [Playwright](https://playwright.dev/docs/intro) for the integration tests (aka user level tests).
More precisely, the JupyterLab helper [Galata](https://github.com/jupyterlab/jupyterlab/tree/master/galata) is used to handle testing the extension in JupyterLab.

More information are provided within the [ui-tests](./ui-tests/README.md) README.

### Packaging the extension

See [RELEASE](RELEASE.md)
