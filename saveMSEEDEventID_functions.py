
def saveWaveformsByID(eventID =71697735,network = 'BG',stations = ['SQK','STY','DRK','INJ','SB4'],
                      dest_name = './events/%s%d.mseed' % ('BG',71697735),
                      starttime ='2011-12-22T01:17:56.485000Z',
                    endtime = '2011-12-22T01:17:58.485000Z'):
    import urllib
    event_str  = 'eventid=%d' % eventID    
    network_str = 'network=%s' % network
    stations_str = 'station=%s' % (','.join(stations))
    #&starttime=2011-12-22T01:17:56.485000&endtime=2011-12-22T01:17:57.485000&eventid=71697735
    query = "http://service.ncedc.org/ncedcws/eventdata/1/query?%s&%s&%s&%s&%s"
    starttime_str = 'starttime=%s' % starttime.format_iris_web_service()
    endtime_str = 'endtime=%s' % endtime.format_iris_web_service()
    
    url =query % (network_str,starttime_str,
                  endtime_str,stations_str, event_str)
    url.replace('\\', '/')
    #print url
    urllib.urlretrieve(url, dest_name)
    #print 'Success'
    #data = urllib.request.urlopen(url)
    return url
    
def saveQuakeMLByID(eventID =71697735,dest_name = './events/%s%d.xml' % ('',71697735)):
    import urllib
    event_str  = 'eventid=%d' % eventID    
    #&starttime=2011-12-22T01:17:56.485000&endtime=2011-12-22T01:17:57.485000&eventid=71697735
    #http://service.ncedc.org/fdsnws/event/1/query?catalog=NCSS&eventid=71697735&&
    query = "http://service.ncedc.org/fdsnws/event/1/query?%s&%s&%s&%s"
    
    catalog_str = 'catalog=NCSS'
    include_str = 'includeallmagnitudes=false&includearrivals=true&includemechanisms=false'
    order_str = 'orderby=time&format=xml'
    
    
    url =query % (catalog_str,event_str,include_str,order_str)
    url.replace('\\', '/')
    #print url
    urllib.urlretrieve(url, dest_name)
    #print 'Success'
    #data = urllib.request.urlopen(url)
    return url    

def toUTC(date_list):
    import obspy
    strUTC = obspy.UTCDateTime('%d-%02d-%02dT%02d:%02d:%2.3f' % tuple(date_list))
    return strUTC

def ReadFilterEQandStations(parent_dir = './events/', cutoff = 200, mag_min=2.0):
    import pandas as pd
    import obspy
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
    allQuakes = allQuakes[(allQuakes.EZ < cutoff) & (allQuakes.EZ > 0) & 
                            (allQuakes.EX < cutoff) & (allQuakes.EX > 0) &
                             (allQuakes.EY < cutoff) & (allQuakes.EY > 0) &
                             (allQuakes.LAT>38.78) & (allQuakes.LAT<38.84)
                             & (allQuakes.LON< -122.72) & (allQuakes.LON> -122.86) &
                              (allQuakes.MAG > mag_min) ]
    allQuakes['UTCDT'] =  allQuakes.iloc[:,0:6].apply(toUTC,axis=1)
    date_cutoff = obspy.UTCDateTime(2003,05,1)
    allQuakes = allQuakes[allQuakes.UTCDT > date_cutoff]
    return allQuakes,allStations

def DrawMapEvents(allQuakes,allStations ,
                  leftcornerbot =[-122.86,38.78-0.0001],
                  rightcornerup = [-122.72,38.84+0.0001],opacity = 0.25):
                      
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap

    #import pandas as pd
    import numpy as np
    w = 15
    h = 15
    fig = plt.figure(figsize = (w,h))
    m = Basemap(llcrnrlon=leftcornerbot[0],llcrnrlat=leftcornerbot[1],
                urcrnrlon=rightcornerup[0],urcrnrlat=rightcornerup[1],
                lat_0 = allQuakes.LAT.mean(),lon_0=allQuakes.LON.mean(),
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
    m.scatter(allQuakes.LON,allQuakes.LAT,30,color=allQuakes.Color,marker='o',alpha=opacity,zorder=10)
    
    # Filter out the stations:
    allStations = allStations[(allStations.LAT>38.78) & (allStations.LAT<38.84) &
                              (allStations.LON< -122.72) & (allStations.LON> -122.86) 
                              ]
    m.scatter(allStations.LON,allStations.LAT,60,color='b',marker='v',alpha=0.99,zorder=10)
    allStations['Name'] =  allStations.Network_Code + '.' + allStations.Station_Code
    for label,x,y in zip(allStations.Name,allStations.LON,allStations.LAT):
        plt.annotate(label,xy = (x,y), bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),zorder=11)
        
    return fig,m