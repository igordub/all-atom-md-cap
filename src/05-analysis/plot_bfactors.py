""" Plot wrangled B-factors

    This script plots experimental, MD and ENM wrangeled B-factor data.

    This script requires that packgaes within the `comp-biophys` environment 
    be installed within the Pyhton environment you are running this script in.
    See `ccenv.yml` for more deatils.

    This file can also be imported as a module and contains the following
    functions:
        * main - the main function of the script
        * import_summary_data - imports and wragles .mdout summary data

"""
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import pandas as pd
import numpy as np
from os.path import join as join_paths, basename as get_basename
import glob

import sys
sys.path.append("./src")
import src.utilities as utils

import matplotlib.pyplot as plt

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
    logger.info('wrangle processed .mdout data')

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
    config = utils.read_config()
    # plt.style.use(config['viz']['default'])
    bfactors = pd.read_csv(join_paths(input_dir, "bfactors.csv"))

    _, ax = plt.subplots(figsize=(4,2.5), constrained_layout=True)

    ax.plot(bfactors['residue_number'], bfactors['bfactor_exp'], label='exp')
    ax.plot(bfactors['residue_number'], bfactors['bfactor_md'], label='MD')
    ax.plot(bfactors['residue_number'], bfactors['bfactor_enm'], label='ENM')
    ax.set_ylabel("B-factor")
    ax.set_xlabel("Residue number")
    ax.set_title("B-factor comparison")
    ax.legend(frameon=False)
    plt.show()

    plt.savefig(join_paths(output_dir, "bfactors.pdf"), bbox_inches='tight')
    plt.savefig(join_paths(output_dir, "bfactors.png"), bbox_inches='tight')


    return None

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main_commandline()



