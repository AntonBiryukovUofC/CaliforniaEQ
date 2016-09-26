import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import integrate
from mpl_toolkits.basemap import Basemap
import obspy
from saveMSEEDEventID_functions import saveWaveformsByID,toUTC,filterEQ
pd.set_option('mode.chained_assignment','warn')
mpl.style.use('ggplot')


header_names1= ['Year','Month','Day','Hour','Min','Sec', 'LAT', 
               'LON','DEP','EX','EY','EZ','MAG','ID','VER','BASE','METH']
header_names2= ['Year','Month','Day','Hour','Min','Sec', 'LAT', 
               'LON','DEP','EX','EY','AZ','EZ','MAG','ID']
#allQuakes = pd.read_csv('NCAeqDDRT.csv',sep='\s+',skiprows=92,header=None,names = header_names)
allQuakes = pd.read_csv('NCAeqDD1984-2011.csv',sep='\s+',skiprows=80,header=None,names = header_names2)
allStations = pd.read_csv('allStationsOnly.txt',sep = '\s+')
allQuakes['EX'] =allQuakes['EX']*1000.0
allQuakes['EY'] =allQuakes['EY']*1000.0
allQuakes['EZ'] =allQuakes['EZ']*1000.0
parent_dir = './events/'
 
cutoff= 200
mag_min =2.0


allQuakes = allQuakes[(allQuakes.EZ < cutoff) & (allQuakes.EZ > 0) & 
                        (allQuakes.EX < cutoff) & (allQuakes.EX > 0) &
                         (allQuakes.EY < cutoff) & (allQuakes.EY > 0) &
                         (allQuakes.LAT>38.78) & (allQuakes.LAT<38.84)
                         & (allQuakes.LON< -122.72) & (allQuakes.LON> -122.86) &
                          (allQuakes.MAG > mag_min) ]
                          
allQuakes['UTCDT'] =  allQuakes.iloc[:,0:6].apply(toUTC,axis=1)
date_cutoff = obspy.UTCDateTime(2003,05,1)
allQuakes = allQuakes[allQuakes.UTCDT > date_cutoff]
#allQuakes['UTCDT'] = '2009-12-31T12:23:34.5'

                          
errors = allQuakes.EY
values,bins = np.histogram(errors,bins=100,density=True)
bins_points = (bins[:-1]+bins[1:])/2.0
pmf = integrate.cumtrapz(values, bins_points, initial=0)
plt.plot(bins_points,pmf)
w = 15
h=15
fig = plt.figure(figsize = (w,h))
m = Basemap(llcrnrlon=-122.86,llcrnrlat=allQuakes.LAT.min()-0.0001,urcrnrlon=-122.72,urcrnrlat=allQuakes.LAT.max()+0.0001,lat_0 = allQuakes.LAT.mean(),lon_0=allQuakes.LON.mean(),
            resolution ='h',area_thresh=10.,fix_aspect=False)
lon_eq = np.linspace(allQuakes.LON.min(),allQuakes.LON.max(),10)
lat_eq = np.linspace(allQuakes.LAT.min(),allQuakes.LAT.max(),10)

m.drawcoastlines()
m.drawcountries()
m.drawmapboundary()
#m.etopo(zorder=0)
m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 800, verbose= True)
#m.fillcontinents(color=(0.1,0.1,0.1),zorder=1)
#m.bluemarble()
m.drawstates()
m.drawparallels(lat_eq,labels = [1,1,1,1])
m.drawmeridians(lon_eq,labels = [1,1,1,1])
m.scatter(allQuakes.LON,allQuakes.LAT,30,color='r',marker='o',alpha=0.25,zorder=10)

# Filter out the stations:
allStations = allStations[(allStations.LAT>38.78) & (allStations.LAT<38.84) &
                          (allStations.LON< -122.72) & (allStations.LON> -122.86) 
                          ]
m.scatter(allStations.LON,allStations.LAT,60,color='b',marker='v',alpha=0.99,zorder=10)
allStations['Name'] =  allStations.Network_Code + '.' + allStations.Station_Code
for label,x,y in zip(allStations.Name,allStations.LON,allStations.LAT):
    plt.annotate(label,xy = (x,y), bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),zorder=11)


returnn
for i,eID in enumerate(allQuakes.ID):
    dest_name = parent_dir + 'BGevent_%d.mseed' % eID
    url =saveWaveformsByID(eventID =eID,network = 'BG',
                           stations = ['SQK','STY','DRK','INJ'],dest_name=dest_name)
    dest_name = parent_dir + 'NCevent_%d.mseed' % eID
    url =saveWaveformsByID(eventID =eID,network = 'NC',
                           stations = ['GCM','GDX','GDXB','GMM'],dest_name=dest_name)
    print "%d / %d is done -- %3.2f" %(i,allQuakes.shape[0],i/allQuakes.shape[0]*100.0)                           
    
        

    
    
    
    
    
    
    
    
    
    
    
   