#!/bin/env bash

echo "Bringing up RASA server"

lsof -t -i tcp:$1 | xargs kill
rasa run --enable-api -m /Users/tathagata/clai/clai/server/plugins/gitbot/rasa/models/rasa-saved-nlu-model.tar.gz -p $1
