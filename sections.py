# generic plot sections

# Todos:
# set min and max for contourf
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
            vv = v[-10:-1]
        else:
            vv = v[-10:-1][:]
        print('{}: {}...\nType:{}, dtype: {}\nSize: {}, Shape:{}, Dim: {}\n'.
            format(name, vv, type(v), v.dtype, v.size, v.shape, v.ndim))


def section(ncfile, parameters, xaxis, start, end, yscale,
    xinterp=24, yinterp=200, clevel=20, autoscale=True):

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

        if autoscale:
            zmin = np.min(z)
            zmax = np.max(z)
        else:
            zmin = nc.variables[var].valid_min
            zmax = nc.variables[var].valid_max
        p('zmin', zmin)
        p('zmax', zmax)
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
            #ax.invert_xaxis()
            ax.invert_yaxis()
            cmap = cm.get_cmap('jet', clevel)
            norm = cm.colors.Normalize(vmin=zmin, vmax=zmax)
            plt1 = ax.contourf(xi, yi, zi, levels=clevel, norm=norm,
                cmap=cmap, extend='both')
            cs = ax.contour(xi, yi, zi, plt1.levels, colors='black')
            ax.clabel(plt1, inline=True, fmt='%3.1f', fontsize=8)
            #plt1.set_clim(zmin, zmax)
            # add test for LONGITUDE and TIME 
            lat_formatter = LatitudeFormatter()
            ax.set_xticks(np.arange(np.round(np.min(x)),np.ceil(np.max(x))))
            ax.xaxis.set_major_formatter(lat_formatter)

        # Matplotlib 2 Subplots, 1 Colorbar
        # https://stackoverflow.com/questions/13784201/matplotlib-2-subplots-1-colorbar
        fig.colorbar(plt1, ax=fig.axes )
        ax.set_xlabel('{}'.format(nc.variables[xaxis].standard_name))
        ax.set_ylabel('{} [{}]'.format(nc.variables[yaxis].standard_name,
            nc.variables[yaxis].units),loc='bottom')
        plt.show()

if __name__ == '__main__':
    
    # ncfile = "netcdf/OS_PIRATA-FR30_CTD.nc"
    # section(ncfile, ['PRES','TEMP','PSAL'], 'LATITUDE', 17, 40, [[0,250], [250,2000]],autoscale=False)
    ncfile = "netcdf/OS_PIRATA-FR31_ADCP.nc"
    section(ncfile, ['DEPTH','EWCT', 'NSCT'], 'LATITUDE', 5, 28, [[0,250], [250,2200]], clevel=20, autoscale=False)
    # section(ncfile, ['DEPTH','EWCT', 'NSCT'], 'LATITUDE', 5, 28, [0,2200])
    # ncfile = "netcdf/OS_PIRATA-FR31_CTD.nc"
    # section(ncfile, ['PRES','TEMP'], 'LATITUDE', 5, 28, [[0,250], [250,2000]])
    # # section(ncfile, ['PRES','TEMP','PSAL','DOX2'], 'LATITUDE', 5, 28, [[0,250], [250,2000]])
    # ncfile = "netcdf/OS_PIRATA-FR31_XBT.nc"
    # section(ncfile, ['DEPTH','TEMP'], 'LATITUDE', 18, 28, [0,900])

