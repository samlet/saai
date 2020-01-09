# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:latest

# Add a custom system library (e.g. git)
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
    netcat

# Add a custom python library (e.g. jupyter)
RUN pip install --no-cache-dir pandas PyMySQL graphene-sqlalchemy cryptography

