#!/usr/bin/env python
"""
This class allows you to plot any type of data from an OceanSites
files, either CTD, XBT or LADCP (profiles and sections)

Todos:
- display the figure on screen (command line option)
"""
from netCDF4 import Dataset
import logging
import argparse
import textwrap
import os
import os.path
import sys
import re
import toml
import json
import ast
from datetime import datetime
import julian
import math
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.dates as mdates
from matplotlib import (ticker, cm, gridspec)
from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter,
                                LatitudeLocator)
import cartopy.crs as ccrs

JULIAN_1950 = 33282
JULIAN_1970 = 2440587.5
DEGREE = u"\u00B0"  # u"\N{DEGREE SIGN}"


class Store_as_array(argparse._StoreAction):
    def __call__(self, parser, namespace, values, option_string=None):
        values = np.array(values)
        if len(values) == 4:
            values = np.array(values).reshape(2, 2)
        return super().__call__(parser, namespace, values, option_string)


def processArgs():
    parser = argparse.ArgumentParser(
        description='This program read CTD NetCDF file and plot parameters vs PRES',
        usage='\npython plots.py -t <TYPE> -s (SECTIONS) <OPTIONS> ... | -p (PROFILES) <OPTIONS> ...\n'
        'PROFILES:\n'
        'python plots.py netcdf/OS_PIRATA-FR31_CTD.nc -t CTD -p -k PRES TEMP PSAL DOX2 FLU2 -g -c k- b- r- m- g-\n'
        'python plots.py netcdf/OS_AMAZOMIX_CTD.nc -t CTD -p -k PRES TEMP PSAL DOX2 FLU2 -g -c k- b- r- m- g- -g -o plots/AMAZOMIX\n'
        'python plots.py netcdf/OS_PIRATA-FR31_XBT.nc -t XBT -p -k DEPTH TEMP DENS SVEL -c k- b- k- g- -g\n'
        'python plots.py netcdf/OS_PIRATA-FR31_ADCP.nc -t ADCP -p -k DEPTH EWCT NSCT -c k- r- b- -g\n'
        'SECTIONS:\n'
        'python plots.py netcdf/OS_PIRATA-FR31_CTD.nc -t CTD -s -k PRES TEMP -l 5 28 --xaxis LATITUDE --yscale 0 250 250 2000 --xinterp 24 --yinterp 200 --clevels=30 --autoscale 0 30\n'
        'python plots.py netcdf/OS_PIRATA-FR31_CTD.nc -t CTD -s --append 1N-10W_10S_10W -k PRES PSAL -l 5 28 --xaxis LATITUDE --yscale 0 250 250 2000 --xinterp 24 --yinterp 100 --clevels=15 --autoscale 34 37\n'
        'python plots.py netcdf/OS_PIRATA-FR31_ADCP.nc -t ADCP -s --append point-fixe_0-10W -k DEPTH EWCT NSCT -l 33 45 --xaxis TIME --yscale 0 500 --xinterp 20 --yinterp 50 --clevels 15 --autoscale -150 150\n'
        'python plots.py netcdf/OS_PIRATA-FR31_XBT.nc -t XBT -s -k DEPTH TEMP -xaxis LATITUDE\n'
        'python plots.py netcdf/OS_PIRATA-FR31_XBT.nc -t XBT -s -k DEPTH TEMP -xaxis TIME -l 29 36\n'
        'python plots.py netcdf/OS_AMAZOMIX_TSG.nc -t TSG --scatter  -k SSPS SSTP -o plots/AMAZOMIX\n'

        ' \n',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='J. Grelet IRD US191 - March 2021 / April 2021')
    parser.add_argument('files',
                        help='netcdf file to parse')
    parser.add_argument('-a', '--append', default="",
                        help='string to append in output filename')
    parser.add_argument('-t', '--type',
                        choices=['CTD', 'XBT', 'ADCP', 'TSG'],
                        required=True,
                        help='select type instrument CTD, XBT, LADCP, TSG')
    parser.add_argument('-p', '--profiles', '--profile',
                        action='store_true',
                        help='plot profiles')
    parser.add_argument('-k', '--keys',
                        nargs='+',
                        help='select physical parameters key(s), (default: %(default)s)')
    parser.add_argument('-l', '--list',
                        nargs='+', type=int,
                        help='select first and last profile, default (none) is all')
    parser.add_argument('-e', '--exclude',
                        # nargs='*', action=Store_as_array, type=int,default=np.asarray([]),
                        nargs='*', type=int, default=[],
                        help='give a list of profile(s) to exclude')
    parser.add_argument('-c', '--colors',
                        nargs='+',
                        help='select colors, ex: k- b- r- m- g-')
    parser.add_argument('-f', '--force',
                        action='store_true',
                        help='force graphic output even if the file exist')
    parser.add_argument('-g', '--grid',
                        action='store_true',
                        help='add grid')
    parser.add_argument('-s', '--sections', '--section',
                        action='store_true',
                        help='plot sections')
    parser.add_argument('--scatters', '--scatter',
                        action='store_true',
                        help='plot scatters')
    parser.add_argument('--dims', '--dimensions',
                        nargs='+', default=['TIME', 'LATITUDE','LONGITUDE'],
                        help='give dimensions name, ex: TIME, LATITUDE, LONGITUDE')
    parser.add_argument('--xaxis',
                        choices=['LATITUDE', 'LONGITUDE', 'TIME'], default='TIME',
                        help='select xaxis for sections')
    parser.add_argument('--yscale', action=Store_as_array, nargs='*', type=int, default=np.asarray([0, 1000]),
                        help='select vartical scale for sections, ex: 0 2000 or 0 250 250 2000')
    parser.add_argument('--xinterp', type=int, default=None,
                        help='horizontal interpolation points')
    parser.add_argument('--yinterp', type=int, default=1,
                        help='vertical interpolation step, none plot raw data')
    parser.add_argument('--clevels', type=int, default=20,
                        help='contour levels')
    parser.add_argument('--autoscale', nargs='*', type=int, default=[0],
                        help=textwrap.dedent('''\
        None:       use NetCDF valid min and max
        True:       use min(Z) and max(Z)
        [min, max]: define manually min and max'''))
    parser.add_argument('--display', '--display_profiles',
                        action='store_true',
                        help='display profiles number on top axes')
    parser.add_argument('--screen',
                        action='store_true',
                        help='display graphics on screen')
    parser.add_argument('-o', '--out',
                        help='output path, default is plots/')
    parser.add_argument('-d', '--debug', help='display debug informations',
                        action='store_true')
    return parser


def on_object_change(func):
    def wrapper(*args, **kwargs):
        print("value changed %s - %s" % (args, kwargs))
        func(*args, **kwargs)
        return wrapper


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def julian2dt(jd):
    # see: https://en.wikipedia.org/wiki/Julian_day
    # Julian Date	12h Jan 1, 4713 BC
    # Modified JD	0h Nov 17, 1858	JD − 2400000.5
    # CNES JD	0h Jan 1, 1950	JD − 2433282.5
    jd = jd + JULIAN_1950
    dt = julian.from_jd(jd, fmt='mjd')
    return dt


def dt2julian(dt):
    jd = julian.to_jd(dt) - JULIAN_1970
    return jd

# Dec2dms convert decimal position to degree, mim with second string,
# hemi = 0 for latitude, 1 for longitude
def Dec2dms(position, hemi):
    if re.match('[EW]', hemi):
        neg = 'W'
        pos = 'E'
    else:
        neg = 'S'
        pos = 'N'
    if position < 0:
        geo = neg
    else:
        geo = pos
    # get integer and decimal part
    dec, intg = math.modf(position)
    # get integer and decimal part of min.sec
    sec, min = math.modf((dec / 100) * 6000)
    if re.match('[EW]', hemi):
        str = "{:0>3.0f}{:s}{:2.4f} {}".format(
            intg, DEGREE, min + sec/100*60, geo)
    else:
        str = "{:0>2.0f}{:s}{:2.4f} {}".format(
            intg, DEGREE, min + sec/100*60, geo)
    return str

# interpolate data on x axis
def interpx(xinterp, x, xi, yi, zi):
    xx, yy = np.meshgrid(xi, yi, indexing='ij')
    xi = np.linspace(x[0], x[-1], xinterp)
    zi = griddata((xx.ravel(), yy.ravel()), zi.ravel(),
                    (xi[None, :], yi[:, None]))
    return (xi,zi)

# class Plots
class Plots():
    def __init__(self, file, dims, keys, ti, colors, append, grid=False):
        self.nc = Dataset(file, mode='r')
        self.dims = dims
        self.keys = keys
        self.colors = colors
        self.type = ti
        self.grid = grid
        self.append = append
        self.fig = None
        self.ax = None

    # @on_object_change
    def __setattr__(self, *args, **kwargs):
        super().__setattr__(*args, **kwargs)

    def __getitem__(self, key):
        ''' overload s[key] with key is the physical parameter '''
        if hasattr(self, key):
            logging.error(
                "plot_profiles.py: invalid attribute: \"{}\"".format(key))
        else:
            return getattr(self, key)

    def plot(self, path, figname):
        dest = os.path.normpath(os.path.join(path, figname))
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest), exist_ok=True)

        print('Printing: ', dest)
        if args.screen:
            plt.show()

        self.fig.savefig(dest)
        plt.close(self.fig)

    def profiles(self, profile):

        # find the profile index
        profiles = self.nc.variables['PROFILE'][:].tolist()
        try:
            index = profiles.index(profile)
        except:
            #print('Profile {} is missing'.format(profile))
            return

        # construct plot file name
        sep = "_" if self.append else ""
        figname = '{}-{:05d}_{}{}{}.png'.format(
            self.nc.cycle_mesure, profile, self.type, sep, self.append)
        dest = os.path.join(path, figname)
        # test if file exist
        if os.path.isfile(dest) and not args.force:
            return

        # initialize subplots
        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        self.fig.subplots_adjust(top=0.95-((len(self.keys)-1)*0.06))
        offset = 0.14
        tkw = dict(size=4, width=1.5)

        # the first plot with the first parameter, DEPTH or PRES
        y = self.nc.variables[self.keys[0]][index, :]
        x = self.nc.variables[self.keys[1]][index, :]
        p, = self.ax.plot(x, y, self.colors[1],
                          label=self.nc.variables[self.keys[1]].long_name)
        self.ax.set_ylim(min(y), max(y))
        self.ax.invert_yaxis()
        self.ax.set_xlim(self.nc.variables[self.keys[1]].valid_min,
                         self.nc.variables[self.keys[1]].valid_max)
        self.ax.set_ylabel('{} [{}]'.format(self.nc.variables[self.keys[0]].long_name,
                                            self.nc.variables[self.keys[0]].units))
        self.ax.set_xlabel('{} [{}]'.format(self.nc.variables[self.keys[1]].long_name,
                                            self.nc.variables[self.keys[1]].units))
        self.ax.xaxis.label.set_color(p.get_color())
        self.ax.tick_params(axis='x', colors=p.get_color(), **tkw)
        self.ax.tick_params(axis='y', **tkw)

        position = 'bottom'

        # loop over the last parameters
        for k in range(2, len(self.keys)):
            i = k-2
            par = self.ax.twiny()
            key = self.keys[k]
            # if (k % 2) == 0:
            #     position = 'top'
            #     par.spines[position].set_position(("outward", 1.0+(offset*i)))
            #     print('{}'.format(1.0+(offset*i)))
            # else:
            #     position = 'bottom'
            #     par.spines[position].set_position(("outward", 0-(offset*i)))
            #     print('{}'.format(0-(offset*i)))

            position = 'top'
            par.spines[position].set_position(("axes", 1.0+(offset*i)))
            make_patch_spines_invisible(par)
            par.spines[position].set_visible(True)

            # get data
            x = self.nc.variables[key][index, :]
            p, = par.plot(x, y, self.colors[k],
                          label=self.nc.variables[key].long_name)
            par.set_xlim(self.nc.variables[key].valid_min,
                         self.nc.variables[key].valid_max)
            par.set_xlabel('{} [{}]'.format(self.nc.variables[key].long_name,
                                            self.nc.variables[key].units))
            par.xaxis.label.set_color(p.get_color())
            par.tick_params(axis='x', colors=p.get_color(), **tkw)

        # add grid on plot
        if(self.grid):
            self.ax.grid()

        # self.ax.legend(lines, [l.get_label() for l in lines])
        self.fig.text(0.15, 0.95,
                      '{}, {}, Profile: {:03d} Date: {} Lat: {} Long: {}'
                      .format(self.nc.cycle_mesure,
                              self.type,
                              profile,
                              julian2dt(
                                  self.nc.variables[self.dims[0]][index]),
                              Dec2dms(
                                  self.nc.variables[self.dims[1]][index], 'N'),
                              Dec2dms(
                                  self.nc.variables[self.dims[2]][index], 'W'),
                              va='center', rotation='horizontal'))
        self.plot(path, figname)

    # plot one or more sections
    def section(self, start, end, xaxis, yscale, exclude,
                xinterp=None, yinterp=1, clevels=20, autoscale=0, display=None):

        # Y variable, PRES or DEPTH, must be first, add test
        yaxis = self.keys[0]
        # get the profile list
        profiles = self.nc.variables['PROFILE'][:].tolist()
        ymax = np.max(yscale)
        # construct the vector index of the profiles list, without excluded value(s)
        # this vector is use to extract the profiles from netcdf file
        index_profiles = []
        index_exclude = []
        for i in exclude:
            index_exclude.append(profiles.index(i))
        for i in range(start, end + 1):
            try:
                index_profiles.append(profiles.index(i))
            except:
                print("invalid --list {}-{}, we use last profile = {}".format(start, end,
                                                                              profiles[-1]))
                i = i - 1
                break
        # remove the exclude list indice from profile list indice
        # https://www.geeksforgeeks.org/python-indices-list-of-matching-element-from-other-list/?ref=rp
        res = [i for i, val in enumerate(index_profiles) if val in index_exclude]
        index_profiles = np.delete(index_profiles, res)
        list_profiles = self.nc.variables['PROFILE'][index_profiles].tolist()

        nbxi = len(index_profiles)
        labelrotation = 15 if nbxi > 15 else 0
        # if xinterp > end - start:
        #     xinterp = end - start
        if xaxis == 'LATITUDE':
            x_formatter = LatitudeFormatter()
        elif xaxis == 'LONGITUDE':
            x_formatter = LongitudeFormatter()
        else:
            x_formatter = mdates.DateFormatter('%Y/%m/%d %H:%M')
            labelrotation = 15
        for k in range(1, len(self.keys)):
            var = self.keys[k]
            x = self.nc.variables[xaxis][index_profiles]
            if xaxis == 'TIME':
                for i in range(0, len(x)):
                    x[i] = dt2julian(julian2dt(x[i]))
            y = self.nc.variables[yaxis][index_profiles, :]
            # find index of the max value given by yscale
            _, c = np.where(y >= ymax)
            if c.size == 0:
                sys.exit("invalid --yscale {}, max value must be <= {}".format(yscale.tolist(),
                                                                               np.max(y)))
            y = self.nc.variables[yaxis][index_profiles, :c[0]]
            z = self.nc.variables[var][index_profiles, :c[0]]
            xi = np.linspace(x[0], x[-1], nbxi)
            yi = np.arange(np.round(np.amin(y)),
                             np.ceil(np.amax(y))+ yinterp, yinterp)
            nbyi = len(yi)

            # contourf indeed works a bit differently than other ScalarMappables.
            # If you specify the number of levels (20 in this case) it will take
            # them between the minimum and maximum data (approximately).
            # If you want to have n levels between two specific values vmin and vmax
            # you would need to supply those to the contouring function.
            if not isinstance(autoscale, list):
                sys.exit("autoscale: bad type {}, value <{}>, should be an integer <0>, <1> or <0 30>".format(
                    type(autoscale), autoscale))
            elif len(autoscale) == 2:
                zmin = autoscale[0]
                zmax = autoscale[1]
            else:
                if autoscale[0] == 1:
                    zmin = np.min(z)
                    zmax = np.max(z)
                elif autoscale[0] == 0:
                    zmin = self.nc.variables[var].valid_min
                    zmax = self.nc.variables[var].valid_max
                else:
                    sys.exit(
                        "autoscale: bad value <{}>, should be <0>, <1> or <0 30>".format(autoscale[0]))

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
            zi = zi.reshape(nbxi, nbyi)

            # horizontal interpolation
            if xinterp == None:
                zi = zi.transpose()
            else:
                (xi, zi) = interpx(xinterp, x, xi, yi, zi)
            
            # Specifies the geometry of the grid that a subplot will be placed
            self.fig = plt.figure(figsize=(8, 8))
            # set gridspec ration, one or two subplots
            ratio = [1, yscale.ndim] if yscale.ndim == 2 else None
            # loop over vertical range, ex: [0,2000] or [[0,250], [250,2000]]
            gs = gridspec.GridSpec(yscale.ndim, 1, height_ratios=ratio)

            # loop over vertical range, ex: [0,2000] or [[0,250], [250,2000]]
            for i, ax in enumerate(gs):
                ax = plt.subplot(gs[i])
                if i == 0:
                    ax.set_title('{}\n{} {}\n{}, {} [{}]'.format(self.nc.cycle_mesure,
                                                               self.type, self.append.replace('_',' '), 
                                                               var, self.nc.variables[var].long_name,
                                                               self.nc.variables[var].units))
                # set vertical axes
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
                # add test for LONGITUDE and TIME
                ax.set_xticks(
                    np.arange(np.round(np.min(x)), np.ceil(np.max(x))), minor=True)
                ax.tick_params(axis='x', labelrotation=labelrotation)
                ax.xaxis.set_major_formatter(x_formatter)
                # add a colorbar on each subplot when profile numbers are displayed
                if display:
                    plt.colorbar(plt1, ax=ax)

            # add a secondary axes on top with profiles number
            if display:
                ax2 = ax.twiny()
                ax2.set_xlim(ax.get_xlim())
                ax2.set_xticks(x)
                ax2.set_xticklabels(list_profiles, fontsize=6)
            else:
                # Matplotlib 2 Subplots, 1 Colorbar
                # https://stackoverflow.com/questions/13784201/matplotlib-2-subplots-1-colorbar
                plt.colorbar(plt1, ax=self.fig.axes)

            ax.set_xlabel('{}'.format(self.nc.variables[xaxis].standard_name))
            ylabel = '{} [{}]'.format(self.nc.variables[yaxis].standard_name,
                                      self.nc.variables[yaxis].units)

            # display common y label with text instead of ax.set_ylabel
            self.fig.text(0.04, 0.5, ylabel, va='center',
                     ha='center', rotation='vertical')
            sep = "_" if self.append else ""
            figname = '{}{}{}-{}-{}.png'.format(
                self.nc.cycle_mesure, sep, self.append, self.type, var)
            #dest = os.path.join(path, figname)
            self.plot(path, figname)
            # fig.savefig(dest)
            # print('Data: {}, printing: {}'.format(np.shape(zi), dest))
            # if args.screen:
            #     plt.show()
            # plt.close(fig)

    def scatters(self, path):
        #ncfile = os.path.join(path, self.nc)

        SSPS = self.nc.variables[self.keys[0]]
        SSTP = self.nc.variables[self.keys[1]]
        TIME = self.nc.variables[self.dims[0]]
        LATITUDE = self.nc.variables[self.dims[1]]
        LONGITUDE = self.nc.variables[self.dims[2]]
        if 'cycle_mesure' in self.nc.ncattrs():
            CM = self.nc.cycle_mesure
        else:
            CM = self.nc.CYCLE_MESURE
       
        x1 = min(LONGITUDE) 
        x2 = max(LONGITUDE) 
        y1 = min(LATITUDE) 
        y2 = max(LATITUDE) 
       
        area = [x1, x2, y1, y2]
        self.fig = plt.figure(figsize=(6, 12))
        gs = gridspec.GridSpec(2,1)
        ax1 = plt.subplot(gs[0], projection=ccrs.Mercator())
        ax1.set_extent(area, crs=ccrs.PlateCarree())
        ax1.coastlines(resolution='auto', color='k')
        ax1.gridlines(color='lightgrey', linestyle='-', draw_labels=True)

        im1 = ax1.scatter(LONGITUDE[:], LATITUDE[:], c=SSPS[:], s=30, cmap='jet', vmin=32, vmax=37, transform=ccrs.PlateCarree())
        self.fig.colorbar(im1, ax=ax1, orientation='vertical', pad=0.15)
        ax1.set(xlabel='{} '.format(LONGITUDE.standard_name), ylabel='{} '.format(LATITUDE.standard_name),
                title='{} - {}'.format(CM, SSPS.long_name))

        ax2 = plt.subplot(gs[1], projection=ccrs.Mercator())
        ax2.set_extent(area, crs=ccrs.PlateCarree())
        ax2.coastlines(resolution='auto', color='k')
        ax2.gridlines(color='lightgrey', linestyle='-', draw_labels=True)

        im2 = ax2.scatter(LONGITUDE[:], LATITUDE[:], c=SSTP[:], s=30, cmap='jet', vmin=5, vmax=32, transform=ccrs.PlateCarree())
        self.fig.colorbar(im2, ax=ax2, orientation='vertical', pad=0.15)
        ax2.set(xlabel='{} '.format(LONGITUDE.standard_name), ylabel='{} '.format(LATITUDE.standard_name),
                title='{} - {}'.format(CM, SSTP.long_name))

        figname = '{}_TSG_COLCOR_SCATTER.png'.format(CM)
        #dest = os.path.join(path, figname)
        self.plot(path, figname)
        # fig.savefig(dest)
        # print('Printing: ', dest)
        # if args.screen:
        #     plt.show()
        # plt.cla()

# main program
# 'b' = blue (bleu), 'g' = green (vert), 'r' = red (rouge),
# 'c' = cyan (cyan), 'm' = magenta (magenta), 'y' = yellow (jaune),
# 'k' = black (noir), 'w' = white (blanc).
if __name__ == '__main__':

    # recover and process line arguments
    parser = processArgs()
    args = parser.parse_args()

    # 'b' = blue (bleu), 'g' = green (vert), 'r' = red (rouge),
    # 'c' = cyan (cyan), 'm' = magenta (magenta), 'y' = yellow (jaune),
    # 'k' = black (noir), 'w' = white (blanc).
    if args.colors == None:
        args.colors = ['k-', 'b-', 'r-', 'm-', 'g-']

    # set output path, default is plots
    if args.out == None:
        if args.profiles:
            path = 'plots/profiles'
        if args.sections:
            path = 'plots/sections'
        if args.scatters:
            path = 'plots/scatters'
    else:
        path = args.out
 
    # set looging mode if debug
    if args.debug:
        logging.basicConfig(
            format='%(levelname)s:%(message)s', level=logging.DEBUG)
        mpl_logger = logging.getLogger('plt')
        mpl_logger.setLevel(logging.ERROR)

    # logging.debug(args)
    # print(args)
    # sys.exit()

    # instanciate plots class
    p = Plots(args.files, args.dims, args.keys, args.type,
              args.colors, args.append, args.grid)

    if args.scatters:
        p.scatters(path)
    else:

        # set first and last profiles or all profiles
        profiles = p.nc.variables['PROFILE']
        end = profiles[-1]
        if args.list == None:
            start = profiles[0]
        # from args.list with start and end values
        elif len(args.list) == 2:
            start, end = args.list[0], args.list[1]
        # from args.list with start to last values
        elif len(args.list) == 1:
            start = args.list[0]

        # plot profiles
        if args.profiles:
            for s in range(start, end+1):
                p.profiles(s)

        # plot sections
        # vars:  start, end, xaxis, yscale, xinterp=24, yinterp=200, clevels=20,
        # autoscale=True
        if args.sections:
            p.section(start, end, args.xaxis, args.yscale, args.exclude, args.xinterp,
                    args.yinterp, args.clevels, args.autoscale, args.display)
