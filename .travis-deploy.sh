#!/bin/bash

echo -n "Trying to deploy to Github pages... "
if [[ "${TOXENV#*doc_travis}" != "$TOXENV" ]]; then
    echo "preparing"
    tox -e doc_travis_deploy
else
    echo "skipped"
    echo "HINT: Only used when 'doc_travis' target is active."
fi
