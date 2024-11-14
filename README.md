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

3. Install Python venv:

```sh
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

4. Select the test sentences from GECCC for evaluation. Current default values
   of the script will select cca 10% of the test sentences, and you should get
   the same stats as in the file `stats.txt`:

```sh
venv/bin/python ./select_sentences_for_evaluation.py
```

5. Manually upload/open the documents in the GEC tools of your choice and accept
   all the suggested GEC corrections. We used the following:

   - Opravidlo Betaverze, https://opravidlo.cz/, accessed 2024-11-14,
   - Google Docs, accessed 2024-11-24.

  You will find the corrections in directory `GECCC_corrections/`.
