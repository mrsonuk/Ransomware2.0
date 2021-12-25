import sys
import json
import subprocess
import os

def main():
    # basic setting
    VTreport = str(sys.argv[1])            # VirusTotal reports saving name	
    reportpath = "report/"                 # path of virustotal reports
	if os.path.isfile(reportpath+VTreport):
        targetfile = reportpath+VTreport   # Complete VirusTotal reports path | one json contains multiple files report (at least 300 files report)
    labelfilespath = "label/"              # prepared label saving position
    
    # counter for testing
    totalcount = 0
    
    logfile = open(labelfilespath+VTreport+"_label_record.txt",'a',encoding='UTF-8')             # open file to log file label
    # filter name from json report
    with open(targetfile,'r',encoding="UTF-8") as file:   # open VirusTotal report (json format)
        content = json.load(file)
    for intend in range(0,len(content['data'])):
        hashname = content['data'][intend]['id']
        mainitem = content['data'][intend]['attributes']['last_analysis_results']
        avresult = content['data'][intend]['attributes']['last_analysis_results']['Kaspersky']['result']
        count = 0                                                                # check our wanted malware type
        
        for each in mainitem:                                                    # Only want type = ransom , if need other types, please modify manually
            if not mainitem[each]['result'] == None:
                if 'Ransom' in mainitem[each]['result']:
                    count += 1
                elif 'ransom' in mainitem[each]['result']:
                    count += 1
        if count > 0:                                                            # ransom
            if avresult == None:
                label = 11                                                       # label = 11 = no result in Kaspersky = ransom judged by other AV vendor
            else:
                label = filterlabel(avresult)                                    # label = 0 = error in normal labeling for Kaspersky in this response
            logfile.write(hashname+","+str(label-1)+"\n")                        # record value label-1, ie, range = [0~9], this will be convenient for ML processing  
            logfile.flush()
        totalcount += 1
    print("Total sample in json report:",totalcount)
    logfile.close()
    # labeling
    
    

def filterlabel(rawresult):
    seplist = rawresult.split(".")
    label = 0
    if seplist[0] == "HEUR:Trojan-Ransom":
        if seplist[-2] == "Blocker" and seplist[-1] == "gen":
            label = 6
        elif seplist[-2] == "Gen" and seplist[-1] == "gen":
            label = 7
        elif seplist[1] = "Win32" and seplist[-1] == "vho":
            label = 9
        else:
            label = 10
    elif seplist[0] == "Trojan-Ransom" and seplist[1] == "Win32":
        if seplist[2] == "Blocker":
            label = 1
        elif seplist[2] == "GandCrypt":
            label = 2
        elif seplist[2] == "Foreign":
            label = 3
        elif seplist[2] == "PornoBlocker":
            label = 4
        elif seplist[2] == "Wanna":
            label = 5
        else:
            label = 10
    elif seplist[0] == "Trojan-Ransom" and seplist[1] == "PHP":
        label = 8
    else:
        label = 10
    return label
    

if __name__ == "__main__":
    main()
