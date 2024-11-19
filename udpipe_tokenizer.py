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
UDPipe Czech sentence tokenizer.

Tokenizes Czech sentences from a txt file, each one by one, thereby treating
the sentences as presegmented. Specifically, the number of output (tokenized)
lines will be exactly the same as the number of input sentences (lines) to
tokenize. Input sentences are not merged, neither are they segmented further.
If the UDPipe suggests further segmentation, the tokenized sentence fragments
are merged together to keep the sentence on one line.

The class UDPipeTokenizer is copied from NameTag 3 server:
https://github.com/ufal/nametag3/blob/main/nametag3_server.py
"""


import sys

import ufal.udpipe


class UDPipeTokenizer:
    class Token:
        def __init__(self, token, spaces_before, spaces_after):
            self.token = token
            self.spaces_before = spaces_before
            self.spaces_after = spaces_after


    def __init__(self, path):
        self._model = ufal.udpipe.Model.load(path)
        if self._model is None:
            raise RuntimeError("Cannot load tokenizer from {}".format(path))

    def tokenize(self, text, mode="untokenized"):
        if mode == "untokenized":
            tokenizer = self._model.newTokenizer(self._model.DEFAULT)
        elif mode == "vertical":
            tokenizer = ufal.udpipe.InputFormat.newVerticalInputFormat()
        elif mode.startswith("conllu"):
            tokenizer = ufal.udpipe.InputFormat.newConlluInputFormat()
        else:
            raise ValueError("Unknown tokenizer mode '{}'".format(mode))
        if tokenizer is None:
            raise RuntimeError("Cannot create the tokenizer")

        sentence = ufal.udpipe.Sentence()
        processing_error = ufal.udpipe.ProcessingError()
        tokenizer.setText(text)
        while tokenizer.nextSentence(sentence, processing_error):
            yield sentence
            sentence = ufal.udpipe.Sentence()
        if processing_error.occurred():
            raise RuntimeError("Cannot read input data: '{}'".format(processing_error.message))


if __name__ == "__main__":

    tokenizer = UDPipeTokenizer("udpipe_tokenizer/czech-pdt-ud-2.5-191206.udpipe")

    for line in sys.stdin:
        sentences = [sentence for sentence in tokenizer.tokenize(line.strip())]

        # Skip multiwords, get tokens from sentences
        tokens = []
        for sentence in sentences:
            word, multiword_token = 1, 0
            while word < len(sentence.words):
                if multiword_token < len(sentence.multiwordTokens) and sentence.multiwordTokens[multiword_token].idFirst == word:
                    token = sentence.multiwordTokens[multiword_token]
                    word = sentence.multiwordTokens[multiword_token].idLast + 1
                    multiword_token += 1
                else:
                    token = sentence.words[word]
                    word += 1
                tokens.append(token.form)

        print(" ".join(tokens))
