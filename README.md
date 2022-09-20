# US-patents-extractor
Using https://github.com/USPTO/PatentPublicData to download corpus, and https://github.com/JusteRaimbault/PatentsMining to parse.

## Download Corpus
### Setup
Run the following commands to clone the USPTO public repository to download the corpus.
```
$ git clone https://github.com/USPTO/PatentPublicData
$ cd PatentPublicData
$ git reset --hard 82d6220d054246265fb14892f45320600288949a
```
Last command is to reset the folder to the same commit used in this repository. You might not need this hard reset.

After this, one need to initalize the repository through Maven. In order to do so, you can run `~/bash_scripts/initialize_maven.sh` from the folder `~/bash_scripts/outputs/`.
This script should download maven into a new repository `~/maven/` and run it on the project `~/PatentPublicData`.

If everything has run smoothly so far, you are ready to download the data.

### Bash script to download corpus
To download the data, run the script `~/bash_scripts/corpus_builder.sh` from the folder `~/bash_scripts/outputs/`. This will download all the weekly bulk data into the folder `~/bulk_data/`.
The script can be interrupted, and it will automatically continue from where it has left.
To change the parameters of the corpus download (e.g. the initial or final date), change the parameters inside the script.

## Parse Corpus