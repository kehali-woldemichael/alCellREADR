from os.path import dirname, split
import os
import sys
import logging


import pandas as pd

from Bio import SeqIO
from Bio.Seq import Seq 
from Bio.SeqRecord import SeqRecord

from py_modules.utility import *

# Generates basepath ... to project directory 
path_outputDir = f"{split(dirname(__file__))[0]}/Test" 
path_targetSeq = f"{path_outputDir}/db/dbRNA.fasta"
path_db = f"{path_outputDir}/output/test_db"


def write_sequences(targetSeq, querySeq):
    outputRecord = SeqRecord(targetSeq.upper(), id = "target sequence", description = "For testing sd binding to target")
    with open(path_targetSeq, "w") as output_handle:
        SeqIO.write(outputRecord, output_handle, "fasta") 
    
    for i, sd in enumerate(querySeq, start = 1):
        outputRecord = SeqRecord(sd.upper(), id = "test_sd", description = "For testing sd binding to target")
        path_querySeq = f"{path_outputDir}/query/queryRNA_sd_{i}.fasta"
        with open(path_querySeq, "w") as output_handle:
            SeqIO.write(outputRecord, output_handle, "fasta") 

def output_RIblast(targetSeq, sesRNAs): 
    write_sequences(targetSeq, sesRNAs)

    # Path and file name for output CSV
    outputName = f"{path_outputDir}/output/output.csv"  

    # Generating pd.DataFrame for storing calculated values
    columns_RIblast = [' Accessibility Energy', ' Hybridization Energy', ' Interaction Energy', ' BasePair',
                    ' Accessibility Energy', ' Hybridization Energy', ' Interaction Energy', ' BasePair']
    useful_RIblast =  pd.DataFrame(columns = columns_RIblast)

    # Generating query database
    commandQuery = f"RIblast db -i {path_targetSeq} -o {path_db}"
    os.system(commandQuery)

    # Iteratively generating calculations for sesRNA-target interaction
    # Made sure to go through sesRNA files in order
    for entry in sorted(os.scandir(f"{path_outputDir}/query"), key=lambda e: e.name):
        logging.debug(f"Path for current sesRNA {entry.path}")
        # Running RIblast calculations
        os.system(f"RIblast ris -i {entry.path} -o {outputName} -d {path_db}")

        # Remove first two lines from CVS to allow for parsing into pandas.Dataframe
        os.system(f"sed -i 1,2d {outputName}")

        outputCSV =  pd.read_csv(outputName, skiprows=[1])
        # Sorting by hybirzation energy ... have to have extra white space before column name
        sorted_outputCSV = outputCSV.sort_values(' Hybridization Energy')

        topHybridizationE = sorted_outputCSV[[' Accessibility Energy', ' Hybridization Energy', ' Interaction Energy', ' BasePair']].iloc[0:1]
        secondHybridizationE = sorted_outputCSV[[' Accessibility Energy', ' Hybridization Energy', ' Interaction Energy', ' BasePair']].iloc[1:2]
        temp_RIblast_ouput = pd.concat([topHybridizationE.reset_index(drop=True), secondHybridizationE.reset_index(drop=True)], axis = 1)

        # Appending calculations for current sesRNA values
        useful_RIblast = pd.concat([useful_RIblast, temp_RIblast_ouput])

        # Clearing csv
        os.system(f"rm -rf {outputName}")
        # Clear BioPython temp fasta file for sesRNA
        os.system(f"rm -rf {entry.path}")

    clear_outputs()
    
    return useful_RIblast
