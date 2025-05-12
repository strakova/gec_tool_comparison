# Comparison of the Czech Off-the-Shelf GEC Tools

This repository contains a rigorous evaluation of the available Czech
off-the-shelf grammar error correction (GEC) tools on a part of the test data of
the GECCC corpus.

| System     | NF    | NWI   | R     | SL    | All Domains   |
| ---------- | ----- | ----- | ----- | ----- | ------------- |
| Opravidlo  | 32.95 | 45.97 | 31.51 | 22.13 | 32.76         |
| Korektor   | 36.90 | 24.66 | 48.86 | 54.66 | 44.71         |
| GoogleDocs | 39.56 | 29.03 | 52.23 | 47.13 | 45.45         |
| MSWord     | 52.25 | 46.20 | 51.63 | 55.22 | 51.54         |
| DeepSeek R1 70B zero-shot (see disclaimer) | 36.06 | 52.34 | 58.46 | 58.11 | 53.58 |
| GPT4o zero-shot (see disclaimer) | 59.06 | 78.88 | 77.16 | 75.64 | 74.60 |
| Naplava2022_synthetic | 45.92 | 38.14 | 51.14 | 61.79 | 51.81 |
| Naplava2022_ag_finetuned | 66.45 | 55.02 | 74.39 | 71.81 | 69.82 |
| Naplava2022_geccc_finetuned | 73.15 | 70.95 | 77.17 | 74.64 | 74.68 |

## How to Reproduce the Results

1. Clone this repository:

```sh
git clone https://github.com/strakova/gec_tool_comparison
```

2. Download the GECCC corpus into the `GECCC` directory, and unzip it:

```sh
mkdir GECCC
cd GECCC
curl --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-4861{/geccc.zip}
unzip geccc.zip
```

3. Install dependencies:

```sh
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

4. Select the test sentences from GECCC for evaluation. Current default values
   of the script will select 10.36% of the test sentences, and you should get
   exactly the same stats as in the file `stats.txt`:

```sh
venv/bin/python ./select_sentences_for_evaluation.py
```

5. Upload/open the documents in the GEC tools of your choice, accept all the
   suggested GEC corrections, and save the results into `GECCC_corrections`. We
   used the following:

   - [Opravidlo Betaverze](https://opravidlo.cz/), accessed 2024-11-14,
     postprocessed with `postprocess_googledocs_and_opravidlo.sh`,
   - [Korektor](https://ufal.mff.cuni.cz/korektor), accessed 2024-11-19, you can
     reproduce the results by running `korektor.sh`,
   - [Google Docs](https://docs.google.com), accessed 2024-11-20, postprocessed
     with `postprocess_googledocs_and_opravidlo.sh`,
   - MSWord, accessed 2025-01-31, using the `final_vba.txt` macro to go
     through data,
   - open-source large language model (LLM) Deep Seek R1 70B, prompted in zero-shot
     setting (see disclaimer below), see `deepseek.py`,
   - large language model (LLM) GPT4o, prompted in zero-shot setting (see
     disclaimer below), accessed 2025-05-02,
   - to get predictions by [Náplava et al. (2022)](https://doi.org/10.1162/tacl_a_00470), run script
     `select_predictions.py` with the default values. The script will select the
     predictions corresponding to the selected sentences from `Naplava2022` to
     `GECCC_corrections`.

Data exposure disclaimer: Since the GECCC training, development, and even test
data have been freely available online since 2022, and the training corpora of
large language models (LLMs) are typically undisclosed, it is impossible to
determine whether the evaluation setting is genuinely zero-shot, that is, to
what extent the GECCC data may have been seen during pretraining. More
concerningly, the test data itself may have been included in the LLMs’ training
sets.

6. Evaluate the system corrections with the m2scorer. The evaluations will be
   printed to `*.eval` files in the directory `GECCC_evals`:

```sh
./evaluate_corrections.sh
```

7. Generate LaTeX table rows from the evaluations in `GECCC_evals`:

```sh
./make_table.py
```

## Contact

Jana Straková `strakova@ufal.mff.cuni.cz`
