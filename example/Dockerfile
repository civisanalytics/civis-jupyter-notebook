FROM python:3.6

ENV SHELL=/bin/bash \
    DEFAULT_KERNEL=python3

RUN pip install civis-jupyter-notebook && \
    civis-jupyter-notebooks-install

EXPOSE 8888
WORKDIR /root/work
CMD ["civis-jupyter-notebooks-start", "--allow-root"]
