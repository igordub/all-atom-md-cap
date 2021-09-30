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

import matplotlib as mpl
import matplotlib.pyplot as plt

import sys
sys.path.append("./src") 
import src.utilities as utils

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
    logger.info('plot eigenvalues')

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
    mpl.rcParams.update(mpl.rcParamsDefault)
    # plt.style.use(config['viz']['default'])
    color_cycler = plt.rcParams['axes.prop_cycle'].by_key()['color']

    MD_EVALS_PATH   = "tmp/evals.dat"
    ENM_EVALS_PATH  = "tmp/eigenvals.csv"
    ENM_FREQ_PATH   = "tmp/mode.frequencies"

    evals_md = pd.read_fwf(MD_EVALS_PATH, infer_nrows=7000, header=None)
    evals_md.columns = ['mode_number', 'eigenvalue_0']
    # evals_md['eigenvalue_0'] = np.sqrt(evals_md['eigenvalue_0'].to_numpy())
    evals_md['mode_number'] = evals_md['mode_number'] + 6
    evals_md.set_index('mode_number', drop=True, inplace=True)

    evals_enm = pd.read_csv(ENM_EVALS_PATH, index_col='mode_number')

    freq_enm = pd.read_csv(ENM_FREQ_PATH, comment='#', header=None)
    freq_enm.columns = ['eigenvalue_0']
    freq_enm['mode_number'] = np.arange(1,freq_enm.shape[0]+1)
    freq_enm.set_index('mode_number', drop=True, inplace=True)
    freq_enm = freq_enm[6:]


    plot_modes = 940
    plot_modes += 6 

    fig, axs = plt.subplots(2,2, figsize=(6,6), constrained_layout=True)

    ax = axs[0][0]
    ax.scatter(evals_md[:plot_modes].index, evals_md[:plot_modes]['eigenvalue_0'],
        label='MD', color=color_cycler[0], s=5)
    ax.scatter(evals_enm[:plot_modes].index, evals_enm[:plot_modes]['eigenvalue_0'],
        label='ENM', color=color_cycler[1], s=5)
    ax.set_ylabel("$\lambda$ [$cm^{-1}$]")
    ax.set_xlabel("Mode number")
    ax.set_title("Eigenvalues")
    ax.legend(frameon=False)


    evals_ratio = evals_md['eigenvalue_0'] / evals_enm['eigenvalue_0']
    ax = axs[0][1]
    ax.scatter(evals_ratio[:plot_modes].index, evals_ratio[:plot_modes],
        color=color_cycler[2], s=5)
    ax.set_ylabel("$\lambda_{MD}/\lambda_{ENM}$")
    ax.set_xlabel("Mode number")
    ax.set_title("MD/ENM ratio")


    no_bins = 35
    hist_kwargs = dict( histtype='step', 
                        alpha=1, 
                        # color = colourWheel[j%len(colourWheel)],
                        # linestyle = lineStyles_hist[j%len(lineStyles_hist)],
                        # density=True,
                        # label = column_name, 
                        bins=no_bins)

    ax = axs[1][0]
    ax.hist(evals_md['eigenvalue_0'][:950].to_numpy(), **hist_kwargs, 
        color=color_cycler[0])
    ax.set_ylabel("# modes per bin")
    ax.set_xlabel("$\lambda$ [$cm^{-1}$]")
    ax.set_title("MD DOS | # bins = {}".format(no_bins))


    ax = axs[1][1]
    ax.hist(evals_enm['eigenvalue_0'][:950].to_numpy(), **hist_kwargs, 
        color=color_cycler[1])
    ax.set_ylabel("# modes per bin")
    ax.set_xlabel("$\lambda$ [?]")
    ax.set_title("ENM DOS | # bins = {}".format(no_bins))
    plt.show()

    plt.savefig(join_paths(output_dir, "evals.evals.pdf"), bbox_inches='tight')
    plt.savefig(join_paths(output_dir, "evals.evals.png"), bbox_inches='tight')


    fig, axs = plt.subplots(2,2, figsize=(6,6), constrained_layout=True)
    ax = axs[0][0]
    ax.scatter(evals_md[:plot_modes].index, evals_md[:plot_modes]['eigenvalue_0'],
        label='MD', color=color_cycler[0], s=5)
    ax.scatter(freq_enm[:plot_modes].index, freq_enm[:plot_modes]['eigenvalue_0'],
        label='ENM', color=color_cycler[1], s=5)
    ax.set_ylabel("$\lambda$ [$cm^{-1}$]")
    ax.set_xlabel("Mode number")
    ax.set_title("Eigenvalues")
    ax.legend(frameon=False)


    evals_ratio = evals_md['eigenvalue_0'] / freq_enm['eigenvalue_0']
    ax = axs[0][1]
    ax.scatter(evals_ratio[:plot_modes].index, evals_ratio[:plot_modes],
        color=color_cycler[2], s=5)
    ax.set_ylabel("$\lambda_{MD}/\lambda_{ENM}$")
    ax.set_xlabel("Mode number")
    ax.set_title("MD/ENM ratio")


    no_bins = 35
    hist_kwargs = dict( histtype='step', 
                        alpha=1, 
                        # color = colourWheel[j%len(colourWheel)],
                        # linestyle = lineStyles_hist[j%len(lineStyles_hist)],
                        # density=True,
                        # label = column_name, 
                        bins=no_bins)

    ax = axs[1][0]
    ax.hist(evals_md['eigenvalue_0'][:950].to_numpy(), **hist_kwargs, 
        color=color_cycler[0])
    ax.set_ylabel("# modes per bin")
    ax.set_xlabel("$\lambda$ [$cm^{-1}$]")
    ax.set_title("MD DOS | # bins = {}".format(no_bins))



    ax = axs[1][1]
    ax.hist(freq_enm['eigenvalue_0'][:950].to_numpy(), **hist_kwargs, 
        color=color_cycler[1])
    ax.set_ylabel("# modes per bin")
    ax.set_xlabel("$\lambda$ [$cm^{-1}$]")
    ax.set_title("ENM DOS | # bins = {}".format(no_bins))
    plt.show()

    plt.savefig(join_paths(output_dir, "evals.freq.pdf"), bbox_inches='tight')
    plt.savefig(join_paths(output_dir, "evals.freq.png"), bbox_inches='tight')

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
