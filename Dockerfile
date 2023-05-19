# Base image with Python and Pipenv installed
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/

# Install project dependencies with Pipenv
RUN pip install pipenv && pipenv install

# Copy the Yaml file to the container
COPY topics.yml /app/

# Copy the Python file to the container
COPY index.py /app/

# Copy the .env file to the container
COPY .env /app/

# Run the Python file with Pipenv
CMD pipenv run python index.py