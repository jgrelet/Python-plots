from netCDF4 import Dataset
import numpy as np
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.interpolate import interp1d

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

def nearest_interp(xi, x, y):
    idx = np.abs(x - xi[:,None])
    return y[idx.argmin(axis=1)]
    
# move subplot outside loop prevent: RuntimeWarning: More than 20 figures have been opened.
fig, ax = plt.subplots()
for x in range(0,STATION) :
    temp = TEMP[x,:]
    depth = DEPTH[x,:]

    maxt = max(temp)
    mint = min(temp)
    xvals = np.linspace(maxt, mint, 100)
    #f = interp1d(temp,depth)
    #yinterp = f(xvals)
    yinterp = nearest_interp(xvals,temp,depth)
    plt.plot(temp, depth, 'o',xvals, yinterp, '-x')

    figname = '{}-{:03d}_XBT.png'.format(CM, PROFILE[x])
    dest = os.path.join(path, figname)
    fig.savefig(dest)
    print('Printing: ', dest)
    #plt.show()
    plt.cla()
plt.close(fig)
print('Done.')

