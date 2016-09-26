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
import plotly.plotly as py
import plotly.tools as tls
tls.set_credentials_file(username='Anton.Biryukov', api_key='q0iwsvqelb')
#py.sign_in('Anton.Biryukov', 'q0iwsvqelb')

client = Client("NCEDC")

def GetClass(item,Centroids):
    #print item
    condition = np.sqrt(((Centroids.X -item.LON)**2 + (Centroids.Y -item.LAT)**2))
    cl = Centroids.ix[condition.argsort()[0]].ID
    return cl
# ind_y_select=  PVelDF.ix[(PVelDF.SourceY-select_y_coord).abs().argsort()[0]].SourceY



allQuakes,allStations = ReadFilterEQandStations(parent_dir = './events/', cutoff = 200,
                                                mag_min=1.7)
errors = allQuakes.EY
values,bins = np.histogram(errors,bins=100,density=True)
bins_points = (bins[:-1]+bins[1:])/2.0
pmf = integrate.cumtrapz(values, bins_points, initial=0)
#plt.plot(bins_points,pmf)
leftcornerbot =[-122.836,38.78-0.0001]
rightcornerup = [-122.732,38.84+0.0001]

                       
# Organize classes :
                       
nX = 5
nY = 5
dx = (rightcornerup[0] - leftcornerbot[0])/nX/2
dy = (rightcornerup[1] - leftcornerbot[1])/nY/2
centroidsX = np.linspace(leftcornerbot[0]+dx,rightcornerup[0]-dx,nX)
centroidsY = np.linspace(leftcornerbot[1]+dy,rightcornerup[1]-dy,nY)



ClX,ClY = np.meshgrid(centroidsX,centroidsY)
norm_Cl=mpl.colors.Normalize(vmin=0,vmax=nX*nY)
ClMap = cm.ScalarMappable(norm=norm_Cl, cmap=cm.Accent)

Centroids = pd.DataFrame({'X':ClX.flatten(),'Y':ClY.flatten(),'ID':range(nX*nY)})
Centroids['Color'] = Centroids.ID.apply(ClMap.to_rgba)


allQuakes['Class'] =allQuakes.apply(GetClass,args = (Centroids,),axis=1)
allQuakes['Color'] =allQuakes['Class'].apply(ClMap.to_rgba)


fig1,m  =DrawMapEvents(allQuakes,allStations,leftcornerbot=leftcornerbot,
                       rightcornerup=rightcornerup,opacity=  0.9)
                       





m.scatter(ClX,ClY,70,color='white',marker='v',alpha=0.99,zorder=13)

plotly_fig = tls.mpl_to_plotly( plt.gcf() )
plotly_url = py.plot(plotly_fig, filename='mpl-time-series')


length = 5  # in seconds


i=0.0
presentBG = np.zeros(allQuakes.shape[0])
presentNC = np.zeros(allQuakes.shape[0])

        

    
    
    
    
    
    
    
    
    
    
    
   