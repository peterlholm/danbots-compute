#!/bin/bash

# udate from git

OUTPUT=/tmp/gitout

git pull >$OUTPUT

mail -s "Git Compute update" peter@l-holm.dk <$OUTPUT

rm $OUTPUT

