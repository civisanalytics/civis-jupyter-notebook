civis-jupyter-notebook
======================

.. image:: https://travis-ci.org/civisanalytics/civis-jupyter-notebook.svg?branch=master
    :target: https://travis-ci.org/civisanalytics/civis-jupyter-notebook

A tool to enable any Docker image to be used with Civis Platform Jupyter notebooks.

Usage
-----

In your ``Dockerfile``, put the following code at the end::

    ENV SHELL=/bin/bash \
        DEFAULT_KERNEL=<your kernel>

    RUN pip install civis-jupyter-notebook && \
        civis-jupyter-notebooks-install

    EXPOSE 8888
    WORKDIR /root/work
    CMD ["civis-jupyter-notebooks-start", "--allow-root"]

Here you need to replace ``<your kernel>`` with the name of your kernel (e.g.,
one of ``python2``, ``python3``, or ``ir``). Note that your Dockerfile must use
``root`` as the default user.

Integration Testing with Platform
---------------------------------

If you would like to test our image's integration with platform locally follow the steps below:

1. Create a notebook in your platform account and grab the id of the notebook
2. Create an environment file called ``my.env`` and add the following to it::

    PLATFORM_OBJECT_ID=<notebook_id>
    CIVIS_API_KEY=<YOUR API KEY>

3. Build your image locally: ``docker build -t test .``
4. Run the container: ``docker run --rm -p 8888:8888 --env-file my.env test``
5. Access the notebook at the ip of your Docker host with port 8888 (e.g., ``http://localhost:8888/notebooks/notebook.ipynb``)

Contributing
------------

See ``CONTIBUTING.md`` for information about contributing to this project.

License
-------

BSD-3

See ``LICENSE.md`` for details.
