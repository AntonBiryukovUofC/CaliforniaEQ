import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import obspy
from saveMSEEDEventID_functions import ReadFilterEQandStations,ndToDataframe
pd.set_option('mode.chained_assignment','warn')
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
tls.set_credentials_file(username='Anton.Biryukov', api_key='q0iwsvqelb')
#py.sign_in('Anton.Biryukov', 'q0iwsvqelb')

mag_min = 1.7
npzfile=  np.load('%2.1f.npz' % mag_min)
allQuakes,allStations = ndToDataframe(npzfile)

subset_stations = pd.read_csv('./subsetStations.csv')
subset_stations['Name'] =  subset_stations.Network_Code + '.' + subset_stations.Station_Code
subset_stations['Labels'] =  ["%s - %d" % x for x in zip(subset_stations.Name,subset_stations.NEvents)]


PltlyMapLayout = go.Layout(
            width=1200,
            height=1200,
            hovermode='closest',
             #yaxis = dict(autorange = 'reversed')
            )
PltlyQuakes = go.Scatter(y=allQuakes.LAT,
                       x=allQuakes.LON,
                       mode = 'markers',
                       marker=dict(
                       size='10',
                       opacity=  0.5,
                       color = allQuakes.DEP, #set color equal to a variable
                       colorscale='Viridis',
                       showscale=True),
                       )       
PltlyStations = go.Scatter(y=subset_stations.LAT,
                       x=subset_stations.LON,
                       mode = 'markers+text',
                       marker=dict(
                       size='20',
                       color='red',
                       showscale=False),
                       text = subset_stations.Labels,
                       textfont=dict(
                       family='sans serif',
                       size=15,
                       color='#1f77b4'
                       )
                       )       

data = [PltlyQuakes,PltlyStations]
pltlyfig = go.Figure(data=data,layout = PltlyMapLayout)
    
    
    
    
    
    
    
    
    
    
   