#!/usr/bin/env bash
set -euo pipefail

echo "[@] -- Creating folders..."
mkdir data
mkdir logs
mkdir ssl

echo "[@] -- Downloading the database dump file..."
curl --output data/neo4j.dump 'https://zenodo.org/records/10911980/files/BioPropaPhenKG.dump?download=1'

echo "[@] -- Importing the database..."
docker compose run --rm neo4j-load

echo "[@] -- Convert database to latest version..."
docker compose run --rm neo4j-migrate
