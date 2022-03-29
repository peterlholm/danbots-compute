#!/bin/bash

HOME=/var/www/compute
ENV=/var/www/compute/env
# create env

python3 -m venv $ENV

. $ENV/bin/activate

cd $HOME
pip install -r requirements.txt

