from netCDF4 import Dataset
import numpy as np
#import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os



# in batch mode, without display
#matplotlib.use('Agg')  

file = 'netcdf/OS_PIRATA-FR29_TSG.nc'
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

fig, ax = plt.subplots(2, 1, figsize=(6, 12))
fig.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.3)

im1 = ax[0].scatter(LONGITUDE[:], LATITUDE[:], c=SSPS[:], s=30, cmap='jet', vmin=32, vmax=37)
fig.colorbar(im1, ax=ax[0], orientation='vertical')
ax[0].set(xlabel='{} '.format(LONGITUDE.standard_name), ylabel='{} '.format(LATITUDE.standard_name),
        title='{} - {}'.format(CM, SSPS.long_name))
ax[0].grid()

im2 = ax[1].scatter(LONGITUDE[:], LATITUDE[:], c=SSTP[:], s=30, cmap='jet', vmin=21, vmax=32)
fig.colorbar(im2, ax=ax[1], orientation='vertical')
ax[1].set(xlabel='{} '.format(LONGITUDE.standard_name), ylabel='{} '.format(LATITUDE.standard_name),
        title='{} - {}'.format(CM, SSPS.long_name))
ax[1].grid()

figname = '{}_TSG_COLCOR_SCATTER.png'.format(CM)
dest = os.path.join(path, figname)
fig.savefig(dest)
print('Printing: ', dest)

plt.show()
plt.cla()

#im1 = cs[0, 0].contourf(lon,lat,result1, np.linspace(20,30,21), extend='both', cmap=cm.jet)
#cs[0, 0].set_title('VOTEMPER OBS  Saison ' + list1[x],fontsize=10)
#fig.colorbar(im1, ax=cs[0, 0], orientation='horizontal')

######################################df = pd.DataFrame(np.transpose([LONGITUDE[:], LATITUDE[:], SSPS[:]]), columns=['LONGITUDE', 'LATITUDE', 'SSPS'])  #, columns=['Longitudes','Latitudes']
######################################ax = df.plot.scatter(x='LONGITUDE', y='LATITUDE', c='SSPS', colormap='viridis')
######################################ax.set_ylim(bottom=-12,top=19)
######################################ax.set_xlim(left=-30, right=15)
######################################print(df)

#A = np.array((LONGITUDE, LATITUDE, SSTP), dtype=float)
#print(SSPS[36])
#print(A)
#plt.plot(LATITUDE,LONGITUDE,A)
