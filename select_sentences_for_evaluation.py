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
Gets data for GEC evaluation.
"""


import os
import sys

import pandas as pd


NATIVES_FORMAL_HEADER_SIZE=15


def read_edits(path):
    """Read edits from an M2 file.

    Arguments:
        path: path to an M2 file.
    """
    edits, lengths, edits_str = [], [], []

    with open(path, "r", encoding="utf-8") as fr:
        for line in fr:
            line = line.strip()

            if not line:
                continue

            if line.startswith("S"):
                edits.append(0)
                lengths.append(len(line.split(" ")))
                edits_str.append([])

            if line.startswith("A"):
                edits[-1] += 1
                edits_str[-1].append(line)

    edits_str = ["\n".join(row) for row in edits_str]

    return pd.DataFrame({"Edits": edits, "Lengths": lengths, "Edits_str": edits_str})


if __name__ == "__main__":
    import argparse

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--geccc", default="GECCC", type=str, help="Path to the GECCC corpus.")
    parser.add_argument("--min_sentences_per_domain", default=200, type=int, help="Minimum sentences to evaluate per domain.")
    parser.add_argument("--seed", default=42, type=str, help="Random seed.")
    parser.add_argument("--output_dir", default="GECCC_test_selection", type=str, help="Output dir to print data for testing to.")
    parser.add_argument("--max_sentences_per_doc", default=10, type=int, help="Maximum sentences to take from one document.")
    args=parser.parse_args()

    meta = pd.read_csv(os.path.join(args.geccc, "data", "meta.tsv"), delimiter="\t", encoding="utf-8")
    meta_sentences = pd.read_csv(os.path.join(args.geccc, "data", "test", "sentence.meta"), delimiter="\t", header=None, names=["Filename"], encoding="utf-8")

    edits = read_edits(os.path.join(args.geccc, "data", "test", "sentence.m2"))

    # Read lines in manually to check for hidden characters, which otherwise
    # make pandas read less sentences than we have in the file.
    with open(os.path.join(args.geccc, "data", "test", "sentence.input"), "r", encoding="utf-8") as fr:
        lines = [line.strip() for line in fr]
    sentences = pd.DataFrame(lines, columns=["Sentence"])

    assert(len(sentences) == len(meta_sentences))
    assert(len(sentences) == len(edits))
    sentences = pd.concat([sentences, meta_sentences, edits], axis=1)

    os.makedirs(args.output_dir, exist_ok=True)

    n_selected_docs, n_total_docs = 0, 0
    total_selected_sentences = []

    for domain in meta["Domain"].unique():

        docs_in_domain = meta[(meta["Filename"].isin(meta_sentences["Filename"])) & (meta["Domain"] == domain)]
        sentences_in_domain = sentences[sentences["Filename"].isin(docs_in_domain["Filename"])]

        shuffled_docs = docs_in_domain.sample(frac=1, random_state=args.seed).reset_index(drop=True)

        sentences_to_print, n_sentences = [], 0
        for i, filename in enumerate(shuffled_docs["Filename"].tolist()):
            doc_sentences = sentences[sentences["Filename"] == filename]

            if n_sentences < args.min_sentences_per_domain:
                if domain == "Natives Formal":
                    doc_sentences = doc_sentences.head(NATIVES_FORMAL_HEADER_SIZE + args.max_sentences_per_doc).tail(args.max_sentences_per_doc)
                else:
                    doc_sentences = doc_sentences.head(args.max_sentences_per_doc)

                if not (len(doc_sentences)):
                    continue

                sentences_to_print.append(doc_sentences)
                n_sentences += len(doc_sentences)

        n_docs_printed = len(sentences_to_print)
        sentences_to_print = pd.concat(sentences_to_print)

        # Write the sentences into a txt file.
        with open(os.path.join(args.output_dir, "{}.txt".format(domain.replace(" ", "_"))), "w", encoding="utf-8") as fw:
            for sentence in sentences_to_print["Sentence"]:
                print(sentence, file=fw)

        # Write the sentences and edits into an M2 file.
        with open(os.path.join(args.output_dir, "{}.m2".format(domain.replace(" ", "_"))), "w", encoding="utf-8") as fw:
            for sentence, edits_str in zip(sentences_to_print["Sentence"], sentences_to_print["Edits_str"]):
                print("S {}".format(sentence), file=fw)
                print(edits_str, file=fw)
                print("", file=fw)

        # Print summary.
        print("Domain \"{}\" Summary:".format(domain))
        print("Selected documents: {}/{} ({:.2f}\%), " \
              "sentences: {}/{} ({:.2f}\%), " \
              "edits: {}/{} ({:.2f}\%)".format(n_docs_printed,
                                               len(docs_in_domain),
                                               n_docs_printed * 100 / len(docs_in_domain),
                                               len(sentences_to_print),
                                               len(sentences_in_domain),
                                               len(sentences_to_print) * 100 / len(sentences_in_domain),
                                               sentences_to_print["Edits"].sum(),
                                               sentences_in_domain["Edits"].sum(),
                                               sentences_to_print["Edits"].sum() * 100 / sentences_in_domain["Edits"].sum()))
        print("Edits per sentence:          {:.2f} \u00B1 {:.2f}".format(sentences_in_domain["Edits"].mean(), sentences_in_domain["Edits"].std()))
        print("Edits per selected sentence: {:.2f} \u00B1 {:.2f}".format(sentences_to_print["Edits"].mean(), sentences_to_print["Edits"].std()))
        print("Sentence lengths:          {:.2f} \u00B1 {:.2f}".format(sentences_in_domain["Lengths"].mean(), sentences_in_domain["Lengths"].std()))
        print("Selected sentence lengths: {:.2f} \u00B1 {:.2f}".format(sentences_to_print["Lengths"].mean(), sentences_to_print["Lengths"].std()))
        print("-------------")

        # Save things for the total stats over all domains
        total_selected_sentences.append(sentences_to_print)
        n_selected_docs += n_docs_printed
        n_total_docs += len(docs_in_domain)

    total_selected_sentences = pd.concat(total_selected_sentences)

    print("Total Summary:".format(domain))
    print("Selected documents: {}/{} ({:.2f}\%), " \
          "sentences: {}/{} ({:.2f}\%), " \
          "edits: {}/{} ({:.2f}\%)".format(n_selected_docs,
                                           n_total_docs,
                                           n_selected_docs * 100 / n_total_docs,
                                           len(total_selected_sentences),
                                           len(sentences),
                                           len(total_selected_sentences) * 100 / len(sentences),
                                           total_selected_sentences["Edits"].sum(),
                                           sentences["Edits"].sum(),
                                           total_selected_sentences["Edits"].sum() * 100 / sentences["Edits"].sum()))
    print("Edits per sentence:          {:.2f} \u00B1 {:.2f}".format(sentences["Edits"].mean(), sentences["Edits"].std()))
    print("Edits per selected sentence: {:.2f} \u00B1 {:.2f}".format(total_selected_sentences["Edits"].mean(), total_selected_sentences["Edits"].std()))
    print("Sentence lengths:          {:.2f} \u00B1 {:.2f}".format(sentences["Lengths"].mean(), sentences["Lengths"].std()))
    print("Selected sentence lengths: {:.2f} \u00B1 {:.2f}".format(total_selected_sentences["Lengths"].mean(), total_selected_sentences["Lengths"].std()))
    print("-------------")
