#!/bin/bash
docker-compose run clai bash -c "cd /zclai && python3 develop.py install --path /zclai && bash"
docker-compose rm -f