# generic plot sections

# Todos:
# add contour(s) with thin every label and large every five
# add intrument type: CTD, XBT, ADCP, ...
# center xlabel over 2 subplots
# interpolate xaxis
# test for LONGITUDE and TIME AXIS

import numpy as np
#import xarray as xr
from netCDF4 import Dataset
#import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib import (ticker, cm)
from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter,
                                LatitudeLocator)

def p(name, v):
    if isinstance(v, (int,float)):
        print('{}: {}'.format(name,v)) 
    else:
        if v.ndim == 0:
            vv = v
        elif v.ndim == 1:
            vv = v[1:10]
        else:
            vv = v[1:10][:]
        print('{}: {}...\nType:{}, dtype: {}\nSize: {}, Shape:{}, Dim: {}\n'.
            format(name, vv, type(v), v.dtype, v.size, v.shape, v.ndim))


def section(ncfile, parameters, xaxis, start, end, yscale,
    xinterp=24, yinterp=200, clevels=20, autoscale=True):

    # Read ctd data
    nc = Dataset(ncfile, "r")

    # Y variable, PRES or DEPTH, must be first, add test
    yaxis = parameters[0]
    yscale = np.array(yscale)

    # find the profile index
    profiles = nc.variables['PROFILE'][:].tolist()
    start = profiles.index(start)
    end = profiles.index(end) + 1
    if xinterp > end -start:
        xinterp = end - start
    yinterp = 200

    for k in range(1, len(parameters)):
        var   = parameters[k]
        x = nc.variables[xaxis][start:end]
        y = nc.variables[yaxis][start:end][:]
        z = nc.variables[var][start:end][:]
        xi = np.linspace(x[0], x[-1], xinterp)
        yi = np.linspace(np.round(np.amin(y)), np.ceil(np.amax(y)), yinterp)
        
        # contourf indeed works a bit differently than other ScalarMappables.
        # If you specify the number of levels (20 in this case) it will take 
        # them between the minimum and maximum data (approximately). 
        # If you want to have n levels between two specific values vmin and vmax 
        # you would need to supply those to the contouring function.
        if isinstance(autoscale,list):
            zmin = autoscale[0]
            zmax = autoscale[1]
        else:
            if autoscale:
                zmin = np.min(z)
                zmax = np.max(z)
            else:
                zmin = nc.variables[var].valid_min
                zmax = nc.variables[var].valid_max
        levels = np.linspace(zmin,zmax,clevels+1)
        sublevels = np.linspace(zmin,zmax,round(clevels/5)+1)

        # interpolate
        zi = np.array(([]))
        for i in range(0, len(z)):
            # convert fill_value from Dataset to numpy
            yy = np.ma.masked_array(y[i]).filled(np.nan)
            zz = np.ma.masked_array(z[i]).filled(np.nan)
            Z = np.interp(yi, yy, zz)
            zi = np.append(zi, Z, axis=0)
        zi = zi.reshape(xinterp, yinterp).transpose()

        # plot contour(s)
        fig, ax = plt.subplots(yscale.ndim,1, sharex=True, squeeze=False)
        fig.axes[0].set_title('{}\n{}, {} [{}]'.format(nc.cycle_mesure, var, 
            nc.variables[var].long_name, nc.variables[var].units))
        # loop over vertical range, ex: [0,2000] or [[0,250], [250,2000]]
        for i, ax in enumerate(fig.axes):
            if yscale.ndim == 1:
                ax.set_ylim(yscale[:])
            else:
                ax.set_ylim(yscale[i])
            ax.invert_yaxis()
            plt1 = ax.contourf(xi, yi, zi, levels=levels, vmin=zmin, vmax=zmax,
                cmap='jet', extend='neither')
            cs = ax.contour(xi, yi, zi, plt1.levels, colors='black', linewidths=0.5)
            cs = ax.contour(xi, yi, zi, sublevels, colors='black', linewidths=1.5)
            ax.clabel(cs, inline=True, fmt='%3.1f', fontsize=8)
            # add test for LONGITUDE and TIME 
            lat_formatter = LatitudeFormatter()
            ax.set_xticks(np.arange(np.round(np.min(x)),np.ceil(np.max(x))))
            ax.xaxis.set_major_formatter(lat_formatter)

        # Matplotlib 2 Subplots, 1 Colorbar
        # https://stackoverflow.com/questions/13784201/matplotlib-2-subplots-1-colorbar
        plt.colorbar(plt1, ax=fig.axes)
        ax.set_xlabel('{}'.format(nc.variables[xaxis].standard_name))
        ax.set_ylabel('{} [{}]'.format(nc.variables[yaxis].standard_name,
            nc.variables[yaxis].units),loc='bottom')
        plt.show()

if __name__ == '__main__':
    
    ncfile = "netcdf/OS_PIRATA-FR31_CTD.nc"
    section(ncfile, ['PRES','TEMP'], 'LATITUDE', 5, 28, [[0,250], [250,2000]],clevels=30,autoscale=[0,30])
    section(ncfile, ['PRES','PSAL'], 'LATITUDE', 5, 28, [[0,250], [250,2000]],clevels=15,autoscale=[34,37])
    section(ncfile, ['PRES','DOX2'], 'LATITUDE', 5, 28, [[0,250], [200,2000]],clevels=22,autoscale=[0,220])
    section(ncfile, ['PRES','TEMP'], 'LATITUDE', 5, 28, [0,2000],clevels=30,autoscale=[0,30])
    # ncfile = "netcdf/OS_PIRATA-FR31_ADCP.nc"
    # section(ncfile, ['DEPTH','EWCT'], 'LATITUDE', 5, 28, [[0,250], [250,2200]], clevels=30, autoscale=False)
    # section(ncfile, ['DEPTH','EWCT', 'NSCT'], 'LATITUDE', 5, 28, [0,2200])
    ncfile = "netcdf/OS_PIRATA-FR31_XBT.nc"
    section(ncfile, ['DEPTH','TEMP'], 'LATITUDE', 29, 36, [[0,250], [250,900]],clevels=30,autoscale=[0,30])
 
