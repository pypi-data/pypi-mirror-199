#!/bin/bash --login
#SBATCH --job-name=ms_weighting_120_23
#SBATCH --time=8-00:00:00
#SBATCH --cpus-per-task=64
#SBATCH --mem-per-cpu=4096
#SBATCH --ntasks=1
#SBATCH --output=/home/prwells/logs/0924_weighting/0924_final/ms_120asec_i23.log
#SBATCH -p p-fassnacht
#SBATCH -A fassnacht

conda activate lenskappa
python -u /home/prwells/scripts/0924_final/ms/ms_i23_120asec.py
