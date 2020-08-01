ARG source_image=python:3.7
FROM ${source_image}

# #anything other than false will trigger a pre-release build
# ARG prerelease=false

RUN pip install pipx
RUN pip install \
    boto3 \
    s3fs

ARG PLUGIN_NAME=tap-pardot
ARG PLUGIN_SOURCE=${PLUGIN_NAME}

RUN pipx install ${PLUGIN_SOURCE} \
    pipx list

ENV PLUGIN_NAME=${PLUGIN_NAME} \
    PLUGIN_SOURCE=${PLUGIN_SOURCE}

RUN ln -s /venv/${PLUGIN_NAME}/bin/${PLUGIN_NAME} /venv/${PLUGIN_NAME}/${PLUGIN_NAME}
ENV PATH="/venv/${PLUGIN_NAME}:${PATH}"

# Check that the plugin is running and on the PATH
RUN test -e $(which ${PLUGIN_NAME}) || exit 1
# RUN ${PLUGIN_NAME} --help

RUN echo "#!bin/bash\n\n${PLUGIN_NAME} \$@\n" > bootstrap.sh
RUN chmod 777 bootstrap.sh

ENTRYPOINT [ "./bootstrap.sh" ]
