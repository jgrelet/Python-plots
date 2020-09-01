from netCDF4 import Dataset
import numpy as np
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import os

file = 'OS_PIRATA-FR30_XBT.nc'
ncpath = 'netcdf'
path = 'sections'
#ncpath = '.'
#path = 'png'

ncfile = os.path.join(ncpath, file)
nc = Dataset(ncfile, mode='r')

TEMP = nc.variables['TEMP']
DEPTH = nc.variables['DEPTH']
PROFILE = nc.variables['PROFILE']
LAT = nc.variables['LATITUDE']
LON = nc.variables['LONGITUDE']
STATION = PROFILE.shape[0]
CM = nc.cycle_mesure

#Create a list of the length we want
# lon : int ; x : list
def list(x,lon):
    max_x = max(x)
    min_x = min(x)
    list = np.linspace(min_x,max_x,lon)
    return list
#Finds the index when a value in the list x is greater than the desired distance
# distance : int ; x : list
def Indice(x,distance):
    dim = (np.where(x<=distance)[0])
    long = len(dim)-1
    return long

labels = ['MIDELO_0N-10W','0-10W - 0-0','3S-0 - 20S-10W','20S-10S - 10W ','10W-23W','23W-0']
LAT1 = ['','','3°N','','5°N','','7°N','','9°N','','11°N','','13°N','','15°N','']
LON1 = ['10°W','','8°W','','6°W','','4°W','','2°W','']
LAT2 = ['','','18°S','','16°S','','14°S','','12°S','','10°S']
LON2 = ['21°W','','19°W','','17°W','','15°W','','13°W','']
LON3 = ['23°W','','21°W','','19°W','','17°W','','15°W','','13°W','','11°W','']
place = [LAT1,LON1,LON1,LAT2,LON2,LON3]
inverse = [True,False,True,False,True,False]

#Arguments :
#TEMP, DEPTH : Matrix
#PROFILE, LATX , inverse: List
#debut, fin : int

def plot_section(TEMP,DEPTH,PROFILE,debut,fin,LATX,inverse):
    fig, ax = plt.subplots(2,1, sharex=True, sharey=True)
    num1 = PROFILE[debut] #number of the first profile
    num2 =  PROFILE[fin] #number of the last profile
    profil = num2 - num1 +1 #number of profile to be drawn
    print('SECTION',num1,'-',num2)
#get the index when the distance is less than 250m

    long1 = Indice(DEPTH[num1-1,:],251)
#get the index when the distance is less than 900m
    long2 = Indice(DEPTH[num1-1,:],901)

    long2 = long2 - long1

#list to have the scale on y for the plot
    Y1 = np.arange(0,300,50)
    Y2 = np.arange(250,900,100)

    TEMP_1 = np.zeros((long1,profil)) 
    TEMP_2 = np.zeros((long2,profil)) 

#length of the new matrix (number of measurements taken into account)
    size1 = long2 + long1
    for k in range(0,size1) :
            
#Values ​​ranging from 0m to 250m below sea surface
        if (k<long1):
            temp = TEMP[num1-1:num2,k]
            
            if (inverse==True) : 
                TEMP_1 [k] = temp[::-1]
            else :
                TEMP_1 [k] = temp 

#Values ​​ranging from 0m to 250m below sea surface            
        if (k>long1):
            temp = TEMP[num1-1:num2,k]
            
            if (inverse==True) : 
                TEMP_2 [k-long1] = temp[::-1]       
            else :
                TEMP_2 [k-long1] = temp  

#List for drawing lines on the plot
    levels=np.arange(0,35,1)
    levels1=np.arange(0,35,5)
    
    fig.text(0.25, 0.02,'LATX : LATITUDE (decimal degree)', va='center', rotation='horizontal')
    fig.text(0.01, 0.5, 'DEPTH ', va='center', rotation='vertical')
    fig.text(0.04, 0.5, 'DEPTH BELLOW SEA SURFACE', va='center', rotation='vertical')
    #First plot
    ax = plt.subplot(211)
    plt.title('{} - XBT Profils : {} - {}'.format(CM, num1,num2-1))
    plt.gca().invert_yaxis()
    #Vmin,Vmax : use to have the same scale
    CS = ax.contourf(TEMP_1,levels,cmap=plt.cm.jet,vmin = 0,vmax = 30)#Trace the background
    CS1 = ax.contour(TEMP_1,levels,colors='k',linewidths=(0.5),vmin = 0,vmax = 30)#Draw the lines in black ('k')
    CS2 = ax.contour(TEMP_1,levels1,colors='k',linewidths=(1.5),vmin = 0,vmax = 30)#Draw the lines in  with different thickness black ('k')
    fig.colorbar(CS, ax=ax)
    plt.yticks(np.arange(0, long1, long1/5),Y1) # write depth on the y axis
    plt.xticks(np.arange(0, profil, profil/len(place)),place)# write latitude on the x axis
    #Second plot
    ax1 = plt.subplot(212)
    plt.gca().invert_yaxis()
    CS_ = ax1.contourf(TEMP_2,levels,cmap=plt.cm.jet,vmin = 0,vmax = 30) #Trace the background
    CS_1 = ax1.contour(TEMP_2,levels,colors='k',linewidths=(0.5),vmin = 0,vmax = 30)#Draw the lines in black ('k')
    CS_2 = ax1.contour(TEMP_2,levels1,colors='k',linewidths=(1.5),vmin = 0,vmax = 30)#Draw the lines in  with different thickness black ('k')
    fig.colorbar(CS_, ax=ax1) #bring up the colorbar
    ax1.clabel(CS_1,inline = True, fmt='%1.0f',fontsize=6) # Write the value of the line on the line
    plt.yticks(np.arange(0, long2, long2/7),Y2) # write depth on the y axis
    plt.xticks(np.arange(0, profil, profil/len(place)),place)  # write latitude on the x axis
    
    figname = '{}-{}-{}_XBT_TEMP_{}.png'.format(CM, PROFILE[debut],PROFILE[fin],label)
    dest = os.path.join(path, figname)
    fig.savefig(dest,format='png', dpi=1200)
    print('Printing: ', dest)
    #plt.show()
    plt.clf()
    plt.close(fig)    
    
L = [0,2,4,6,8,10]
num_p=[0,15,16,25,27,41,41,52,55,64,67,102]

for label,place,inverse,indice in zip(labels,place,inverse,L):
    plot_section(TEMP,DEPTH,PROFILE,LAT,LON,num_p[indice],num_p[indice+1],place,inverse)
print('DONE')