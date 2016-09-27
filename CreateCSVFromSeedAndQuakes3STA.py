import pandas as pd
import obspy
from saveMSEEDEventID_functions import DrawMapEvents
allQuakesSubset = pd.read_csv('./quakesOn3Sta.csv')
allStations = pd.read_csv('allStationsOnly.txt',sep = '\s+')
#plot1 = DrawMapEvents(allQuakesSubset,allStations)
sta_triplet = ['ACR','SB4','JKR']
index = 1000
ideq = allQuakesSubset.ix[index].ID

freqmin=5
freqmax=30

BGst = obspy.read('./events/BGevent_%d.mseed' % ideq)
STA1_tr = BGst.select(station=sta_triplet[0]).filter(type='bandpass',
                                                freqmin=freqmin,
                                                freqmax=freqmax)[0]
STA1_tr.trim(starttime = STA1_tr.stats.starttime,
             endtime = STA1_tr.stats.starttime+3.2)
STA1_tr.resample(sampling_rate = 100).normalize().taper(type ='hann',
                                                        max_percentage=0.5)

STA2_tr = BGst.select(station=sta_triplet[1]).filter(type='bandpass',
                                                freqmin=freqmin,
                                                freqmax=freqmax)[0]
STA2_tr.trim(starttime = STA1_tr.stats.starttime,
             endtime = STA1_tr.stats.starttime+3.2)
STA2_tr.resample(sampling_rate = 100).normalize().taper(type ='hann',
                                                        max_percentage=0.5)


STA3_tr = BGst.select(station=sta_triplet[2]).filter(type='bandpass',
                                                freqmin=freqmin,
                                                freqmax=freqmax)[0]
STA3_tr.trim(starttime = STA1_tr.stats.starttime,
             endtime = STA1_tr.stats.starttime+3.2)
STA3_tr.resample(sampling_rate = 100).normalize().taper(type ='hann',
                                                        max_percentage=0.5)

