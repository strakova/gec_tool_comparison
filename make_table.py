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
Makes pretty table from evaluation results.
"""


import os
import sys


# The preferred order of domains (from the GECCC TACL paper)
DOMAINS = ["NF", "NWI", "R", "SL", "All"]

DOMAIN_SHORTCUTS = {"Natives_Formal": "NF",
                    "Natives_Web_Informal": "NWI",
                    "Romani": "R",
                    "Second_Learners": "SL",
                    "All": "All"}

if __name__ == "__main__":
    import argparse

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--evals", default="GECCC_evals/", type=str, help="Path to the system evaluations.")
    args=parser.parse_args()

    evals = dict()

    for filename in os.listdir(args.evals):
        domain, rest = filename.split("-")
        system, _ = rest.split(".")

        # Parse eval
        with open(os.path.join(args.evals, filename), "r", encoding="utf-8") as fr:
            for line in fr:
                line = line.strip()
                if line.startswith("F_0.5"):
                    Fscore = line.split(":")[1][1:]

        domain = DOMAIN_SHORTCUTS[domain]

        if system not in evals:
            evals[system] = dict()
        evals[system][domain] = float(Fscore) * 100

    print("System & {} \\\\".format(" & ".join(DOMAINS)))
    print("\\midrule")

    for system, system_evals in evals.items():
        print("{} & ".format(system), end="")
        Fscores = [system_evals[domain] for domain in DOMAINS]
        print(" & ".join(["{:.2f}".format(Fscore) for Fscore in Fscores]), end="")
        print(" \\\\")
