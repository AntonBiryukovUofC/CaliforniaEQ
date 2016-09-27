import pandas as pd
import obspy
import numpy as np
from saveMSEEDEventID_functions import DrawMapEvents,ExtractDataFromSeedID



allQuakesSubset = pd.read_csv('./quakesOn3Sta.csv')
allStations = pd.read_csv('allStationsOnly.txt',sep = '\s+')
#plot1 = DrawMapEvents(allQuakesSubset,allStations)
sta_triplet = ['ACR','SB4','FUM']

# Do for one index :
CSVObservations = []
LatLonDep = []
allQuakesSubset.index = range(allQuakesSubset.shape[0])
for index,row in allQuakesSubset.iterrows():
    ideq = row.ID
    BGst = obspy.read('./events/BGevent_%d.mseed' % ideq)

    rowInCsv = ExtractDataFromSeedID(ideq,sta_triplet=sta_triplet)
    if rowInCsv == None:
        print 'The event is missing - the record is too short ' 
    else:
        CSVObservations.append(rowInCsv)
        LatLonDep.append([row.LAT,row.LON,row.DEP])
    print 'Processing row %d , done %3.2f percent' % (index,100.0*index/allQuakesSubset.shape[0])

print 'Saving CSV with Observations'
Obs = np.zeros((len(CSVObservations),960))
for i,item in enumerate(CSVObservations):
    Obs[i,:] = item

CSVObsDF = pd.DataFrame(data = Obs[0:,0:],columns = range(960))
CSVObsDF.to_csv('ObservationsTriplet.csv')

LatLonDepArray  =np.array(LatLonDep)
print 'Saving CSV with Labels'

LabelsDF = pd.DataFrame({'LAT':LatLonDepArray[:,0],'LON':LatLonDepArray[:,1],'DEP':LatLonDepArray[:,2]})
LabelsDF.to_csv('LabelsTriplet.csv')





