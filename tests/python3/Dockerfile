FROM python:3.6

ENV SHELL=/bin/bash \
    DEFAULT_KERNEL=python3

RUN mkdir -p /root/civis-jupyter-notebooks
COPY ./ /root/civis-jupyter-notebooks/

RUN pip install /root/civis-jupyter-notebooks && \
    civis-jupyter-notebooks-install

# put a requirements.txt file in the right spot to test pip installs
RUN echo "funny==0.1" > /root/work/requirements.txt

EXPOSE 8888
WORKDIR /root/work
CMD ["civis-jupyter-notebooks-start", "--allow-root"]
