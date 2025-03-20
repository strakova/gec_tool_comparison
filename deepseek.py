#!/usr/bin/env python3
# coding=utf-8
#
# Copyright 2025 Institute of Formal and Applied Linguistics, Faculty of
# Mathematics and Physics, Charles University, Czech Republic.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
GEC by prompting LLM (DeepSeek) on the ollama engine.

This script sends HTTP requests to the DeepSeek LLM running on the Ollama
engine.

Example Usage:
--------------

For zero-shot DeepSeek:

./llm_baseline.py --server http://my-ollama-server:port --model=deepseek-r1:70b --num_ctx=2048
"""


import random
import requests
import os
import sys
import time


if __name__ == "__main__":
    import argparse

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="GECCC_test_selection/", type=str, help="Input directory.")
    parser.add_argument("--max_tokens", default=5000, type=int, help="Maximum tokens in sentences (recommended: max LLM context size / 2).")
    parser.add_argument("--model", default="deepseek-r1:70b", type=str, help="Model name.")
    parser.add_argument("--num_ctx", default=None, type=int, help="Model context size.")
    parser.add_argument("--output", default="GECCC_corrections/DeepSeek70B_zero_shot/", type=str, help="Output directory.")
    #parser.add_argument("--seed", default=42, type=int, help="Random seed.")
    parser.add_argument("--server", required=True, default=None, type=str, help="Server address with port.")
    parser.add_argument("--sleep", default=1, type=int, help="Sleep seconds between requests.")

    args = parser.parse_args()

    #random.seed(args.seed)

    prompt = "Jsi expert na opravu gramatických chyb. Tvým úkolem je opravit pouze gramatické chyby v daném textu, aniž bys měnil(a) styl, význam nebo faktický obsah. Neměň tón, volbu slov, strukturu vět ani faktické informace, pokud to není nezbytné k opravě gramatické chyby. Uveď pouze opravenou verzi bez vysvětlení. Pokud je text už gramaticky správný, okopíruj pouze opravovaný text přesně beze změny a už nic jiného. Oprav následující text:\n"

    for domain in os.listdir(args.input):
        domain_dir = os.path.join(args.input, domain)
        if not os.path.isdir(domain_dir):
            continue

        output_domain_dir = os.path.join(args.output, domain)
        print("Making output directory {}".format(output_domain_dir))
        os.makedirs(output_domain_dir, exist_ok=True)

        for input_filename in os.listdir(domain_dir):

            print("Prompting corrections for file {}".format(os.path.join(domain_dir, input_filename)))
            with open(os.path.join(domain_dir, input_filename), "r", encoding="utf-8") as fr:

                output_filename = os.path.join(output_domain_dir, input_filename)
                print("Writing corrections to output file {}".format(output_filename), file=sys.stderr)
                with open(os.path.join(output_domain_dir, input_filename), "w", encoding="utf-8") as fw:

                    for line in fr.readlines():
                        line = line.strip()
                        line_prompt = prompt + line

                        # Log the prompt
                        print("Prompt:", file=sys.stderr)
                        print(line_prompt, file=sys.stderr)

                        # Create request
                        response_options_json = {
                            "model": args.model,
                            "prompt": line_prompt,
                            "stream": False
                        }

                        if args.num_ctx:
                            response_options_json["options"] = {
                                "num_ctx": args.num_ctx
                            }

                        # Make request
                        try:
                            response = requests.post("{}/api/generate".format(args.server), json=response_options_json)
                            if response.status_code == 200:
                                correction = response.json()["response"].split("\n")[-1]

                                # DeepSeek copied the prompt instead of input => copy input.
                                if correction.startswith("Jsi expert na opravy gramatických chyb.") or correction.startswith("Oprav následující text:") or correction.startswith("Opravený text:"):
                                    print("Warning: DeepSeek copied the prompt into output, removing the prompt and copying the input.", file=sys.stderr)
                                    correction = line

                                # Log the postprocessed correction
                                print("Response:", file=sys.stderr)
                                print(correction, file=sys.stderr)

                                print(correction, file=fw, end="\n", flush=True)
                            else:
                                print("Warning: Response status code {} for sentences file {}".format(response.status_code, os.path.join(domain_dir, input_filename)), file=sys.stderr)
                        except requests.exceptions.RequestException as error:
                            print("Warning: A server error occured on the side of server: {} for file {}".format(error, os.path.join(domain_dir, input_filename)), file=sys.stderr)

                        # Pacing mechanism to be nice.
                        time.sleep(args.sleep)
