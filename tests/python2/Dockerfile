FROM python:2.7

COPY ./requirements.txt /root/requirements.txt
RUN pip install -r /root/requirements.txt

ENV DEFAULT_KERNEL=python2
EXPOSE 8888
WORKDIR /root/work
ENTRYPOINT ["/bin/bash"]
CMD ["civis-jupyter-notebooks-start"]

# put a requirements.txt file in the right spot to test pip installs
RUN echo "funny==0.1" > /root/work/requirements.txt

COPY ./ /root/civis-jupyter-notebooks/
RUN pip install /root/civis-jupyter-notebooks && \
    civis-jupyter-notebooks-install
