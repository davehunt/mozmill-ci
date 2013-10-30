#!/usr/bin/env bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

echo "Checking patches"
./test/check_patches.sh || exit $?

echo "Running setup"
./setup.sh

echo "Starting Jenkins"
./start.sh > jenkins.out &
sleep 60

VERSION_VIRTUALENV=1.9.1
VENV_DIR="test/venv"
# Check if environment exists, if not, create a virtualenv:
if [ -d $VENV_DIR ]
then
  echo "Using virtual environment in $VENV_DIR"
else
  echo "Creating a virtual environment (version ${VERSION_VIRTUALENV}) in ${VENV_DIR}"
  curl https://raw.github.com/pypa/virtualenv/${VERSION_VIRTUALENV}/virtualenv.py | python - --no-site-packages $VENV_DIR
fi
. $VENV_DIR/bin/activate || exit $?

pip install selenium
python test/save_config.py

echo "Killing Jenkins"
pid=$(lsof -i:8080 -t); kill -TERM $pid || kill -KILL $pid

git --no-pager diff --exit-code
