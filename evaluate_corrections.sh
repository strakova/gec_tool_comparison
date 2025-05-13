#!/bin/sh
#
# Copyright 2024 Institute of Formal and Applied Linguistics, Faculty of
# Mathematics and Physics, Charles University, Czech Republic.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

GOLD="GECCC_test_selection"
CORRECTIONS="GECCC_corrections"
EVALS="GECCC_evals"
TMP="/tmp"

if [ -d $EVALS ]; then
  echo "Removing previously existing directory $EVALS"
  rm -r $EVALS
fi

echo "Making directory $EVALS"
mkdir -p $EVALS

echo "Evaluating:"
for system in `ls $CORRECTIONS`; do

  # Eval files for overall evaluation
  all_tokenized=$EVALS/All-$system.txt
  >$all_tokenized

  all_m2=$EVALS/All-$system.m2
  >$all_m2

  # Domain evaluation
  for domain in "Natives_Formal" "Natives_Web_Informal" "Romani" "Second_Learners"; do
    m2=$GOLD/$domain.m2

    system_corrections=$TMP/$system.txt
    cat $CORRECTIONS/$system/$domain/*.txt > $system_corrections

    eval_file=$EVALS/$domain-$system.eval

    echo "Evaluating system $system on domain $domain, printing results to eval file $eval_file"

    # Tokenize
    case $system in
      # When predictions are already tokenized, skip the tokenization step.
      Korektor|Naplava*|Ours)
        tokenized=$system_corrections;;
      *)
        tokenized=/tmp/$domain-$system.tokenized
        cat $system_corrections | venv/bin/python ./udpipe_tokenizer.py > $tokenized;;
    esac

    # Evaluate with m2scorer
    venv/bin/m2scorer $tokenized $m2 > $eval_file

    # Aggregate for overall evaluation
    cat $m2 >> $all_m2
    cat $tokenized >> $all_tokenized
  done

  # Overall evaluation
  all_eval_file=$EVALS/All-$system.eval
  echo "$all_tokenized -> $all_eval_file"
  venv/bin/m2scorer $all_tokenized $all_m2 > $all_eval_file

  rm $all_tokenized
  rm $all_m2
done
