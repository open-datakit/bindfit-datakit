#! /usr/bin/env bash
# Build bindfit container first with containers/build.sh script
docker run -it -v ${PWD}:/usr/src/app/datapackage -e ALGORITHM=bindfit -e CONTAINER=ods/bindfit -e ARGUMENTS=default ods/bindfit
