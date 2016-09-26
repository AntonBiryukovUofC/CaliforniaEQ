import obspy
from obspy.io.xseed import Parser
import pandas as pd
import glob

list_seed = glob.glob('.\\Stations\\*.seed')
StationsCSV_all = pd.DataFrame()
for file_seed in list_seed:
    try:
        parser = Parser(file_seed)
    except:
        print 'Error on %s ' % file_seed
    print ' Working on %s' % file_seed
    parser_entries =parser.get_inventory()
    StationsCSV = pd.DataFrame(parser_entries['channels'])
    StationsCSV_all = pd.concat((StationsCSV,StationsCSV_all))
StationsCSV_all.to_csv('allStations.csv')