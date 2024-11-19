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

echo "Evaluating:"
for domain in "Natives_Formal" "Natives_Web_Informal" "Romani" "Second_Learners"; do
  m2=$GOLD/$domain.m2

  for system in `ls $CORRECTIONS`; do
    eval_file=$CORRECTIONS/$system/$domain-$system.eval
    system_corrections=$CORRECTIONS/$system/$domain-$system.txt
    echo "$system_corrections -> $eval_file"

    if [ ! -f $system_corrections ]; then continue; fi

    venv/bin/m2scorer $system_corrections $m2 > $eval_file
  done
done
