FROM python:3.6

RUN pip install civis-jupyter-notebook && \
    civis-jupyter-notebooks-install

# Add Tini
ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

ENV DEFAULT_KERNEL python3
EXPOSE 8888
WORKDIR /root/work
ENTRYPOINT ["/tini", "--"]
CMD ["civis-jupyter-notebooks-start"]
