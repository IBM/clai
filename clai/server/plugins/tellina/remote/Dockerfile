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
#ADD manage.py /app/manage.py
ADD bashlint /app/bashlint
ADD encoder_decoder /app/encoder_decoder
ADD eval /app/eval
ADD nlp_tools /app/nlp_tools
ADD db.sqlite3 /app/db.sqlite3
ADD hello.py /app/hello.py
ADD manifest.yml /app/manifest.yml
ADD Procfile /app/Procfile
ADD setup.py /app/setup.py
ADD translate_cmd.py /app/translate_cmd.py
ADD vcap-local.template.json /app/vcap-local.template.json
ADD run-dev /app/run-dev
ADD runtime.txt /app/runtime.txt

# Invoke running server
CMD python3 hello.py
