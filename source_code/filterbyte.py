import os
import subprocess
import sys

def main():
    targetdir = "bin/"                                                   # binary file save location
    samplelist = os.listdir(targetdir)
    bytedir = "byte/"                                                    # save location of new converted byte file
    xxdcmd = "xxd -c 16 -g 1 "
    if not os.path.isdir(bytedir):                                       # check save location dir exist
        subprocess.check_output("mkdir "+bytedir,shell=True)
    existfilelist = os.listdir(bytedir)                                  # check and import list of already converted file
    for rawindex in range(0,len(existfilelist)):
        existfilelist[rawindex] = existfilelist[rawindex].split(".")[0]
    count = 0
    for name in samplelist:
        orifilename = name.split(".")[0]                                 # name = xxx.<extname>, orifilename = xxx
        existflag = 0
        for existname in existfilelist:                                  # if there are multiple diretory, check file in new directory exist in old directory or not
            if existname == orifilename:
                existflag = 1
        if existflag == 0:                                               # if file has already converted, it will not convert again
            if os.path.isfile(targetdir+name):
                outfile = open(bytedir+orifilename+".byte",'a',encoding='UTF-8')  # bytefile name = xxx.byte
                cmdresult = str(subprocess.check_output(xxdcmd+targetdir+name, shell=True)).split("\\n")
                for index in range(0,len(cmdresult)-1):
                    retstr = ""
                    if index == 0:
                        tmpstr = cmdresult[0].replace("b'","")
                        splitstr = tmpstr.split(" ")
                        retstr = splitstr[0]
                        for index in range(1,17):
                            retstr += " "+splitstr[index]
                    else:
                        splitstr = cmdresult[index].split(" ")
                        retstr = splitstr[0]
                        if len(splitstr) < 17:
                            for inn in range(1,len(splitstr)):
                                if len(splitstr[inn]) == 2:
                                    partstr = splitstr[inn]
                                    hexjudge = judgerule(partstr)
                                    if hexjudge:
                                        retstr += " "+splitstr[inn]
                        else:
                            for inn in range(1,17):
                                if len(splitstr[inn]) == 2:
                                    partstr = splitstr[inn]
                                    hexjudge = judgerule(partstr)
                                    if hexjudge:
                                        retstr += " "+splitstr[inn]
                    if index == len(cmdresult)-2:
                        outfile.write(retstr)
                    else:
                        outfile.write(retstr+"\n")
                count += 1
                print(count,"-st sample finish ="+name)
                outfile.close()
                    
def judgerule(rawstr):
    retbool = False
    flag1 = False
    flag2 = False
    for index in range(0,2):
        if (rawstr[index] >= '0' and rawstr[index] <= '9') or (rawstr[index] >= 'a' and rawstr[index] <= 'f'):
            if index == 0:
                flag1 = True
            elif index == 1:
                flag2 = True
    retbool = retbool or (flag1 and flag2)
    return retbool

if __name__ == "__main__":
    main()
