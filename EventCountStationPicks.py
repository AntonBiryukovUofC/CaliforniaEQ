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
from plotly.plotly import plot
import plotly.graph_objs as go
import plotly.tools as tls 
tls.set_credentials_file(username='Anton.Biryukov', api_key='q0iwsvqelb')


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


#plt.plot(bins_points,pmf)
leftcornerbot =[-122.836,38.78-0.0001]
rightcornerup = [-122.732,38.84+0.0001]
#sta_triplet = ['ACR','SB4','AL4']
sta_triplet = ['ACR','SB4','FUM']

subset_stations = allStations.ix[
                                (allStations['LAT']>leftcornerbot[1]) & (allStations['LAT']<rightcornerup[1]) &
                                (allStations['LON']>leftcornerbot[0]) & (allStations['LON']<rightcornerup[0]) &
                                (allStations['Station_Code'].isin(sta_triplet))
                                ]
subset_stations.index = range(subset_stations.shape[0])
allQuakes.index = range(allQuakes.shape[0])

counts = np.zeros((allQuakes.shape[0],len(sta_triplet)))

for indSta,rowSta in subset_stations.iterrows():
    print 'Counting events on %s.%s' % (rowSta['Network_Code'],rowSta['Station_Code'])
    for index, row in allQuakes.iterrows():
        count=0
    
        ideq = row['ID']
        #NCst = obspy.read('./events/NCevent_%d.mseed' % ideq).select(station = rowSta)
        BGst = obspy.read('./events/BGevent_%d.mseed' % ideq).select(station=rowSta['Station_Code']).count()
        count+=BGst
        #print '%3.2f' % (1.0*index/(allQuakes.shape[0]))
        counts[index,indSta] = count
counts = counts.astype('bool')

allQuakes['inSTA1'] = counts[:,0]
allQuakes['inSTA2'] = counts[:,1]
allQuakes['inSTA3'] = counts[:,2]
allQuakes = allQuakes.ix[allQuakes['inSTA1'] & allQuakes['inSTA2'] & allQuakes['inSTA3']]
#subset_stations['NEvents'] = counts
#subset_stations.to_csv('./subsetStationsAL4ACRFUM.csv')
allQuakes.to_csv('./quakesOn3Sta.csv')
#QMLst = obspy.read('./events/QML_event_%d.mseed' % ideq)
    
    
    
    
    
    
    
    
   