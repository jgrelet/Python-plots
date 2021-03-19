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
TUR3 = nc.variables['TUR3']

PROFILE = nc.variables['PROFILE']
STATION = PROFILE.shape[0]
CM = nc.cycle_mesure

# move subplot outside loop prevent: RuntimeWarning: More than 20 figures have been opened.


def plot_4 (TEMP,DEPTH,PRES,PSAL,VAR,FLU3,i):
    fig = plt.figure(figsize=(9,9), dpi=1200)
    for x in range(0,STATION):
    
        host = host_subplot(111, axes_class = AA.Axes)
        plt.subplots_adjust(bottom=0.20, top=0.80)

#Allow to copy y axis 3 times (this means we will have 4 different parameters on y)
        par1 = host.twiny() # instantiate a second axes that shares the same y-axis
        par2 = host.twiny() # instantiate a third axes that shares the same y-axis
        par3 = host.twiny() # instantiate a fourth axes that shares the same y-axis

#Allows you to choose the location of additional axes
        new_fixed_axis = par2.get_grid_helper().new_fixed_axis
        new_fixed_axis = par3.get_grid_helper().new_fixed_axis
        par2.axis["top"] = new_fixed_axis(loc="top",axes=par2,offset=(0, 30))
        par3.axis["bottom"] = new_fixed_axis(loc="bottom",axes=par3,offset=(0,-30))
                                         
        par1.axis["top"].toggle(all=True)
        par2.axis["top"].toggle(all=True)
        par3.axis["bottom"].toggle(all=True)

    # Use the data that we need
        temp = TEMP[x,:]
        depth = DEPTH[x,:]
        pres = PRES[x,:]
        psal = PSAL[x,:]
        flu3 = FLU3[x,:]
        var = VAR[x,:]

        host.set_ylabel("Pressure, Digiquartz [db]")
        host.set_xlabel("Temperature [ITS-90, deg C]")
        par1.set_xlabel("Salinity, Pratical [PSU]")
        par2.set_xlabel("Fluorescence, WET Labs ECO-EFLD/FL [mg/m^3]")
        par3.set_xlabel('{} [{}]'.format(VAR.long_name, VAR.units))

    
        p1, = host.plot(temp, pres)
        p2, = par1.plot(psal, pres)
        p3, = par2.plot(flu3, pres)
        p4, = par3.plot(var, pres)

        host.invert_yaxis()
    #put a different color for each plot
        host.axis["bottom"].label.set_color(p1.get_color())
        par1.axis["top"].label.set_color(p2.get_color())
        par2.axis["top"].label.set_color(p3.get_color())
        par3.axis["bottom"].label.set_color(p4.get_color())

        fig.text(0.4, 0.9, '{},  dfr300{}'.format(CM, PROFILE[x]), va='center', rotation='horizontal')
    
    #plt.title('{},  dfr300{}'.format(CM, PROFILE[x]))
        figname = 'dfr30{:03d}-{}.png'.format(PROFILE[x],i)
        dest = os.path.join(path, figname)
        plt.savefig(dest,format='png', dpi=1200)
        print('Printing: ', dest)
        #plt.show()
        plt.draw()
        plt.clf()
    plt.close(fig)
i=0
VAR = [FLU2,DOX2,TUR3]
for k in VAR :
    plot_4 (TEMP,DEPTH,PRES,PSAL,k,FLU3,i)
    i=i+1
print('DONE')
