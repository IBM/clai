# Start with Tensorflow 2.0.0rc0
FROM tensorflow/tensorflow:2.0.0rc0-py3-jupyter

# Creating app directory
WORKDIR /app

# Add requirements file
ADD requirements.txt /app

# Upgrade pip
RUN pip install --upgrade pip

# Install requirements
RUN pip install -r requirements.txt

# Copying relevant files and dirs from tellina local install
ADD tellina /app/tellina
ADD tellina_learning_module /app/tellina_learning_module
ADD website /app/website
ADD Makefile /app/Makefile
ADD manage.py /app/manage.py

# Clean to remove old DB
RUN make clean

# Make database
RUN make db

# Invoke running server
CMD make run