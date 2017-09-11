FROM python:3.6

RUN pip install civis-jupyter-notebook && \
    civis-jupyter-notebooks-install

ENV DEFAULT_KERNEL=python3
EXPOSE 8888
WORKDIR /root/work
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["civis-jupyter-notebooks-start"]
