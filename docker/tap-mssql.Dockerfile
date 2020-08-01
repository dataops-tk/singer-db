# docker build -f tap-mssql.Dockerfile -t dataopstk/tapdance:tap-mssql .

FROM dataopstk/tapdance:tap-mssql-raw as tap


FROM python:3.7

# #anything other than false will trigger a pre-release build
# ARG prerelease=false

ENV PLUGIN_NAME=tap-mssql

RUN apt-get update && apt-get install -y default-jre
RUN apt-get update && apt-get install -y leiningen

COPY --from=tap /home/tap-mssql /venv/tap-mssql

WORKDIR /venv/tap-mssql

RUN pip install boto3 s3fs
ENV PATH "/venv/tap-mssql/bin:${PATH}"

RUN tap-mssql

ENTRYPOINT [ "tap-mssql" ]
