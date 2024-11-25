#!/bin/sh
#
# Copyright 2024 Institute of Formal and Applied Linguistics, Faculty of
# Mathematics and Physics, Charles University, Czech Republic.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

set -e

for f in GECCC_corrections/GoogleDocs/*/*.txt GECCC_corrections/Opravidlo/*/*.txt; do
  echo "Postprocessing $f"
  sed -i "s/\r//g" $f   # carriage returns
  sed -i -e '$a\' $f
  sed -i '1s/^\xEF\xBB\xBF//' $f        # BOM
  sed -i 's/\xC2\xA0/ /g' $f    # unbreakable spaces
done
