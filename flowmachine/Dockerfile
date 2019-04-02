# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

FROM python:3.7

WORKDIR /usr/src/flowmachine
# Note: the flowkit_common/ folder must be copied manually into the flowmachine/ folder
# so that docker can pick it up here. This is a temporary workaround until flowkit_common
# can be installed from PyPI.
COPY ./flowkit_common /usr/src/flowkit_common/
COPY Pipfile* /usr/src/flowmachine/
RUN pip install pipenv && pipenv install --deploy
COPY . /usr/src/flowmachine/
RUN pipenv install --skip-lock .
CMD ["pipenv", "run", "flowmachine"]
ENV LOG_LEVEL=error
ENV FLOWDB_PORT=5432
ENV FLOWDB_HOST=flowdb
ENV FLOWDB_USER=analyst
ENV DEBUG=False
