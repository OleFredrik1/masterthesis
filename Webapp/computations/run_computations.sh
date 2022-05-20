#!/bin/sh
for f in *.py; do python "$f" & done
wait
echo "Done"