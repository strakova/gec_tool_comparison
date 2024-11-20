#!/bin/sh
#
# Copyright 2024 Institute of Formal and Applied Linguistics, Faculty of
# Mathematics and Physics, Charles University, Czech Republic.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

OUTPUTS="GECCC_corrections/Korektor"
INPUTS="GECCC_test_selection"
MODEL="czech-spellchecker_2edits-130202"
TMP="/tmp"

if [ -d $OUTPUTS ]; then
  echo "Removing existing dir \"$OUTPUTS\""
  rm -r $OUTPUTS;
fi

for domain in `ls $INPUTS/`; do
  # Skip M2 files
  if [ ! -d $INPUTS/$domain ]; then continue; fi

  echo "Correcting domain $INPUTS/$domain with Korektor:"
  mkdir -p $OUTPUTS/$domain/

  for input in `ls $INPUTS/$domain/*.txt`; do
    # Tokenize input before sending to Korektor
    tokenized_input=$TMP/input_tokenized
    cat $input | venv/bin/python ./udpipe_tokenizer.py > $tokenized_input

    output="$OUTPUTS/$domain/$(basename ${input%.txt})-Korektor.txt"
    echo "$input -> $output"

    curl -F "data=@$tokenized_input" -F "input=horizontal" -F "model=$MODEL" http://lindat.mff.cuni.cz/services/korektor/api/correct | PYTHONIOENCODING=utf-8 python3 -c "import sys,json; sys.stdout.write(json.load(sys.stdin)['result'])" > $output

    rm $tokenized_input

    # Be nice
    sleep 1
  done
done
