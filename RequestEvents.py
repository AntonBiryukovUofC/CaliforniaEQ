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
client = Client("NCEDC")

allQuakes,allStations = ReadFilterEQandStations(parent_dir = './events/', cutoff = 200,
                                                mag_min=1.7)
errors = allQuakes.EY
values,bins = np.histogram(errors,bins=100,density=True)
bins_points = (bins[:-1]+bins[1:])/2.0
pmf = integrate.cumtrapz(values, bins_points, initial=0)
plt.plot(bins_points,pmf)


fig1  =DrawMapEvents(allQuakes,allStations)
length = 5  # in seconds





i=0.0
presentBG = np.zeros(allQuakes.shape[0])
presentNC = np.zeros(allQuakes.shape[0])
returnn
for _, item in allQuakes.iterrows():
    dest_name = parent_dir + 'BGevent_%d.mseed' % item.ID
    t = item.UTCDT
    try:
        listBG="BUC,SQK,STY,INJ,DRK,FUM,SB4,DXR,AL4"
        stBG = client.get_waveforms("BG", "*", "*", "*Z", t, t + length,attach_response=False)
        #stBG = client.get_waveforms("BG", listBG, "*", "*Z", t, t + 3,attach_response=False)
        presentBG[i] =1
        stBG.write(dest_name,format='MSEED')
        print 'Saving %s ' % dest_name
    except:
        print 'This event %d data is not available for BG' % item.ID
    

    dest_name = parent_dir + 'NCevent_%d.mseed' % item.ID
    try: 
        stNC = client.get_waveforms("NC", "GCM,GDX,GDXB,GMM", "*", "*Z", t, t + length,attach_response=False)
        presentNC[i] =1
        stNC.write(dest_name,format='MSEED')
        print 'Saving %s ' % dest_name
    except:
        print 'This event %d data is not available for BG' % item.ID
    
    
    
    
    
        
    try:
        dest_name = parent_dir + 'QML_event_%d.xml' % item.ID
        event = client.get_events(eventid=item.ID)
        event.write(dest_name,format = 'QUAKEML')
        print 'Saving %s ' % dest_name
    
    except:
        print 'Event data not found for %d' % item.ID
    
    i+=1
    print "%d / %d is done -- %3.2f" %(i,allQuakes.shape[0],i/allQuakes.shape[0]*100.0)                           

np.savez('%2.1f.npz' % mag_min, presentBG=presentBG,presentNC=presentNC,allQuakes=allQuakes,allStations=allStations)
        

    
    
    
    
    
    
    
    
    
    
    
   