# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
""" B-factors data wrangler

    This script wrangles B-factors data outputed from `cpptraj`.

    This script requires that packgaes within the `comp-biophys` environment 
    be installed within the Pyhton environment you are running this script in.
    See `ccenv.yml` for more deatils.

    This file can also be imported as a module and contains the following
    functions:
        * main - the main function of the script
        * import_exp_bfacts - imports experimental B-factors
        * import_enm_bfacts - imports B-factors from ENM simulation 
        * import_md_bfacts - imports B-factors from MD simulation

"""
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import pandas as pd
import numpy as np
from os.path import join as join_paths, basename as get_basename
import glob


@click.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path())
def main_commandline(input_dir, output_dir):
    """ The main command line function.
        Uses `click` decorators. 

        Parameters
        ----------
        input_dir : str
            The location of the input directory
        output_dir : str
            The location of the output directory

        Returns
        -------
        None

    """ 
    logger = logging.getLogger(__name__)
    logger.info('wrangle B-factors data')

    main(input_dir, output_dir)

    return None
    
###################################################################################

def main(input_dir, output_dir):
    """ The main fucniton of this script. 

        Parameters
        ----------
        input_dir : str
            The location of the input directory
        output_dir : str
            The location of the output directory

        Returns
        -------
        None

    """ 
    # bfactors_exp = pd.read_csv(join_paths("data/external", "bfactors.exp.csv"))
    bfactors_md = import_md_bfactors(join_paths("data/05-analysis", "bfactors.CA.agr"))
    bfactors_enm = import_enm_bfactors(join_paths("data/external", "mode.bfactors"))
    # Renumber residues
    # For the future, use PDB files processed for all-atom MD 
    # when running ENM simulations

    bfactors = bfactors_enm[['residue_number', 'bfactor_exp', 'bfactor_scaled']].copy()
    bfactors.rename(columns={'bfactor_scaled': 'bfactor_enm'}, inplace=True)
    bfactors['bfactor_md'] = bfactors_md['bfactor'][
        bfactors_md['residue_number'].isin(bfactors['residue_number'])]

    bfactors.to_csv(join_paths(output_dir, "bfactors.csv"), index=None)

    return None

def import_md_bfactors(filepath):
    """ Imports summary data from `process_mdout.perl`
        script output data. 

        Parameters
        ----------
        filepaths : list
            The summary file paths

        Returns
        -------
        pandas.DataFrame
            wrangled data into a single DataFrame

    """ 
    bfactors = pd.read_fwf(filepath, infer_nrows= 100000, header=None, 
        comment='@', skiprows=8)
    bfactors.columns = ['residue_number', 'bfactor']

    return bfactors

def import_enm_bfactors(filepath):
    """ Imports summary data from `process_mdout.perl`
        script output data. 

        Parameters
        ----------
        filepaths : list
            The summary file paths

        Returns
        -------
        pandas.DataFrame
            wrangled data into a single DataFrame

    """ 
    bfactors = pd.read_fwf(filepath, infer_nrows= 100000, header=None, comment='#')
    bfactors.columns = ['record_name', 'atom_number', 'atom_name',
        'residue_name', 'chain_id', 'residue_number', 
        'bfactor_pred', 'bfactor_fullscaled', 'bfactor_scaled', 
        'bfactor_exp']
    bfactors.astype({'record_name': str, 'atom_number': int, 'atom_name': str,
        'residue_name': str, 'chain_id':str, 'residue_number': int, 
        'bfactor_pred': float, 'bfactor_fullscaled': float, 'bfactor_scaled': float, 
        'bfactor_exp': float})

    return bfactors

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main_commandline()
