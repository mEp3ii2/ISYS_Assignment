import csv
from time import sleep
from unidecode import unidecode

# opens the csv and reads in the values to the associated lists
def enterData(cursor):
    csvFile = "complete.csv"
    with open(csvFile,'r') as file:
        csvReader = csv.reader(file)
        next(csvReader)
        for data in csvReader:
            if (data[45] ==  "Individual"):
                ind = list((data[12], #id
                            data[13], #name
                            data[19], #gender
                            data[21], #birth
                            data[28], #death
                            data[23], #cityB
                            data[25], #countryB
                            data[24], #contB
                            data[30], #cityD
                            data[33], #countyrD
                            data[31] #continetD
                            ))
                aff = list((data[48],
                            data[49],
                            data[50],
                            data[51]))
                insertInd(ind,cursor)
                insertAff(aff,cursor)
            elif(data[45]== "Organization"):
                org = list((data[12], #id
                            data[35], #name
                            data[40], #foundingCity
                            data[43], #foundingCountry
                            data[41] #foundingCont                            
                            )) 
                insertOrg(org,cursor)

            prize =list((   data[0], #year
                            data[1], #cat
                            data[5], #prizeAmout
                            data[7])) #awardDate
            
            award = list((  data[8],
                            data[9]))
            insertPrize(prize,cursor)
            insertAwardedTo(award,cursor)

# takes the ind list and cleans the data before running the
# procedure to insert the entry
def insertInd(ind,cursor):
        ind = cleanIndData(ind)
        ind = replaceEmptyWithNull(ind)
        
        for i in range(5,len(ind)):
            if(ind[i] is not None):
                ind[i]= replaceSpecialChars(ind[i])

        checkID = "SELECT 1 FROM Individual WHERE ID = %s"
        cursor.execute(checkID,(ind[0],))
        result = cursor.fetchone()
        if result:
            cursor.execute("SET @indID = %s",(ind[0],))
            cursor.execute("SET @recID = %s",(ind[0],))
        else:
         
            cursor.callproc('insertRecipient',
                        (ind[0],'I'))
        
            cursor.callproc('insertInd',ind)

# takes the aff list and cleans the data before running the
# procedure to insert the entry
def insertAff(aff,cursor):
    for i in range(0,len(aff)): 
        affDets = aff[i].split(',')
        if not all(element == "" for element in affDets):
            for item in affDets:
                item = replaceSpecialChars(item)
            if(len(affDets)==2):
                name= affDets[0]
                country =affDets[1]
            elif (len(affDets)==3):
                name = affDets[0]
                location = affDets[1]
                country = affDets[2]
            elif(len(affDets)==4):
                name = affDets[0]
                location = affDets[1]
                state = affDets[2]
                country = affDets[3]
            elif(len(affDets)==5):
                name = affDets[0]
                location = affDets[1]
                state = affDets[2]
                country = affDets[4]
            elif(len(affDets)==6):
                name = affDets[0]
                location = affDets[2]
                state = affDets[3]
                country = affDets[5]
            else:
                print("Unknown Error!")
                print(affDets)
                print(len(affDets))
            try:
                l = location
            except NameError:
                location = None
            try:
                s = state
            except NameError:
                state = None
            
            checkAff = "SELECT 1 FROM Affiliate WHERE NAME = %s AND Country = %s"
            cursor.execute(checkAff,(name,country,))
            result = cursor.fetchone()
            if not result:
                cursor.callproc('insertAff',(name,country,location,state))
            else:
                cursor.execute("SELECT @recID;")
                result = cursor.fetchone()
                id = result[0]
                cursor.execute("SELECT 1 FROM AffiliatedTo WHERE ID =%s",(id,))
                result = cursor.fetchall() # changed this to fetchall ??? cause it said there was unread results found when it was fetchone
                if not result:
                    cursor.callproc('insertAffTo',(id,name,country))

# takes the org list and cleans the data before running the
# procedure to insert the entry     
def insertOrg(org,cursor):
    org = replaceEmptyWithNull(org)
    for i in range(1,len(org)):
         if (org[i] is not None):
            org[i]= replaceSpecialChars(org[i])
    checkID = "SELECT 1 FROM Organisation WHERE ID =%s"
    cursor.execute(checkID,(org[0],))
    result = cursor.fetchone()
    if not result:
        cursor.callproc('insertRecipient',
                        (org[0],'O'))
        cursor.callproc('insertOrg',org)
    else:
        cursor.execute("SET @recID = %s",(org[0],))

# converts the gender to single char
# adds - into dates
def cleanIndData(ind):
    
    if(ind[2]=="female"):
        ind[2]="F"
    elif(ind[2]=="male"):
        ind[2]="M"
    else:
        ind[2]=None

    birthYear=ind[3].split('-')
    deathYear= ind[4].split('-')
    ind[3]= dateFixer(birthYear)
    ind[4]= dateFixer(deathYear)
    return ind

#  adds default value of 01-01
def dateFixer(dates):
    if(len(dates)>1):
        if (dates[1]=='00'):
            dates[1]= '01'
        if(dates[2]=='00'):
            dates[2]= '01'
    seperator='-'
    dates = seperator.join(dates)
    return dates
#  replace emoty strings with none
def replaceEmptyWithNull(list):
    return [None if item == "" else item for item in list]

# replace special chars with normal one
def replaceSpecialChars(string):    
    return unidecode(string)

# takes prize list and replaces empty string with none before inserting 
# values into table
def insertPrize(prize,cursor):
    prize[0]=prize[0]+"-01-01"
    prize = replaceEmptyWithNull(prize)
    checkPrize = "SELECT 1 FROM Prize WHERE Year = %s AND Category = %s"
    cursor.execute(checkPrize,(prize[0],prize[1],))
    result = cursor.fetchone()
    if result:
        cursor.execute("SET @oYear = %s",(prize[0],))
        cursor.execute("SET @oCategory = %s",(prize[1],))
    else: 
        
        cursor.callproc('insertPrize',prize)

# takes award lit filters out special chars
# before inserting values into table
def insertAwardedTo(award,cursor):
   
    award[1] = replaceSpecialChars(award[1])
    cursor.callproc('insertAwardTo',award)

        


