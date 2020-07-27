from netCDF4 import Dataset
import matplotlib
import numpy as np
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

import matplotlib.pyplot as plt
import os

# in batch mode, without display
matplotlib.use('Agg')  

file = 'OS_PIRATA-FR30_top_CTD.nc'
ncpath = 'netcdf'
path = 'plots'
#ncpath = '.'
#path = 'png'

ncfile = os.path.join(ncpath, file)
nc = Dataset(ncfile, mode='r')

TEMP = nc.variables['TEMP']
DEPTH = nc.variables['DEPTH']
PRES = nc.variables['PRES']
PSAL = nc.variables['PSAL']
PROFILE = nc.variables['PROFILE']
STATION = PROFILE.shape[0]
CM = nc.cycle_mesure

# move subplot outside loop prevent: RuntimeWarning: More than 20 figures have been opened.
fig, ax = plt.subplots()
for x in range(0,STATION):
    temp = TEMP[x,:]
    depth = DEPTH[x,:]
    pres = PRES[x,:]
    psal = PSAL[x,:]

    ax.plot(psal,pres)
    ax.invert_yaxis()
    
    ax.set_ylabel('{} ({})'.format(PRES.long_name,PRES.units))
    ax.set_xlabel('{} ({})'.format(PSAL.long_name, PSAL.units))

    ax.set_title('{} - CTD  profile n° {}'.format(CM, PROFILE[x]))

    ax.axis('auto')
   
    ax.grid()

    figname = '{}-{:03d}_CTD.png'.format(CM, PROFILE[x])
    dest = os.path.join(path, figname)
    fig.savefig(dest)
    print('Printing: ', dest)
    #plt.show()
    plt.cla()
plt.close(fig)
print('Done.')
