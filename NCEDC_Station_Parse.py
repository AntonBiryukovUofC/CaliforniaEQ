# Parse the website, get the stations infos:
import ftplib

ftp = ftplib.FTP('ncedc.org')
ftp.login()
ftp.cwd('/pub/doc/')
sta_dir_all = ftp.nlst()[0:-5]

allseed=  []

for directory in sta_dir_all:
    sta_dest = '/pub/doc/%s' % directory
    ftp.cwd(sta_dest)
    print 'Changed to %s' % sta_dest
    f_list =ftp.nlst()    
    sta_file = [f_list[i] for i in range(len(f_list)) if f_list[i].endswith('seed')]
    print sta_file
    if len(sta_file) >0 :
        file_seed = './Stations/%s' % sta_file[0]
        ftp.retrbinary("RETR " + sta_file[0] ,open(file_seed, 'wb').write)
        #allseed.append()