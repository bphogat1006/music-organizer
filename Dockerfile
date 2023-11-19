# set base image (host OS)
FROM python:3.9

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

# expose port for flask app
ARG PORT
EXPOSE ${PORT}
ENV BINDING=0.0.0.0:${PORT}

# command to run on container start
CMD gunicorn --bind ${BINDING} --access-logfile - server:app
