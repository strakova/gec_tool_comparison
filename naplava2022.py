#!/usr/bin/env python3
# coding=utf-8
#
# Copyright 2024 Institute of Formal and Applied Linguistics, Faculty of
# Mathematics and Physics, Charles University, Czech Republic.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Read selected test predictions by Náplava et al. (2022).
"""


import os
import shutil
import sys


DOMAINS = ["Natives_Formal", "Natives_Web_Informal", "Romani", "Second_Learners"]


if __name__ == "__main__":
    import argparse

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--geccc_test_selection", default="GECCC_test_selection", type=str, help="Path to the GECCC test selection directory.")
    parser.add_argument("--sentences_test_indices", default="sentences_test_indices.txt", type=str, help="Selected sentences indices into the GECCC test set.""")
    parser.add_argument("--naplava", default="Naplava2022", type=str, help="Directory with predictions by Naplava et al. (2022) on the GECCC test data.")
    parser.add_argument("--output_dir", default="GECCC_corrections", type=str, help="Output dir for selected sentences corrections.")
    args=parser.parse_args()

    # Read selected sentences indices into the GECCC test set
    sentence2test = dict()
    with open(args.sentences_test_indices, "r", encoding="utf-8") as fr:
        for line in fr:
            index, sentence = line.strip().split("\t")
            sentence2test[sentence] = int(index)

    for filename in os.listdir(args.naplava):
        system = "Naplava2022_{}".format(filename[:-4])
        print("Getting predictions for system {}".format(system), file=sys.stderr)

        # Read predictions by Naplava et al. (2022)
        predictions = []
        with open(os.path.join(args.naplava, filename), "r", encoding="utf-8") as fr:
            predictions = [line.strip() for line in fr]

            # Read sentences in each domain and their corresponding predictions
            for domain in DOMAINS:
                sentences = []
                for filename in sorted(os.listdir(os.path.join(args.geccc_test_selection, domain))):
                    with open(os.path.join(args.geccc_test_selection, domain, filename), "r", encoding="utf-8") as fr:
                        sentences.extend([line.strip() for line in fr])

                output_domain_dir = os.path.join(args.output_dir, system, domain)
                if os.path.exists(output_domain_dir) and os.path.isdir(output_domain_dir):
                    print("Removing existing dir \"{}\"".format(output_domain_dir), file=sys.stderr)
                    shutil.rmtree(output_domain_dir)
                print("Making dir \"{}\"".format(output_domain_dir), file=sys.stderr)
                os.makedirs(output_domain_dir, exist_ok=True)

                with open(os.path.join(output_domain_dir, "{}-{}.txt".format(domain, system)), "w", encoding="utf-8") as fw:
                    for sentence in sentences:
                        print(predictions[sentence2test[sentence]], file=fw)
