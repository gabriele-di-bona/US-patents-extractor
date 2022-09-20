# US-patents-extractor
Using https://github.com/USPTO/PatentPublicData to download corpus, and https://github.com/JusteRaimbault/PatentsMining to parse.

## Download Corpus
### Setup
Run the following commands from the terminal to clone the USPTO public repository to download the corpus.
```
git clone https://github.com/USPTO/PatentPublicData
cd PatentPublicData
git reset --hard 82d6220d054246265fb14892f45320600288949a
```
Last command is to reset the folder to the same commit used in this repository. You might not need this hard reset.

After this, one need to initalize the repository through Maven. In order to do so, you can run `~/bash_scripts/initialize_maven.sh` from the folder `~/bash_scripts/outputs/`.
This script should download maven into a new repository `~/maven/` and run it on the project `~/PatentPublicData`.

If everything has run smoothly so far, you are ready to download the data.

### Bash script to download corpus
To download the data, run the script `~/bash_scripts/corpus_builder.sh` from the folder `~/bash_scripts/outputs/`. This will download all the weekly bulk data into the folder `~/bulk_data/`.
The script technically can be interrupted, and it will automatically continue from where it has left. However, there are some bugs and it could fail to download some of the files. We recommend to delete or move all the files already downloaded within the specified dates.
To change the parameters of the corpus download (e.g. the initial or final date), change the parameters inside the script.

## Extract and Parse Corpus
To process and extract the data, run the script `~/bash_scripts/extract.sh` from the folder `~/bash_scripts/outputs/`. This will process the first archive (only 1 week). In order to process the other archives, run the script changing the index. The processed data is saved into the folder `~/extracted_data/` as a list of dicts saved as `.pkl.gz` files, one dict for each patent.
The keys of each patent could be empty strings if not found. if there is any mistake during the process, a respective error `.txt` file is created.

In order to see how many archives there are, either check the output of the extraction script, or run the following inside the directory `~/bulk_data/`.

```
ls | wc -l
```