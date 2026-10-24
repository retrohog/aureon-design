#!/bin/bash
# Double-click this after you change the mock-up.
# It republishes https://retrohog.github.io/aureon-design/ with the newest
# "Aureon Pulse.html" from your Desktop.

cd "$(dirname "$0")" || exit 1
clear

echo "Aureon design link — publishing"
echo "================================"
echo

PY=/usr/bin/python3
if [ ! -x "$PY" ]; then PY=python3; fi

"$PY" publish.py "$@"
STATUS=$?

echo
if [ $STATUS -eq 0 ]; then
  echo "Done. You can close this window."
else
  echo "Something went wrong (see the message above)."
fi
echo
echo "Press return to close."
read -r _
