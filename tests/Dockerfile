FROM python:3.12.3-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && apt-get purge -y --auto-remove \
 && rm -rf /var/lib/apt/lists/*

# Add Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

ENV DEFAULT_KERNEL python3
EXPOSE 8888
WORKDIR /root/work
ENTRYPOINT ["/tini", "--"]
CMD ["civis-jupyter-notebooks-start"]

# put a requirements.txt file in the right spot to test pip installs
RUN echo "funny==0.1" > /root/work/requirements.txt

COPY ./ /root/civis-jupyter-notebooks/
RUN pip install /root/civis-jupyter-notebooks && \
    civis-jupyter-notebooks-install
