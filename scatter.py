from netCDF4 import Dataset
import numpy as np
#import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
import os



# in batch mode, without display
#matplotlib.use('Agg')  

file = 'netcdf/OS_PIRATA-FR31_TSG.nc'
ncpath = '.'
path = 'plots'

ncfile = os.path.join(ncpath, file)
nc = Dataset(ncfile, mode='r')

SSPS = nc.variables['SSPS']
SSTP = nc.variables['SSTP']
TIME = nc.variables['TIME']
LATITUDE = nc.variables['LATITUDE']
LONGITUDE = nc.variables['LONGITUDE']
CM = nc.cycle_mesure

# move subplot outside loop prevent: RuntimeWarning: More than 20 figures have been opened.

fig = plt.figure(figsize=(6, 12))
gs = gridspec.GridSpec(2,1)
ax1 = plt.subplot(gs[0], projection=ccrs.PlateCarree())
ax1.set_extent([-40, 20, -30, 50], crs=ccrs.PlateCarree())
ax1.coastlines(resolution='auto', color='k')
ax1.gridlines(color='lightgrey', linestyle='-', draw_labels=True)

im1 = ax1.scatter(LONGITUDE[:], LATITUDE[:], c=SSPS[:], s=30, cmap='jet', vmin=32, vmax=37, transform=ccrs.PlateCarree())
fig.colorbar(im1, ax=ax1, orientation='vertical')
ax1.set(xlabel='{} '.format(LONGITUDE.standard_name), ylabel='{} '.format(LATITUDE.standard_name),
        title='{} - {}'.format(CM, SSPS.long_name))

ax2 = plt.subplot(gs[1], projection=ccrs.PlateCarree())
ax2.set_extent([-40, 20, -30, 50], crs=ccrs.PlateCarree())
ax2.coastlines(resolution='auto', color='k')
ax2.gridlines(color='lightgrey', linestyle='-', draw_labels=True)

im2 = ax2.scatter(LONGITUDE[:], LATITUDE[:], c=SSTP[:], s=30, cmap='jet', vmin=21, vmax=32, transform=ccrs.PlateCarree())
fig.colorbar(im2, ax=ax2, orientation='vertical')
ax2.set(xlabel='{} '.format(LONGITUDE.standard_name), ylabel='{} '.format(LATITUDE.standard_name),
        title='{} - {}'.format(CM, SSPS.long_name))

figname = '{}_TSG_COLCOR_SCATTER.png'.format(CM)
dest = os.path.join(path, figname)
fig.savefig(dest)
print('Printing: ', dest)

plt.show()
plt.cla()
