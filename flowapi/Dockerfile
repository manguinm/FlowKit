# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

FROM python:3.7

WORKDIR /flowapi
COPY Pipfile* /
RUN pip install pipenv && pipenv install --deploy
COPY . /flowapi/
RUN pipenv install --skip-lock .
ENV QUART_ENV=production
CMD ["pipenv", "run", "./start.sh"]
