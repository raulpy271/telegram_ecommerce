#!/bin/bash
docker rmi telegram_ecomm:latest -f
docker-compose up --force-recreate