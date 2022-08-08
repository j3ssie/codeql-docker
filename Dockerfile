FROM j3ssie/codeql-base:latest
ENV CODEQL_HOME /root/codeql-home
ENV PATH="$PATH:${CODEQL_HOME}/codeql:/root/go/bin:/root/.go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
COPY containers /root/containers
COPY scripts /root/scripts

WORKDIR /root/
ENTRYPOINT ["/root/scripts/analyze.py"]
