# generic plot sections

# Todos:
# test if last profile is in file (line 50)
# write profile number on top axes

import numpy as np
#import xarray as xr
from netCDF4 import Dataset
#import pandas as pd
from scipy.interpolate import (interp1d, griddata)
import matplotlib.pyplot as plt
from matplotlib import (ticker, cm, gridspec)
import matplotlib.dates as mdates
from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter,
                                LatitudeLocator)


def p(name, v):
    if isinstance(v, (int, float, list)):
        print('{}: {}'.format(name, v))
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
            xinterp=20, yinterp=200, clevels=20, autoscale=True, marks=True):

    # Read ctd data
    nc = Dataset(ncfile, "r")

    # Y variable, PRES or DEPTH, must be first, add test
    yaxis = parameters[0]
    yscale = np.array(yscale)
    pmax = np.max(yscale)

    # find the profile index
    profiles = nc.variables['PROFILE'][:].tolist()
    start = profiles.index(start)
    end = profiles.index(end) + 1
    nbxi = end - start

    if xinterp > end - start:
        xinterp = end - start
    # add test for LONGITUDE and TIME
    if xaxis == 'LATITUDE':
        x_formatter = LatitudeFormatter()
    elif xaxis == 'LONGITUDE':
        x_formatter = LongitudeFormatter()
    else:
        x_formatter = mdates.DateFormatter('%m/%d')

    # for each physical parameter
    for k in range(1, len(parameters)):
        # extract data from netcdf variables
        var = parameters[k]
        x = nc.variables[xaxis][start:end]
        y = nc.variables[yaxis][start:end][:]
        # find index of the max value given by yscale
        r, c = np.where(y == pmax)
        #y = y[:][0:columns[0]]
        y = nc.variables[yaxis][start:end,:c[0]]
        z = nc.variables[var][start:end,:c[0]]
        print(y.shape, z.shape)
        xi = np.linspace(x[0], x[-1], nbxi)
        yi = np.linspace(np.round(np.amin(y)), np.ceil(np.amax(y)), yinterp)

        # contourf indeed works a bit differently than other ScalarMappables.
        # If you specify the number of levels (20 in this case) it will take
        # them between the minimum and maximum data (approximately).
        # If you want to have n levels between two specific values vmin and vmax
        # you would need to supply those to the contouring function.
        if isinstance(autoscale, list):
            zmin = autoscale[0]
            zmax = autoscale[1]
        else:
            if autoscale:
                zmin = np.min(z)
                zmax = np.max(z)
            else:
                zmin = nc.variables[var].valid_min
                zmax = nc.variables[var].valid_max
        levels = np.linspace(zmin, zmax, clevels+1)
        sublevels = np.linspace(zmin, zmax, round(clevels/5)+1)

        # verticale interpolation
        zi = np.array(([]))
        for i in range(0, len(z)):
            # convert fill_value from Dataset to numpy
            yy = np.ma.masked_array(y[i]).filled(np.nan)
            zz = np.ma.masked_array(z[i]).filled(np.nan)
            Z = np.interp(yi, yy, zz)
            zi = np.append(zi, Z, axis=0)
        zi = zi.reshape(nbxi, yinterp)

        xx, yy = np.meshgrid(xi, yi, indexing='ij')
        xi = np.linspace(x[0], x[-1], xinterp)
        zi = griddata((xx.ravel(), yy.ravel()), zi.ravel(),
                      (xi[None, :], yi[:, None]))
        # Specifies the geometry of the grid that a subplot will be placed
        fig = plt.figure(figsize=(8, 8))
        ratio = [1, yscale.ndim] if yscale.ndim == 2 else None
        gs = gridspec.GridSpec(yscale.ndim, 1, height_ratios=ratio)

        # loop over vertical range, ex: [0,2000] or [[0,250], [250,2000]]
        for i, ax in enumerate(gs):
            ax = plt.subplot(gs[i])
            if i == 0:
                ax.set_title('{}\n{}, {} [{}]'.format(nc.cycle_mesure, var,
                                                      nc.variables[var].long_name, nc.variables[var].units))
            ax.set_ylim(yscale[:]) if yscale.ndim == 1 else ax.set_ylim(
                yscale[i])
            ax.invert_yaxis()
            # plot contour(s)
            plt1 = ax.contourf(xi, yi, zi, levels=levels, vmin=zmin, vmax=zmax,
                               cmap='jet', extend='neither')
            cs = ax.contour(xi, yi, zi, plt1.levels,
                            colors='black', linewidths=0.5)
            cs = ax.contour(xi, yi, zi, sublevels,
                            colors='black', linewidths=1.5)
            ax.clabel(cs, inline=True, fmt='%3.1f', fontsize=8)
            ax.set_xticks(np.arange(np.round(np.min(x)), np.ceil(np.max(x))),minor=True)
            ax.xaxis.set_major_formatter(x_formatter)
            ax2 = ax.twiny()
            ax2.spines["top"].set_position(("axes", 1.0))
            print(profiles[start:end])
            #ax2.set_xlim(33,45)
            #ax2.set_xticks(ax.get_xticks())
            ax2.set_xticklabels(profiles[start:end])
            # ax2.xaxis.set_major_formatter(profiles[start:end])

        # Matplotlib 2 Subplots, 1 Colorbar
        # https://stackoverflow.com/questions/13784201/matplotlib-2-subplots-1-colorbar
        plt.colorbar(plt1, ax=fig.axes)
        ax.set_xlabel('{}'.format(nc.variables[xaxis].standard_name))
        ylabel = '{} [{}]'.format(nc.variables[yaxis].standard_name,
                                  nc.variables[yaxis].units)
        # display common y label with text instead of ax.set_ylabel
        fig.text(0.04, 0.5, ylabel, va='center',
                 ha='center', rotation='vertical')
        plt.show()


if __name__ == '__main__':

    ncfile = "netcdf/OS_PIRATA-FR31_CTD.nc"
    # section(ncfile, ['PRES', 'TEMP'], 'LATITUDE', 5, 28, [
    #    [0, 250], [250, 2000]], xinterp=20, yinterp=200, clevels=30, autoscale=[0, 30])
    section(ncfile, ['PRES', 'TEMP'], 'TIME', 33, 49,
        [0, 200], xinterp=16, yinterp=50, clevels=30, autoscale=[0, 30])
    # section(ncfile, ['PRES', 'TEMP'], 'LATITUDE', 5, 28, [
    #         [0, 250], [250, 2000]], xinterp=20, yinterp=200, clevels=30, autoscale=[0, 30])
    # # section(ncfile, ['PRES','PSAL'], 'LATITUDE', 5, 28, [[0,250], [250,2000]],clevels=15,autoscale=[34,37])
    # section(ncfile, ['PRES','DOX2'], 'LATITUDE', 5, 28, [[0,250], [200,2000]],clevels=22,autoscale=[0,220])
    # section(ncfile, ['PRES','TEMP'], 'LATITUDE', 5, 28, [0,2000],clevels=30,autoscale=[0,30])

    ncfile = "netcdf/OS_PIRATA-FR31_ADCP.nc"
    # section(ncfile, ['DEPTH', 'EWCT'], 'LATITUDE', 5, 28, [[0, 250], [
    #         250, 2200]], xinterp=24, yinterp=200, clevels=30, autoscale=False)
    # section(ncfile, ['DEPTH','EWCT', 'NSCT'], 'LATITUDE', 5, 28, [0,2200])
    # section(ncfile, ['DEPTH', 'EWCT'], 'TIME', 33, 45, [[0, 200], [200, 500]],
    #        xinterp=20, yinterp=100, clevels=15, autoscale=[-150, 150])

    ncfile = "netcdf/OS_PIRATA-FR31_XBT.nc"
    # section(ncfile, ['DEPTH', 'TEMP'], 'LATITUDE', 29, 36, [
    #         [0, 250], [250, 900]], clevels=30, autoscale=[0, 30])
    # section(ncfile, ['DEPTH', 'TEMP'], 'LATITUDE', 29,
    #         36, [0, 900], clevels=30, autoscale=[0, 30])
    # section(ncfile, ['DEPTH', 'TEMP'], 'LONGITUDE', 39,
    #        46, [0, 900], clevels=30, autoscale=[0, 30])
