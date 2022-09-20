# US-patents-extractor
Using https://github.com/USPTO/PatentPublicData to download corpus, and https://github.com/JusteRaimbault/PatentsMining to parse.

## Download Corpus
### Clone USPTO repository
Run the following commands to clone the USPTO public repository to download the corpus.
```
$ git clone https://github.com/USPTO/PatentPublicData
$ cd PatentPublicData
$ git reset --hard 82d6220d054246265fb14892f45320600288949a
```
Last command is to reset the folder to the same commit used in this repository. You might not need this hard reset.

### Bash script to 