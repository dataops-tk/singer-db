ARG source_image=python:3.7
FROM ${source_image}

# #anything other than false will trigger a pre-release build
# ARG prerelease=false

RUN pip install pipx
RUN pip install \
    boto3 \
    s3fs

ARG TAP_NAME=tap-pardot
ARG TAP_SOURCE=${TAP_NAME}
ARG TARGET_NAME=target-s3-csv
ARG TARGET_SOURCE=${TARGET_NAME}

ENV TAP_NAME=${TAP_NAME} \
    TAP_SOURCE=${TAP_SOURCE} \
    TARGET_NAME=${TARGET_NAME} \
    TARGET_SOURCE=${TARGET_SOURCE} \
    tap_shortname=${TAP_NAME/#"tap-"} \
    target_shortname=${TARGET_NAME/#"target-"}

RUN pipx install ${TAP_SOURCE}
RUN pipx install ${TARGET_SOURCE}
RUN pipx list

# Check that both plugins are running and on the PATH
RUN if [ ! -e $(which ${TAP_NAME}) ]; then \
    echo "ERROR: count not find ${TAP_NAME} on path" && \
    exit 1; \
    fi;
RUN if [ ! -e $(which ${TARGET_NAME}) ]; then \
    echo "ERROR: count not find ${TARGET_NAME} on path" && \
    exit 1; \
    fi;

ENTRYPOINT []
CMD [ "${TAP_NAME}} --config=.secrets/${tap_shortname}-config.json | ${TAP_NAME} --config=.secrets/${target_shortname}-config.json" ]
