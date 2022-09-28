#!/bin/bash
#$ -cwd
#$ -t 1-2490
#$ -j y
#$ -pe smp 1
#$ -l h_vmem=10G
# #$ -l highmem
#$ -l h_rt=240:0:0
# #$ -m bae

module load anaconda3
export OMP_NUM_THREADS=1
conda activate patents
cd ../../python_scripts # we are running this job from the subfolder outputs in bash_scripts

python extractor.py -i ${SGE_TASK_ID}