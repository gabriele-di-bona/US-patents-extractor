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

Notice that this has downloaded also an archive named `ipg200317_r1.zip`, which is a copy of `ipg200317.zip` and can be ignored.

## Extract and Parse Corpus
To process and extract the data, run the script `~/bash_scripts/extract.sh` from the folder `~/bash_scripts/outputs/`. This will process the first archive (only 1 week). In order to process the other archives, run the script changing the index. The processed data is saved into the folder `~/extracted_data/` as a list of dicts saved as `.pkl.gz` files, one dict for each patent.
The keys of each patent could be empty strings if not found. if there is any mistake during the process, a respective error `.txt` file is created.

In order to see how many archives there are, either check the output of the extraction script, or run the following inside the directory `~/bulk_data/`:
```
ls | wc -l
```

## Filter data

Once all data has been downloaded and extracted, now we need to solve all issues in the dataset, better define uid, citations, kind, and classification. 

Here, we want to consider only the utility patents, i.e., of kind A before 2001, and B1 and B2 after 2001 (they're just a continuation of A). The only difference between B1 and B2 is that in B1 there has not been any applications published before this patent has been granted.

In order to filter all data, one needs to run the whole jupyter notebook `~/notebooks/filter_extracted_data.ipynb`. 
If the process is successful, you should find two files in your repository, named `~/filtered_data/utility_df.pkl.gz`, a pd.DataFrame containing only utility patents and all their informations (notice the last columns, that have processed the data and are in the correct format, e.g., `correct_uid` vs `uid`), and `~/filtered_data/mapping_old_to_correct_uid.pkl.gz`, a dict linking `uid` to `correct_uid`. 