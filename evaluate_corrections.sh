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

mkdir -p $EVALS

echo "Evaluating:"
for system in `ls $CORRECTIONS`; do
  all_system_corrections=$EVALS/All-$system.txt
  >$all_system_corrections

  all_m2=$EVALS/All-$system.m2
  >$all_m2

  for domain in "Natives_Formal" "Natives_Web_Informal" "Romani" "Second_Learners"; do
    m2=$GOLD/$domain.m2

    eval_file=$EVALS/$domain-$system.eval
    system_corrections=$CORRECTIONS/$system/$domain-$system.txt
    echo "$system_corrections -> $eval_file"

    if [ ! -f $system_corrections ]; then continue; fi

    venv/bin/m2scorer $system_corrections $m2 > $eval_file

    # Aggregate for overall evaluation
    cat $m2 >> $all_m2
    cat $system_corrections >> $all_system_corrections
  done

  # Overall evaluation
  all_eval_file=$EVALS/All-$system.eval
  echo "$all_system_corrections -> $all_eval_file"
  venv/bin/m2scorer $all_system_corrections $all_m2 > $all_eval_file

  rm $all_system_corrections
  rm $all_m2
done
