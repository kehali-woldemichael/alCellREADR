
from os.path import basename, dirname, splitext, split
import pandas as pd 

base_path = split(dirname(__file__))[0]
path_speciesEnsembl = f"{base_path}/Reference/SpeciesEnsembl.csv" 

def return_scientificName(speciesName):
    """Returns scientific name in correct format given species common name
    For accessing ensembl rest API"""

    # csv file from ensembl of species comman names and etc ...
    speciesEnsembl = pd.read_csv(path_speciesEnsembl)
    scientificName = speciesEnsembl[speciesEnsembl['Common name'] == speciesName]['Scientific name']
    taxonID = speciesEnsembl[speciesEnsembl['Common name'] == speciesName]['Taxon ID']

    return scientificName.tolist()[0].lower().replace(" ", "_"), taxonID.tolist()[0]
