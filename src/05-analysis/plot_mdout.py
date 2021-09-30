# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
""" Plot wrangled mdout summary data

    This script plots MD out processed data.

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
    summary_data = pd.read_csv(join_paths(input_dir, "summary_mdout.csv"), index_col='time')
    color_cycler = plt.rcParams['axes.prop_cycle'].by_key()['color']

    fig = plt.figure(constrained_layout=True, figsize=(10,5))

    subfigs = fig.subfigures(1, 2)

    subfigsnest = subfigs[0].subfigures(2, 1)

    gs = subfigsnest[0].add_gridspec(3, hspace=0)
    axsnest0 = gs.subplots(sharex=True)
    # axsnest0 = subfigsnest[0].subplots(3, 1, sharex=True)
    subplot_axs = axsnest0
    subplot_axs[0].plot(summary_data.index, summary_data['eptot'], color=color_cycler[0])
    subplot_axs[1].plot(summary_data.index, summary_data['ektot'], color=color_cycler[1])
    subplot_axs[2].plot(summary_data.index, summary_data['etot'], color=color_cycler[2])
    # subfigsnest[0].supylabel("Energy [$kcal\:mol^{-1}$]")

    axsnest1 = subfigsnest[1].subplots(2, 1, sharex=True)
    subplot_axs = axsnest1

    ax = subplot_axs[0]
    ax.plot(summary_data.index, summary_data['temp'], color=color_cycler[4])
    ax.set_xlabel("")
    ax.set_ylabel("Temp [K]")

    ax = subplot_axs[1]
    ax.plot(summary_data.index, summary_data['pres'], color=color_cycler[5])
    ax.set_xlabel("Time [ps]")
    ax.set_ylabel("Pres\n[$kcal\:mol^{-1}\:\AA^{-1}$]")    

    axsRight = subfigs[1].subplots(3, 1, sharex=True)
    ax = axsRight[0]
    ax.plot(summary_data.index, summary_data['volume'], color=color_cycler[6])
    ax.set_xlabel("")
    ax.set_ylabel("Volume [$\AA^{-3}$]")

    ax = axsRight[1]
    ax.plot(summary_data.index, summary_data['density'], color=color_cycler[7])
    ax.set_xlabel("")
    ax.set_ylabel("Density [$g\:cm^{-3}$]")

    ax = axsRight[2]
    ax.plot(summary_data.index, summary_data['rmsd'], color=color_cycler[8])
    ax.set_xlabel("Time [ps]")
    ax.set_ylabel("RMSD [$\AA$]")

    plt.savefig(join_paths(output_dir, "summary_mdout.pdf"), bbox_inches='tight')
    plt.savefig(join_paths(output_dir, "summary_mdout.png"), bbox_inches='tight')


    plt.show()


    # _, axs = plt.subplots(3,2, figsize=(12,9), constrained_layout=True, sharex=True)

    # ax = axs[0][0]
    # gs = ax.add_gridspec(3, hspace=0)
    # subplot_axs= gs.subplots(sharex=True)
    # subplot_axs[0].plot(summary_data.index, summary_data['eptot'], color=color_cycler[0])
    # subplot_axs[1].plot(summary_data.index, summary_data['ektot'], color=color_cycler[1])
    # subplot_axs[2].plot(summary_data.index, summary_data['etot'], color=color_cycler[2])

    # # Hide x labels and tick labels for all but bottom plot.
    # for subplot_ax in subplot_axs:
    #     subplot_ax.label_outer()

    # ax.plot(summary_data.index, summary_data['eptot'], color=color_cycler[0])
    # ax.set_ylabel("Potential energy [$kcal\:mol^{-1}$]")
    # ax.set_xlabel("")

    # ax = axs[1][0]
    # ax.plot(summary_data.index, summary_data['temp'], color=color_cycler[4])
    # ax.set_xlabel("")
    # ax.set_ylabel("Temp [K]")

    # ax = axs[2][0]
    # ax.plot(summary_data.index, summary_data['pres'], color=color_cycler[5])
    # ax.set_xlabel("Time [ps]")
    # ax.set_ylabel("Pres ($kcal\:mol^{-1}\:\AA^{-1}$)")

    # ax = axs[0][1]
    # ax.plot(summary_data.index, summary_data['volume'], color=color_cycler[6])
    # ax.set_xlabel("")
    # ax.set_ylabel("Volume ($\AA^{-3}$)")

    # ax = axs[1][1]
    # ax.plot(summary_data.index, summary_data['density'], color=color_cycler[7])
    # ax.set_xlabel("")
    # ax.set_ylabel("Density ($g\:cm^{-3}$)")

    # plt.savefig(join_paths(output_dir, "summary_mdout.pdf"), bbox_inches='tight')

    
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



