#!/bin/sh
#
# Copyright 2024 Institute of Formal and Applied Linguistics, Faculty of
# Mathematics and Physics, Charles University, Czech Republic.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This is a sanity check test for the evaluation setting.

# The GECCC TACL paper (Náplava et al. 2022) reports F_0.5 = 45.09 for Korektor
# in Table 7:
# http://ufal.mff.cuni.cz/biblio/attachments/2022-naplava-p2208933306287912570.pdf
#
# Our evaluation on the entire GECCC test set should reproduce similar number:
#
# Precision   : 0.5513
# Recall      : 0.2631
# F_0.5       : 0.4522

set -e

TMP=/tmp
MODEL="czech-spellchecker_2edits-130202"
input=GECCC/data/test/sentence.input
input_tokenized=$TMP/sentence.tokenized
output=$TMP/sentence.output

# Tokenize
cat $input | venv/bin/python ./udpipe_tokenizer.py > $input_tokenized

# Split input file into chunks to meet Korektor processing limit
head -5000 $input_tokenized > $input_tokenized.1
tail -n +5001 $input_tokenized > $input_tokenized.2

# Correct the file chunks by calling Korektor
echo "Correcting GECCC test data with Korektor:"
for i in 1 2; do
  echo "$input_tokenized.$i -> $output.$i"
  curl -F "data=@$input_tokenized.$i" -F "model=$MODEL" -F "input=horizontal" http://lindat.mff.cuni.cz/services/korektor/api/correct | PYTHONIOENCODING=utf-8 python3 -c "import sys,json; sys.stdout.write(json.load(sys.stdin)['result'])" > $output.$i
done

# Join the chunks
cat $output.1 $output.2 > $output

# Evaluate with m2scorer
echo "Evaluating with m2scorer:"
venv/bin/m2scorer $output GECCC/data/test/sentence.m2
