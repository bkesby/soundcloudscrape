# Version 0.2
# Use official Debian runtime as parent image
FROM debian:9.4

# Install python and dependencies
RUN apt-get update && \
	apt-get install --assume-yes --no-install-recommends \
		gcc \
		libffi-dev \
		libssl-dev \
		libxml2-dev \
		libxslt1-dev \
		python-pip \
		python-dev \
		zlib1g-dev && \
	apt-get clean && \
	rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install pip and requirements.txt
RUN pip install --upgrade pip && \
	pip install --upgrade \
		setuptools \
		wheel && \
	pip install --upgrade \
		sqlalchemy \
		psycopg2 \
		scrapy \
		facebook-sdk