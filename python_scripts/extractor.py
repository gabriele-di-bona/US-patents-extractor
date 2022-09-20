import os
from datetime import datetime
import argparse
import zipfile
import joblib
import gzip

# Change directory to the root of the folder (this script was launched from the subfolder python_scripts)
# All utils presuppose that we are working from the root directory of the github folder
os.chdir("../")
import sys
# Add utils directory in the list of directories to look for packages to import
sys.path.insert(0, os.path.join(os.getcwd(),'utils'))
sys.path.insert(0, os.path.join(os.getcwd(),'utils', 'extraction'))

# local utils
from parsing import *


def import_file(file_path = None, file_object = None, use_default_folder = True, use_as_name_archive = True, year = None, bulk_data_folder='./bulk_data/'):
    if file_path is None:
        print('No file_path provided, try again.')
        return None
    if file_object is None:
        if use_as_name_archive == False:
            name_archive = file_path.split('/')[-1]
        else:
            name_archive = file_path
        if '.' in file_path:
            name_archive = name_archive.split('.')[-2]
        if use_as_name_archive == True:
            file_path = os.path.join(bulk_data_folder,f'{name_archive}.zip')
        archive = zipfile.ZipFile(file_path, 'r')
        for filename in archive.namelist():
            file_object = archive.open(f'{filename}', mode='r')
    else:
        if use_as_name_archive == False:
            name_archive = file_path.split('/')[-1]
        else:
            name_archive = file_path
        if '.' in file_path:
            name_archive = name_archive.split('.')[-2]
    print('importing file '+str(name_archive))

    data = parse_file(f=file_path,file_object=file_object, year=year)

    return data


########################### MAIN ###########################

start_time = datetime.now()
print(f"Started script at {start_time}", flush = True)


# Use arguments to give from shell
shell_parser = argparse.ArgumentParser(description='Extract all patents from the bulk data. This script processes only one archive at a time, whose index is given by shell. The data is saved as a list of dicts, one dict for each patent. The keys of each patent could be empty strings if not found.')

# quiet argument, to supress info
shell_parser.add_argument(
    "-i", "--index_archive", type=int,
    default=-1,
    help="Index of the archive list to choose the archive to be processed."
    )

# Parse shell arguments
arguments = shell_parser.parse_args()
index_archive = arguments.index_archive


# Define all folder paths
root_folder = './'
bulk_data_folder = os.path.join(root_folder, 'bulk_data/')
extracted_data_folder = os.path.join(root_folder, 'extracted_data/')
os.makedirs(extracted_data_folder, exist_ok = True)


# NB: archives are all .zip
archives_paths = [path for path in os.listdir(bulk_data_folder) if path[-4:] == ".zip"]
path = archives_paths[index_archive]
print('Requested path n. %d out of %d, that is\n\t%s'%(index_archive,len(archives_paths), path), flush=True)

name_archive = path[:-4] # cutting the '.zip' string
archive = zipfile.ZipFile(os.path.join(bulk_data_folder,f'{name_archive}.zip'), 'r')
if len(archive.namelist()) > 1:
    print('There are more than 1 element inside the archive, which one should I choose? Here they are.', flush=True)
    print(archive.namelist(), flush=True)
    with open(os.path.join(extracted_data_folder, f'{name_archive}_ERROR.txt'), 'w') as fp:
        fp.writelines(archive.namelist())
    print(f'Exiting at {datetime.now()}...', flush=True)
    exit()

for unzipped_file_path in archive.namelist():
    print('Opening',unzipped_file_path)
    file_name = unzipped_file_path.split('/')[-1]
    file_object = archive.open(f'{unzipped_file_path}', mode='r')
    patents = import_file(file_path=unzipped_file_path,file_object=file_object, year=None,use_as_name_archive = False)

print(f"FOUND {len(patents)} PATENTS.", flush=True)

with gzip.open(os.path.join(extracted_data_folder, f'{name_archive}.pkl.gz'), 'wb') as fp:
    joblib.dump(patents, fp)

print('All dumped', flush=True)
print(f'Script time: {datetime.now() - start_time}', flush=True)
print(f'Exiting script at {datetime.now()}', flush=True)