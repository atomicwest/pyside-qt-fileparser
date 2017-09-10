'''
assumptions:
- all parsed target filenames will have . delimiters
- incomplete ranges will be revealed with the UI message box

#store information about filenames as a list
#where the list[0] is the count of files in the range
#list[-2] is a list of the frame numbers, allowing for checking incomplete ranges
#list[-1] is the extension
'''

def formatFilenames(filenames):
    numfiles = {}
    for f in filenames:
        
        parsef = f.split(".")
        namestring = ""
        
        for i in range(-len(parsef),-2):
            namestring+=parsef[i]
            namestring+="."
        
        if f.count(".") <= 1:
            numfiles[f] = [f]
        elif namestring in numfiles.keys():
            numfiles[namestring][0]+=1
            numfiles[namestring][1].append(parsef[-2])
        else:
            numfiles[namestring] = [1,[parsef[-2]], parsef[-1]]

            
    for k in numfiles.keys():
        if len(numfiles[k]) > 1:
            fname = k
            padding = str(len(numfiles[k][1][0]))
            ext = numfiles[k][2]
            
            #doesn't track incomplete ranges
            firstf = str(int(numfiles[k][1][0]))
            lastf = str(int(numfiles[k][1][-1]))
            frange = "%s-%s" % (firstf,lastf)
            
            if len(padding)==1:
                padding = "0"+padding
            collapsename = fname + "%" + "%sd.%s %s" % (padding,ext,frange)
            numfiles[k].append(collapsename)
        
    lists = []
        
    for k in numfiles.keys():
        #print numfiles[k][-1]
        #lists.append((k,numfiles[k][-1]))
        lists.append(numfiles[k][-1])
    
    lists.sort()
    
    return lists
