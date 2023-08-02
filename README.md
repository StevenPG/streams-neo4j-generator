# Streams Neo4j Generator

This project's purpose is provide an all-in-one scripted application
that will scan a configured list of spring-cloud-streams enabled microservices,
with a configured list of repositories and spring configuration files.

This application will use a locally installed git executable to clone
the repositories, scan them for spring-cloud-streams bindings and insert
them into a Neo4j database.

The database will then be served via docker, and a Neo4J browser
can be used to access the database and review the configuration.

This effectively generates a graph of your spring-cloud-streams
environment with some basic assumptions:

- Each repository contains a single application
- Your github repository contains the correct configuration for your streams applications
- You've configured all of your services for this app to consume, so there are no hanging destinations

You can use Neo4j tooling to manually add missing pathways and connections and export
the output for documentation purposes.

#### Currently ONLY supports YML files and basic Spring Cloud Streams Binding Configurations

## Development

Create a local Pyenv using `python -m venv .venv` and `source .venv/bin/activate` on OSX

#### Docker

    docker run --publish=7474:7474 --publish=7687:7687 neo4j
