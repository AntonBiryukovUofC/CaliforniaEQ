import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import integrate
from mpl_toolkits.basemap import Basemap
import obspy
from saveMSEEDEventID_functions import ReadFilterEQandStations,DrawMapEvents
pd.set_option('mode.chained_assignment','warn')
mpl.style.use('ggplot')
from obspy.fdsn import Client
from matplotlib import cm

def ndToDataframe(allQuakes):
    import pandas as pd
    header_names2= ['Year','Month','Day','Hour','Min','Sec', 'LAT', 
                   'LON','DEP','EX','EY','AZ','EZ','MAG','ID','UTCDT']
    allQuakesDF = pd.DataFrame(allQuakes)
    allQuakesDF.columns = header_names2
    return allQuakesDF
    
mag_min = 1.7
allStations = pd.read_csv('allStationsOnly.txt',sep = '\s+')


npzfile=  np.load('%2.1f.npz' % mag_min)
presentBG= npzfile['presentBG']
presentNC = npzfile['presentNC']
allQuakes = ndToDataframe(npzfile['allQuakes'])
allQuakes['inBG'] = presentBG.astype('bool')
allQuakes['inNC'] = presentNC.astype('bool')

allQuakes = allQuakes.ix[allQuakes['inBG'] & allQuakes['inNC'] ,:]

errors = allQuakes.EY
values,bins = np.histogram(errors,bins=100,density=True)
bins_points = (bins[:-1]+bins[1:])/2.0
pmf = integrate.cumtrapz(values, bins_points, initial=0)
#plt.plot(bins_points,pmf)
leftcornerbot =[-122.836,38.78-0.0001]
rightcornerup = [-122.732,38.84+0.0001]

    
    
    
    
    
    
    
    
   