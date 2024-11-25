# Comparison of the Czech Off-the-Shelf GEC Tools

This repository contains a rigorous evaluation of the available Czech
off-the-shelf grammar error correction (GEC) tools on a part of the test data of
the GECCC corpus.

| System     | NF    | NWI   | R     | SL    |       |
| ---------- | ----- | ----- | ----- | ----- | ----- |
| Opravidlo  | 32.95 | 45.97 | 31.51 | 22.13 | 32.76 |
| Korektor   | 36.90 | 24.66 | 48.86 | 54.66 | 44.71 |
| GoogleDocs | 39.56 | 29.03 | 52.23 | 47.13 | 45.45 |

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

5. Manually upload/open the documents in the GEC tools of your choice, accept
   all the suggested GEC corrections, and save the results into
   `GECCC_corrections`. We used the following:

   - [Opravidlo Betaverze](https://opravidlo.cz/), accessed 2024-11-14,
     postprocessed with `postprocess_googledocs_and_opravidlo.sh`,
   - [Korektor](https://ufal.mff.cuni.cz/korektor), accessed 2024-11-19,
   - [Google Docs](https://docs.google.com), accessed 2024-11-20, postprocessed
     with `postprocess_googledocs_and_opravidlo.sh`.

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
