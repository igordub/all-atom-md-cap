# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
""" mdout summary data wrangler

    This script wrangles `process_mdout.perl` output data.

    This script requires that packgaes within the `comp-biophys` environment 
    be installed within the Pyhton environment you are running this script in.
    See `ccenv.yml` for more deatils.

    This file can also be imported as a module and contains the following
    functions:
        * main - the main function of the script
        * import_summary_data - imports and wragles .mdout summary data
        * import_rmsd - imports RMSD data into a DataFrame

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
    summary_filepaths = glob.glob(join_paths(input_dir, "summary.*"))
    summary_data = import_summary_data(summary_filepaths)
    
    # rmsd_path = join_paths(input_dir, "rmsd.all.agr")
    # rmsd_data = import_rmsd(rmsd_path)

    # summary_data['rmsd'] = rmsd_data['rmsd'].to_numpy()

    summary_data.to_csv(join_paths(output_dir, "summary_mdout.csv"))

    return None

def import_summary_data(filepaths):
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
    summary_data = pd.read_fwf(filepaths[0], infer_nrows= 100000, header=None, usecols=[0])
    summary_data.columns = ['time']

    for filepath in filepaths:
        values = pd.read_fwf(filepath, infer_nrows= 100000, header=None, usecols=[0,1]).to_numpy()
        column_name = get_basename(filepath).replace("summary.","").lower()
        if values.shape[1] == 1:
            continue
        summary_data[column_name] = values[:,1]

    summary_data.set_index('time', inplace=True)
    summary_data = summary_data[['eptot', 'ektot', 'etot', 'temp', 'pres', 'volume', 'density']]

    return summary_data

def import_rmsd(filepath):
    """ Imports RMSD data from `cpptraj` output. 

        Parameters
        ----------
        filepath : str
            The location of the RMSD file

        Returns
        -------
        pandas.DataFrame
            wrangled data into a single DataFrame

    """ 
    rmsd_data = pd.read_fwf(filepath, infer_nrows= 100000, header=None, comment='@')
    rmsd_data.columns = ['time', 'rmsd']
    rmsd_data.set_index('time', inplace=True)

    return rmsd_data

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main_commandline()



