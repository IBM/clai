# Start with a python 3 image
FROM python:3

# Document who is responsible for this image
MAINTAINER Bashbot "bashbot@us.ibm.com"

# Expose any ports the app is expecting in the environment
EXPOSE 8081

# Set up a working folder and install the pre-reqs
WORKDIR /app
ADD sample-application-files/requirements.txt /app
RUN pip install -r requirements.txt

# Add the code as the last Docker layer because it changes the most
ADD sample-application-files/run.py /app

# Run the service
CMD [ "python", "run.py" ]
