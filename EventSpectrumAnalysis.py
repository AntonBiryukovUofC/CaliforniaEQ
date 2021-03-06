import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import integrate
from mpl_toolkits.basemap import Basemap
import obspy
from saveMSEEDEventID_functions import ReadFilterEQandStations,DrawMapEvents
pd.set_option('mode.chained_assignment','warn')
from obspy.fdsn import Client
from matplotlib import cm

def ndToDataframe(npzfile):
    import pandas as pd
    header_names2= ['Year','Month','Day','Hour','Min','Sec', 'LAT', 
                   'LON','DEP','EX','EY','AZ','EZ','MAG','ID','UTCDT']
    allQuakesDF = pd.DataFrame(npzfile['allQuakes'])
    presentBG= npzfile['presentBG']
    presentNC = npzfile['presentNC']
    
    allQuakesDF.columns = header_names2
    
    allQuakesDF['inBG'] = presentBG.astype('bool')
    allQuakesDF['inNC'] = presentNC.astype('bool')
    
    
    allStations = pd.read_csv('allStationsOnly.txt',sep = '\s+')

    return allQuakesDF, allStations
    
mag_min = 1.7

npzfile=  np.load('%2.1f.npz' % mag_min)

allQuakes,allStations = ndToDataframe(npzfile)


allQuakes = allQuakes.ix[allQuakes['inBG'] & allQuakes['inNC'] ,:]

errors = allQuakes.EY
values,bins = np.histogram(errors,bins=100,density=True)
bins_points = (bins[:-1]+bins[1:])/2.0
pmf = integrate.cumtrapz(values, bins_points, initial=0)
#plt.plot(bins_points,pmf)
leftcornerbot =[-122.836,38.78-0.0001]
rightcornerup = [-122.732,38.84+0.0001]

subset_stations = allStations.ix[
                                (allStations['LAT']>leftcornerbot[1]) & (allStations['LAT']<rightcornerup[1]) &
                                (allStations['LON']>leftcornerbot[0]) & (allStations['LON']<rightcornerup[0]) &
                                (allStations['Network_Code'].isin(['NC','BG']))
                                ]

ideq = 71701935

NCst = obspy.read('./events/NCevent_%d.mseed' % ideq)
BGst = obspy.read('./events/BGevent_%d.mseed' % ideq)
event_record = allQuakes[allQuakes.ID == ideq]
#QMLst = obspy.read('./events/QML_event_%d.mseed' % ideq)
    
    
    
    
    
    
    
    
   