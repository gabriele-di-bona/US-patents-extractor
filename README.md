# US-patents-extractor
With this repository, you can download the corpus of all USPTO patents, and parse the information.

Using https://github.com/USPTO/PatentPublicData to download corpus, and https://github.com/JusteRaimbault/PatentsMining to parse.

In this repository, we suppose that the root folder `~/` is this main repository directory. 
This has been tested on QMUL Apocrita HPC cluster. 
It only uses bash scripts that launches jobs on the cluster. 

## Download Corpus
### Setup
Run the following commands from the terminal to clone the USPTO public repository to download the corpus.
```
git clone https://github.com/USPTO/PatentPublicData
cd ~/PatentPublicData
git reset --hard 82d6220d054246265fb14892f45320600288949a
```
Last command is to reset the folder to the same commit used in this repository by the author. You might not need this hard reset, but without it you might not obtain the same results or get new issues.

After this, one need to initalize the repository through Maven (the scripts run code in java). In order to do so, you can run `~/bash_scripts/initialize_maven.sh` from the folder `~/bash_scripts/outputs/`.
This script should download maven into a new repository `~/maven/` and run it on the project `~/PatentPublicData`.

If everything has run smoothly so far, you are ready to download the data.

### Bash script to download corpus
To download the data, run the script `~/bash_scripts/corpus_builder.sh` from the folder `~/bash_scripts/outputs/` (create it with mkdir command). This will download all the weekly bulk data into the folder `~/bulk_data/`.
The script works downloading the whole corpus, although it technically can be interrupted, and it will automatically continue from where it has left. 
However, this option has not been thoroughly tested by the author. There seem to be some weird bugs in this case, and it could fail to download some of the files. 
We hence recommend to delete or move all the files already downloaded within the specified dates.
To change the parameters of the corpus download (e.g. the initial or final date), change the parameters inside the script.

Notice that this has downloaded also an archive named `ipg200317_r1.zip`, which is a copy of `ipg200317.zip` and can be ignored.

## Extract and Parse Corpus
To process and extract the data, run the script `~/bash_scripts/extract.sh` from the folder `~/bash_scripts/outputs/`. This will process the each archive, one per week, depending on the intex of the job. 

These jobs run python 3.9.5 scripts. The environment requirements used are saved in `~\patents.yml`, which should be used to create a local environment and obtain the same results with the command:
```
conda env create -f patents.yml
```

The processed data is saved into the folder `~/extracted_data/` as a list of dicts saved as `.pkl.gz` files, one dict for each patent.
The keys of each patent could be empty strings if not found. if there is any mistake during the process, a respective error `.txt` file is created.

In order to see how many archives there are (and so how many indices to use in extract.sh), either check the output of the extraction script, or run the following inside the directory `~/bulk_data/`:
```
ls | wc -l
```

## Filter data and more analysis

Once all data has been downloaded and extracted, now we need to solve all issues in the dataset, better define uid, citations, kind, and classification. 
This is all done in the other repository `Recombinations-evolution` (check the README therein for more information).