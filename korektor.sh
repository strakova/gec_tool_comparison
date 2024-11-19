#!/bin/sh
#
# Copyright 2024 Institute of Formal and Applied Linguistics, Faculty of
# Mathematics and Physics, Charles University, Czech Republic.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

CORRECTIONS="GECCC_corrections/Korektor"
INPUTS="GECCC_test_selection"

mkdir -p $CORRECTIONS

echo "Correcting with Korektor:"
for input in `ls $INPUTS/*.txt`; do
  output="$CORRECTIONS/$(basename ${input%.txt})-Korektor.txt"
  echo "$input -> $output"
  curl -F "data=@$input" http://lindat.mff.cuni.cz/services/korektor/api/correct | PYTHONIOENCODING=utf-8 python3 -c "import sys,json; sys.stdout.write(json.load(sys.stdin)['result'])" > $output
done

