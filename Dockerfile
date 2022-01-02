FROM python:3.7
LABEL maintainer "Asad Iqbal Github -- <https://github.com/asadiqbal08>"

# Add package files, install updated node and pip
WORKDIR /tmp

# Install packages and add repo needed for postgres 9.6
COPY apt.txt /tmp/apt.txt
RUN apt-get update
RUN apt-get install -y $(grep -vE "^\s*#" apt.txt  | tr "\n" " ")

RUN apt-get update && apt-get install libpq-dev postgresql-client -y


# Add, and run as, non-root user.
RUN mkdir /src
RUN adduser --disabled-password --gecos "" asadiqbal08
RUN mkdir /var/media && chown -R asadiqbal08:asadiqbal08 /var/media

# Install project packages
COPY requirements.txt /tmp/requirements.txt
COPY test_requirements.txt /tmp/test_requirements.txt
RUN pip install -r requirements.txt -r test_requirements.txt

# Add project
COPY . /src
WORKDIR /src
RUN chown -R asadiqbal08:asadiqbal08 /src

RUN apt-get clean && apt-get purge
USER asadiqbal08

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# # Set pip cache folder, as it is breaking pip when it is on a shared volume
# ENV XDG_CACHE_HOME /tmp/.cache

# EXPOSE 8000
# ENV PORT 8000
