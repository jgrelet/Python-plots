from netCDF4 import Dataset
import numpy as np
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os

# in batch mode, without display
matplotlib.use('Agg')  

file = 'OS_PIRATA-FR30_XBT.nc'
ncpath = 'netcdf'
path = 'plots'
#ncpath = '.'
#path = 'png'

ncfile = os.path.join(ncpath, file)
nc = Dataset(ncfile, mode='r')

TEMP = nc.variables['TEMP']
DEPTH = nc.variables['DEPTH']
PROFILE = nc.variables['PROFILE']
STATION = PROFILE.shape[0]
CM = nc.cycle_mesure

# move subplot outside loop prevent: RuntimeWarning: More than 20 figures have been opened.
fig, ax = plt.subplots()

for x in range(0,STATION):
    temp = TEMP[x,:]
    depth = DEPTH[x,:]

   
    ax.plot(temp, depth)
    ax.invert_yaxis()
    ax.set(xlabel='{} ({})'.format(TEMP.long_name, TEMP.units), ylabel='{} ({})'.format(DEPTH.long_name,DEPTH.units),
           title='{} - XBT Sippican profile n° {}'.format(CM, PROFILE[x]))
    ax.axis('auto')
    ax.set_ylim(top=0)
    ax.set_xlim(left=0, right=32)
    ax.grid()

    figname = '{}-{:03d}_XBT.png'.format(CM, PROFILE[x])
    dest = os.path.join(path, figname)
    fig.savefig(dest)
    print('Printing: ', dest)
    #plt.show()
    plt.cla()
plt.close(fig)
print('Done.')
