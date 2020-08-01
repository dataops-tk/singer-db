ARG source_image=python:3.7
FROM ${source_image}

# #anything other than false will trigger a pre-release build
# ARG prerelease=false

RUN pip install pipx
RUN pip install \
    boto3 \
    s3fs

ARG PIP_SOURCES="tap-salesforce target-csv"
ARG PLUGIN_NAMES="tap-salesforce target-csv"
ENV PIP_SOURCES="${PIP_SOURCES}" \
    PLUGIN_NAMES="${PLUGIN_NAMES}"

# Install each plugin to isolated environments via pipx
RUN pipx ensurepath && \
    for plugin in ${PIP_SOURCES}; do \
        pipx install ${plugin}; \
    done
RUN pipx list

# Check that each plugin is running and on the PATH
RUN for plugin in ${PLUGIN_NAMES}; do \
        if [ -e $(which ${plugin}) ]; then \
            echo "${plugin}?"; \
            echo `which ${plugin}`; \
        else \
            echo "ERROR: count not find ${plugin} on path" && \
            exit 1; \
        fi; \
    done

RUN echo "#!bin/bash\n\n${PLUGIN_NAME} \$@\n" > bootstrap.sh
RUN chmod 777 bootstrap.sh

ENTRYPOINT [ "./bootstrap.sh" ]
