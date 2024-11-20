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
# Our evaluation on the entire GECCC test set should reproduce similar number.
#
# Ours:
#
# Precision   : 0.5120
# Recall      : 0.2472
# F_0.5       : 0.4217 (!)
#
# This is not exactly it, although close, so let's check why we did not exactly
# reproduce the results:
#
# 1. CORRECT: We are using the same tokenizer:
#    udpipe_tokenizer/czech-pdt-ud-2.5-191206.udpipe, with the official
#    udpipe_tokenizer.py script.
#
# 2. TODO: diff sentences in M2 vs. our tokenized Korektor outputs.

set -e

echo "Correcting GECCC test data with Korektor:"
input=GECCC/data/test/sentence.input
output=/tmp/sentence.output
echo "$input -> $output"
curl -F "data=@$input" http://lindat.mff.cuni.cz/services/korektor/api/correct | PYTHONIOENCODING=utf-8 python3 -c "import sys,json; sys.stdout.write(json.load(sys.stdin)['result'])" > $output

output_tokenized=${output}.tokenized
cat $output | venv/bin/python ./udpipe_tokenizer.py > $output_tokenized

venv/bin/m2scorer $output_tokenized GECCC/data/test/sentence.m2
