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
FLU3 = nc.variables['FLU3']
FLU2 = nc.variables['FLU2']
DOX2 = nc.variables['DOX2']


PROFILE = nc.variables['PROFILE']
STATION = PROFILE.shape[0]
CM = nc.cycle_mesure

# move subplot outside loop prevent: RuntimeWarning: More than 20 figures have been opened.
fig = plt.figure()

for x in range(0,STATION):
    host = host_subplot(111, axes_class = AA.Axes)
    plt.subplots_adjust(bottom=0.20, top=0.80)

    par1 = host.twiny()
    par2 = host.twiny()
    par3 = host.twiny()

    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    new_fixed_axis = par3.get_grid_helper().new_fixed_axis
    par2.axis["top"] = new_fixed_axis(loc="top",axes=par2,offset=(0, 30))
    par3.axis["bottom"] = new_fixed_axis(loc="bottom",axes=par3,offset=(0,-30))
                                         
    par1.axis["top"].toggle(all=True)
    par2.axis["top"].toggle(all=True)
    par3.axis["bottom"].toggle(all=True)
    
    temp = TEMP[x,:]
    depth = DEPTH[x,:]
    pres = PRES[x,:]
    psal = PSAL[x,:]
    flu3 = FLU3[x,:]
    flu2 = FLU2[x,:]
    dox2 = DOX2[x,:]

    host.set_ylabel("Pressure, Digiquartz [db]")
    host.set_xlabel("Temperature [ITS-90, deg C]")
    par1.set_xlabel("Salinity, Pratical [PSU]")
    par2.set_xlabel("Fluorescence, WET Labs ECO-EFLD/FL [mg/m^3]")
    par3.set_xlabel("Oxygen, SBE43 [umol/kg]")

    
    #host.set_title('{} - dfr3000{}'.format(CM, PROFILE[x]))
    
    p1, = host.plot(temp, pres)
    p2, = par1.plot(psal, pres)
    p3, = par2.plot(flu3, pres)
    p4, = par3.plot(dox2, pres)

    host.invert_yaxis()
    
    host.axis["bottom"].label.set_color(p1.get_color())
    par1.axis["top"].label.set_color(p2.get_color())
    par2.axis["top"].label.set_color(p3.get_color())
    par3.axis["bottom"].label.set_color(p4.get_color())

    figname = '{}-{:03d}_CTD.png'.format(CM, PROFILE[x])
    dest = os.path.join(path, figname)
    plt.savefig(dest)
    print('Printing: ', dest)
    #plt.show()
    plt.draw()
    plt.clf()
plt.close(fig)
print('Done.')
