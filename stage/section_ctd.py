from netCDF4 import Dataset
import numpy as np
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import os

file = 'OS_PIRATA-FR30_top_CTD.nc'
ncpath = 'netcdf'
path = 'sections'
#ncpath = '.'
#path = 'png'

ncfile = os.path.join(ncpath, file)
nc = Dataset(ncfile, mode='r')

TEMP = nc.variables['TEMP']
DEPTH = nc.variables['DEPTH']
PSAL = nc.variables['PSAL']
DOX2 = nc.variables['DOX2']
DENS = nc.variables['DENS']
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
#Arguments :
#TEMP, DEPTH : Matrix
#PROFILE, LATX : List
#mini, maxi, debut, fin : int

def plot_section(TEMP,DEPTH,PROFILE,debut,fin,LATX,inverse,mini,maxi,pas1,pas2):

    fig, ax = plt.subplots(2,1, sharex=True, sharey=True)
    
    num1 = PROFILE[debut] #number of the first profile
    num2 =  PROFILE[fin]  #number of the last profile
    profil = num2 - num1 +1 #number of profile to be drawn
    print('SECTION',num1,'-',num2)

#get the index when the distance is less than 250
    long1 = Indice(DEPTH[num1-1,:],251)
#get the index when the distance is less than 2000
    long2 = Indice(DEPTH[num1-1,:],2000)
    long2 = long2 - long1

#list to have the scale on y for the plot
    Y1 = np.arange(0,300,50)
    Y2 = np.arange(300,2000,200)

#creation of two matrices filled with zeros for the two section plots
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
    levels=np.arange(int(mini),int(maxi),pas1)
    levels1=np.arange(mini,int(maxi),pas2)

    fig.text(0.01, 0.5, 'DEPTH ', va='center', rotation='vertical')
    fig.text(0.04, 0.5, 'DEPTH BELLOW SEA SURFACE', va='center', rotation='vertical')
    
    #First plot
    ax = plt.subplot(211)
    fig.suptitle('{} - CTD Profils : {} - {}'.format(CM, num1,num2-1))
    plt.title('{} : {} ({})'.format(TEMP.standard_name,TEMP.long_name,TEMP.units))
    plt.gca().invert_yaxis()
    CS = ax.contourf(TEMP_1,levels,cmap=plt.cm.jet,extend='both')#Trace the background
    CS1 = ax.contour(TEMP_1,levels,colors='k',linewidths=(0.5),vmin = mini,vmax = maxi)#Draw the lines in black ('k')
    CS2 = ax.contour(TEMP_1,levels1,colors='k',linewidths=(1.5),vmin = mini,vmax = maxi)#Draw the lines in  with different thickness black ('k')
    fig.colorbar(CS, ax=ax)
    plt.yticks(np.arange(0, long1, long1/5),Y1)# write depth on the y axis
    plt.xticks(np.arange(0, profil, profil/len(place)),place)# write latitude on the x axis
    #Second plot
    ax1 = plt.subplot(212)
    plt.gca().invert_yaxis()
    CS_ = ax1.contourf(TEMP_2,levels,cmap=plt.cm.jet,extend='both') #Trace the background
    CS_1 = ax1.contour(TEMP_2,levels,colors='k',linewidths=(0.5),vmin = mini,vmax = maxi) #Draw the lines in black ('k')
    CS_2 = ax1.contour(TEMP_2,levels1,colors='k',linewidths=(1.5),vmin = mini,vmax = maxi)#Draw the lines in  with different thickness black ('k')
    fig.colorbar(CS_, ax=ax1)
    ax1.clabel(CS_1,fmt='%8.5g',fontsize=6) # Write the value of the line on the line
    plt.yticks(np.arange(0, long2, long2/7),Y2)# write depth on the y axis
    plt.xticks(np.arange(0, profil, profil/len(place)),place)# write latitude on the x axis
    plt.xlabel('LATX : LATITUDE (decimal degree)')
    
    figname = '{}-{}-{}_CTD-radiale-{}-{}-{}.png'.format(CM,PROFILE[debut],PROFILE[fin],TEMP.standard_name,label,TEMP.standard_name)
    dest = os.path.join(path, figname)
    fig.savefig(dest,format='png', dpi=1200)
    print('Printing: ', dest)
    plt.show()
    plt.clf()
    plt.close(fig)    

# list to correctly write the x scale
LAT1 = ['','','1°S','','']
LAT2 = ['','','8°S','','6°S','','4°S','','2°S','','0°S','']
place = [LAT1,LAT2]
labels=['3S-1N_0W-0-2000m','10S-1-30N_10W-0-2000m']
#list to know if we must invert the x-axis or the latitudes
inverse = [True,False]
num_p=[7,14,16,39] #list of profiles that we want plotted (start and end)
L = [0,2] #prosition in num_p of the profile with which we want to start the plot

'''
for label,place,inverse,indice in zip(labels,place,inverse,L):
    pas1 = 1
    pas2 = 5
    plot_section(TEMP,DEPTH,PROFILE,num_p[indice],num_p[indice+1],place,inverse,0,32,pas1,pas2)
for label,place,inverse,indice in zip(labels,place,inverse,L):
    pas1 = 0.1
    pas2=0.5
    plot_section(PSAL,DEPTH,PROFILE,num_p[indice],num_p[indice+1],place,inverse,31,37,pas1,pas2)
for label,place,inverse,indice in zip(labels,place,inverse,L):
    pas1 = 10
    pas2 = 50
    plot_section(DOX2,DEPTH,PROFILE,num_p[indice],num_p[indice+1],place,inverse,20,230,pas1,pas2)
'''

for label,place,inverse,indice in zip(labels,place,inverse,L):
    pas1 = 0.5
    pas2 = 1
    plot_section(DENS,DEPTH,PROFILE,num_p[indice],num_p[indice+1],place,inverse,20,30,pas1,pas2)
print('DONE')
