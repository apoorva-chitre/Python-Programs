# Program to validate a data file with credit card transactions and output a formatted report of valid transactions

import os
import re
import sys
import time


amexData = [] # list to store valid amexCard transactions
mcData = [] # list to store valid MasterCard transactions
visaData = [] # list to store valid VisaCard transactions


#function to check and extract valid data from the input file read

def validTransactions(line):

    validRecord = []
    correctDate = ""

    nameMatcher = re.compile(r"(?P<fname>[a-zA-Z]+)\ (?P<mname>[a-zA-Z]?\.?\ )?(?P<lname>[a-zA-Z]+[\-|\ ]?[a-zA-Z]+\ ?(?:[JS]r|III?|IV)?\.?)") # regex to extract valid name

    dateMatcher1 = re.compile(r"(?P<month>Jan(\.?|uary)|Feb(\.?|ruary)|Mar(\.?|ch)|Apr(\.?|il)|May|Jun(\.?|e)|Jul(\.?|y)|Aug(\.?|ust)|Sep(\.?|tember)|Oct(\.?|ober)|Nov(\.?|ember)|Dec(\.?|ember))\ (?P<day>0?[1-9]|[12][0-9]|3[01])[\,|\ ]\ ?(?P<year>19|20[0-9]{2})" ) # regex to extract valid date
    dateMatcher2 = re.compile(r"(?P<month>0?[1-9]|1[012])[\/|-](?P<day>0?[1-9]|[12][0-9]|3[01])[\/|-](?P<year>19[789][0-9]|20(?:0[0-9]|1[0-6])|[789][0-9]|0[0-9]|1[0-6])") # regex to extract valid date

    amountMatcher = re.compile(r"(?P<dls>\$0?[0-9]+)\.?(?P<cts>[0-9]{2})?") # regex to extract valid amount

    visaMatcher = re.compile(r"(?P<v1>4[0-9]{3})[\ |\-]?(?P<v2>[0-9]{4})[\ |\-]?(?P<v3>[0-9]{4})[\ |\-]?(?P<v4>[0-9]{4})$") # regex to extract valid visa cc number
    mcMatcher = re.compile(r"(?P<m1>5[1-5][0-9]{2}|2(2[2-9]\d|[3-6]\d\d|7([0-1]\d|2[0-1])))[\ |-]?(?P<m2>[0-9]{4})[\ |-]?(?P<m3>[0-9]{4})[\ |-]?(?P<m4>[0-9]{4}$)") # regex to extract valid mastercard cc number
    amexMatcher = re.compile(r"(?P<a1>3[47][0-9]{2})[\ |-]?(?P<a2>[0-9]{6})[\ |-]?(?P<a3>[0-9]{5})$") # regex to extract valid amex cc number

    # extracting valid name from each line
    matchName = nameMatcher.search(line)
    if matchName :
        fname = matchName.group('fname')
        mname = matchName.group('mname')
        lname = matchName.group('lname')
        if mname == None :
            mname = ""

    else:
        print("Invalid name format!")

    # extracting valid date from each line
    matchDate1 = dateMatcher1.search(line)
    matchDate2 = dateMatcher2.search(line)
    if matchDate1 :
        month = matchDate1.group('month')
        day = matchDate1.group('day')
        year = matchDate1.group('year')
        #print(month,day,year)
    elif matchDate2 :
        month = matchDate2.group('month')
        day = matchDate2.group('day')
        year = matchDate2.group('year')
        #print(month,day,year)
    else:
        print("Invalid date format!")


    # extracting valid amount from each line
    matchAmt = amountMatcher.search(line)
    if matchAmt :
        dollars = matchAmt.group('dls')
        cents = matchAmt.group('cts')
        if cents == None :
            cents = "00"
    else:
        print("Invalid amount format!")

    # extracting valid cc number from each line
    matchVisa = visaMatcher.search(line)
    matchMC = mcMatcher.search(line)
    matchAmex = amexMatcher.search(line)

    if matchVisa :
        cc1 = matchVisa.group('v1')
        cc2 = matchVisa.group('v2')
        cc3 = matchVisa.group('v3')
        cc4 = matchVisa.group('v4')


    elif matchMC :
        cc1 = matchMC.group('m1')
        cc2 = matchMC.group('m2')
        cc3 = matchMC.group('m3')
        cc4 = matchMC.group('m4')

    elif matchAmex:
        cc1 = matchAmex.group('a1')
        cc2 = matchAmex.group('a2')
        cc3 = matchAmex.group('a3')

    else :
        print("Invalid CC number format!")


    # converting dates in proper format using the function defined for it

    if matchDate1 or matchDate2 :
        correctDate = formatDate(month,day,year)

    # storing individual pieces of data into one record for each customer and
    # then storing each record in respective lists for card companies

    if matchName and (matchDate1 or matchDate2) and matchAmt and matchAmex :
        validRecord.append(fname)
        validRecord.append(mname)
        validRecord.append(lname)
        validRecord.append(correctDate[0])
        validRecord.append(correctDate[1])
        validRecord.append(correctDate[2])
        validRecord.append(dollars)
        validRecord.append(cents)
        validRecord.append(cc1)
        validRecord.append(cc2)
        validRecord.append(cc3)
        amexData.append(validRecord)

    if matchName and (matchDate1 or matchDate2) and matchAmt and matchVisa :
        validRecord.append(fname)
        validRecord.append(mname)
        validRecord.append(lname)
        validRecord.append(correctDate[0])
        validRecord.append(correctDate[1])
        validRecord.append(correctDate[2])
        validRecord.append(dollars)
        validRecord.append(cents)
        validRecord.append(cc1)
        validRecord.append(cc2)
        validRecord.append(cc3)
        validRecord.append(cc4)
        visaData.append(validRecord)

    if matchName and (matchDate1 or matchDate2) and matchAmt and matchMC :
        validRecord.append(fname)
        validRecord.append(mname)
        validRecord.append(lname)
        validRecord.append(correctDate[0])
        validRecord.append(correctDate[1])
        validRecord.append(correctDate[2])
        validRecord.append(dollars)
        validRecord.append(cents)
        validRecord.append(cc1)
        validRecord.append(cc2)
        validRecord.append(cc3)
        validRecord.append(cc4)
        mcData.append(validRecord)

    print(validRecord)

# function to format date as per report format

def formatDate(month,day,year) :

    #To replace different month formats to one required format

    if month == "Jan." or month == "Jan" or month == "January" :
        month = "01"

    if month == "Feb." or month == "Feb" or month == "February" :
        month = "02"

    if month == "Mar." or month == "Mar" or month == "March" :
        month = "03"

    if month == "Apr." or month == "Apr" or month == "April" :
        month = "04"

    if month == "May" :
        month = "05"

    if month == "Jun." or month == "Jun" or month == "June" :
        month = "06"

    if month == "Jul." or month == "Jul" or month == "July" :
        month = "07"

    if month == "Aug." or month == "Aug" or month == "August" :
        month = "08"

    if month == "Sep." or month == "Sep" or month == "September" :
        month = "09"

    if month == "Oct." or month == "Oct" or month == "October" :
        month = "10"

    if month == "Nov." or month == "Nov" or month == "November" :
        month = "11"

    if month == "Dec." or month == "Dec" or month == "December" :
        month = "12"


    #for zero padding day of the date

    if len(day) != 2 :
        day = "0"+day

    # for converting YY format to YYYY in range 1970-2016

    if len(year) != 4 and 70<=int(year)<=99 :
        year = "19"+year
    elif len(year) != 4 and 00<=int(year)<=16:
        year = "20"+year

    return [month,day,year]


# condition to check valid file is read or not

if len(sys.argv) != 2 :
    print("Error: missing or extra inputs!")
else:
    if os.path.isfile(sys.argv[1]) :
        try:
            fileobj = open(sys.argv[1],"r")
            lines = fileobj.readlines()
            fileobj.close()
            print("-----------------------------Transactions Analyzer------------------------------")
            print()
            print("Reading Transactions..............")
            time.sleep(3)
            print()
            time.sleep(2) # Delays for displaying step by step output
            for line in lines:
                validTransactions(line)
            print()
            time.sleep(2)
            print("Valid transactions read successfully!")
            print()
            time.sleep(2)
            print("Generating report..............")
            time.sleep(5)
            print()

            #sorting the data based on given criterion

            amexData = sorted(amexData,key = lambda x: (x[5],x[3],x[4],x[2],x[6],x[7]))
            mcData = sorted(mcData,key = lambda x: (x[5],x[3],x[4],x[2],x[6],x[7]))
            visaData = sorted(visaData,key = lambda x: (x[5],x[3],x[4],x[2],x[6],x[7]))

            #Printing the Transactions Report in required format

            print("Customer Name","Transaction Date","Amount","Credit Card Number",sep="  \t  ")
            print()
            print("---------------------------------Amex-------------------------------------------")
            for i in amexData :
                print(i[2]+","+i[0]+" "+i[1],i[3]+"/"+i[4]+"/"+i[5],i[6]+"."+i[7],i[8]+" "+i[9]+" "+i[10],sep="  \t  ")
            print("-------------------------------MasterCard---------------------------------------")
            for i in mcData :
                print(i[2]+","+i[0]+" "+i[1],i[3]+"/"+i[4]+"/"+i[5],i[6]+"."+i[7],i[8]+" "+i[9]+" "+i[10]+" "+i[11],sep="  \t  ")
            print("----------------------------------Visa------------------------------------------")
            for i in visaData :
                print(i[2]+","+i[0]+" "+i[1],i[3]+"/"+i[4]+"/"+i[5],i[6]+"."+i[7],i[8]+" "+i[9]+" "+i[10]+" "+i[11],sep="  \t  ")
            print()

        except BaseException as e:
            print("Error:",e)
            sys.exit()







