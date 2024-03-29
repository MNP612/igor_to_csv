from igor import binarywave
import numpy as np
import pandas as pd
import glob
import os

from matplotlib import pyplot as plt

# "single" for single file
# "all" to transform all files in a folder
TRANSFORM = 'all'

PATH = '/Users/Marvin/Desktop/'
EXTENSION = '.ibw'
SAVE_PATH = '/Users/Marvin/Desktop/'

FILE = 'Apr30_0005P2p' # use only for "single" mode

INTEGRATE = True # choose if you want to keep all sweeps (False) or to average over all sweeps (True)
PLOT = False # choose if you want to plot the data for a quick look (image will not be saved)

###-------------------------------###


def read(PATH, EXTENSION, FILE):
    binary = binarywave.load(PATH + FILE + EXTENSION)

    energy_start = round(binary['wave']['wave_header']['sfB'][0],2)
    energy_step = round(binary['wave']['wave_header']['sfA'][0],2)
    n_points = round(binary['wave']['wave_header']['nDim'][0],2)
    energy_stop = energy_start + (energy_step * (n_points - 1))

    energy_axis = np.linspace(energy_start, energy_stop, n_points)

    wave = binary['wave']['wData']
    intensity = np.sum(wave,axis=1).T
    if INTEGRATE:
        n_sweeps = len(intensity)
        intensity = np.sum(intensity, axis=0) / n_sweeps

    if pd.DataFrame(intensity).shape[1] > 1:
        df = pd.DataFrame(intensity).T
    else:
        df = pd.DataFrame(intensity)

    df['kinetic_energy'] = energy_axis
    df['note'] = ''
    df['note'][0] = binary['wave']['note']

    if PLOT:
        plt.plot(energy_axis,df[0])
        plt.show()

    return df

def save(df, file, SAVE_PATH):
    df.to_csv(SAVE_PATH + file + '.csv',index=False)

def main():
    if TRANSFORM == 'single':
        df = read(PATH, EXTENSION, FILE)
        save(df, FILE, SAVE_PATH)
    elif TRANSFORM == 'all':
        file_list_full = glob.glob(PATH + '*' + EXTENSION)
        file_list_basenames = [os.path.basename(f)[:-4] for f in file_list_full]
        for file in file_list_basenames:
            try:
                df = read(PATH, EXTENSION, file)
                save(df, file, SAVE_PATH)
            except:
                print('could not transform ' + file)
    else:
        raise TypeError('Expected input: "sf" (single file) or "folder"')

main()
