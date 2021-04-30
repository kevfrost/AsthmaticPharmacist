#Script to pull data from openprescribing, compare it with drug dictionary to identify drugs which have high carbon footprint
#To do: add carbon to remainder of devices
#To do: add other WYH 

import requests,json,csv,sys
InhalerNames = []
InhalerIDs = []
InhalerTypes = []
InhalerCarbon = []

def request (drugCode,orgCode):
    RequestString = "https://openprescribing.net/"

    #API code
    RequestString = RequestString + "api/1.0/spending_by_practice/?code=" + drugCode
    
    #Restrict to Bradford Craven CCG
    RequestString = RequestString + "&org="+orgCode

    #Format
    RequestString = RequestString + "&format=json"

    response = requests.get(RequestString)
    print(RequestString)
    print(response.status_code)

    return(response)

# E54000005 is WYH 0 not picking up, e-mailed
# Or is QWO the code? Looks like it, will need to export to csv to see
# 36J is B&C CCG
#https://openprescribing.net/analyse/#org=CCG&numIds=0301011R0AAAAAA,0301011R0AAADAD,0301011R0AAAFAF,0301011R0AAAPAP,0301011R0AAAQAQ,0301011R0AABUBU,0301011R0AABZBZ,0301011R0AACBCB,0301011R0AACCCC,0301011R0BEAHAQ,0301011R0BEAIAP,0301011R0BEAPAV,0301011R0BIAFAP,0301011R0BIAGBU,0301011R0BIAHAP,0301011R0BJ,0301011R0BK,0301011R0BL,0301011R0BM,0301011R0BT,0301011R0BW,0301011R0BX,0301011R0BY,0301011R0BZ,0301011V0AABBBB,0301011V0BBADAA,0301011V0BBARBB&denomIds=0301011R0AAAAAA,0301011R0AAADAD,0301011R0AAAFAF,0301011R0AAAPAP,0301011R0AAAQAQ,0301011R0AABUBU,0301011R0AABZBZ,0301011R0AACBCB,0301011R0AACCCC,0301011R0BEAHAQ,0301011R0BEAIAP,0301011R0BEAPAV,0301011R0BIAFAP,0301011R0BIAGBU,0301011R0BIAHAP,0301011R0BJ,0301011R0BK,0301011R0BL,0301011R0BM,0301011R0BT,0301011R0BW,0301011R0BX,0301011R0BY,0301011R0BZ,0301011V0AABBBB,0301011V0BBADAA,0301011V0BBARBB,0302000C0,0302000K0AAAAAA,0302000K0AAADAD,0302000K0AAAGAG,0302000K0AAAHAH,0302000K0AAAKAK,0302000K0AAALAL,0302000K0AAAMAM,0302000K0AAAUAU,0302000K0AAAVAV,0302000K0AAAWAW,0302000K0AAAZAZ,0302000K0AABABA,0302000K0AABBBB,0302000K0BBADAD,0302000K0BBAEAA,0302000K0BBAHAG,0302000K0BBAIAH,0302000K0BBAKAK,0302000K0BBAMAZ,0302000K0BBANBA,0302000K0BD,0302000K0BF,0302000K0BG,0302000K0BH,0302000K0BI,0302000N0AAAAAA,0302000N0AAADAD,0302000N0AAAEAE,0302000N0AAAFAF,0302000N0AAAPAP,0302000N0AAARAR,0302000N0AAASAS,0302000N0AAATAT,0302000N0AAAUAU,0302000N0AAAXAX,0302000N0AAAYAY,0302000N0AAAZAZ,0302000N0AABABA,0302000N0AABCBC,0302000N0AABEBE,0302000N0AABFBF,0302000N0AABGBG,0302000N0AABHBH,0302000N0AABJBJ,0302000N0AABKBK,0302000N0AABLBL,0302000N0AABPBP,0302000N0AABQBQ,0302000N0BBAAAA,0302000N0BBACAC,0302000N0BBAEAE,0302000N0BBAFAF,0302000N0BBARAR,0302000N0BBASAS,0302000N0BBATAT,0302000N0BBAUAU,0302000N0BBAYBA,0302000N0BBBABC,0302000N0BBBBBH,0302000N0BC,0302000N0BD,0302000N0BF,0302000N0BG,0302000N0BH,0302000N0BI,0302000N0BJ,0302000N0BK,0302000N0BL,0302000N0BM,0302000R0,0302000U0,0302000V0&selectedTab=map

#Drug = "0301011R0AABUBU"
#Org = "QWO" #WYH broken
#Org = "B82020" #Crosshills
        

Org = "36J" #B&C

with open('Antibiotics.csv', newline='') as csvfile:
    DrugFile = csv.reader(csvfile, delimiter=',',)
    next(DrugFile)
    for row in DrugFile:
        if row[3] != "Non-inhaler":
            
            InhalerName= row[2]
            InhalerID = row [0]
            Type = row [3]

            InhalerNames.append(InhalerName)
            InhalerIDs.append(InhalerID)
            InhalerTypes.append(Type)

#For Each drug in the CSV file, pull the data and add it to output csv.
for Drug in InhalerIDs:
    


        ResponseFromAPI=request(Drug,Org);
        #print("Request function says: "+str(ResponseFromAPI.status_code))
        #print(ResponseFromAPI.json());


                  

        #Write to CSV
        R = ResponseFromAPI.json()
        LengthofR =len(R)

        if(len(R)== 0):
            print("no entries returned")
        else:
            i=0
            while i<LengthofR:
                    R[i]['drugid']=Drug
                    R[i]['Inhaler Name']=InhalerNames[InhalerIDs.index(Drug)]
                    R[i]['Device Type']=InhalerTypes[InhalerIDs.index(Drug)]
                    i+=1

            with open('output.csv', 'a', newline='') as file:
                fieldnames = R[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()
                i=0
                while i<LengthofR:
                    writer.writerow(R[i])
                    i+=1
