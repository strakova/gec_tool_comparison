# Comparison of the Czech Off-the-Shelf GEC Tools

This repository contains a rigorous evaluation of the available Czech grammar
error correction (GEC) tools on a part of the test data of the GECCC corpus.

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

   - Opravidlo Betaverze, https://opravidlo.cz/, accessed 2024-11-14,
   - Google Docs, accessed 2024-11-24.

6. Evaluate the system corrections with the m2scorer:

```sh
./evaluate_corrections.sh
```

## Contact

Jana Straková `strakova@ufal.mff.cuni.cz`
