__author__ = 'Apoorva Chitre'

# Program to merge the contents of two simplified user account tables contained in two seperate databases

import sqlite3
import sys
import os.path as osp

inputList1 = [] #List to store and process inputDB1 data
inputList2 = [] #List to store and process inputDB2 data
outputList = [] #List to store and process outputDB data


# function to find and process common data records in lists for input DB accounts tables and then add them in list for outputDB accounts table

def commonRecords(list1,list2,list3):

    for data in list1:
        if data in list2:
            L = []
            L.append(data[0]+"_old")
            L.append("/home/old_"+data[0])
            L.append(data[2])
            list3.append(L)

    for data in list2 :
        if data in list1:
            L=[]
            L.append(data[0]+"_new")
            L.append("/home/"+data[0]+"_new")
            L.append(data[2])
            list3.append(L)

# function to find and process data records only in list for inputDB1 accounts table and then add them in list for outputDB accounts table

def otherListOneRecords(list1,list2,list3) :

    for data in list1 :
        if data not in list2:
            if data[1] != "None" :
                L = []
                L.append(data[0])
                L.append(data[1])
                L.append(data[2])
                list3.append(L)

# function to find and process data records only in list for inputDB2 accounts table and then add them in list for outputDB accounts table

def otherListTwoRecords(list1,list2,list3):

    for data in list2:
        if data not in list1:
            L =[]
            L.append(data[0])
            L.append(data[1])
            L.append(data[2])
            list3.append(L)

# validating the user input to make sure all db filenames are in the required format
if len(sys.argv) != 4 :
    print("Missing or extra input arguments!")
else:
    if((osp.isfile(sys.argv[1]) and sys.argv[1].endswith(".db")) and (osp.isfile(sys.argv[2]) and sys.argv[2].endswith(".db")) and (osp.isfile(sys.argv[3]) and sys.argv[3].endswith(".db"))):

        db = sqlite3.connect(sys.argv[1]) # connect to the first input DB inputDB1
        curs1 = db.cursor() # create a new cursor

        curs1.execute("select * from accounts order by username desc") # query db table accounts table data to get all records

        inputList1 = curs1.fetchall() # add fetched records to list for processing

        db.commit() # commit changes


        db = sqlite3.connect(sys.argv[2]) # connect to the second input DB inputDB2
        curs2 = db.cursor() # create a new cursor

        curs2.execute("select * from accounts order by username desc")  # query db table accounts table data to get all records

        inputList2 = curs2.fetchall() # add fetched records to list for processing

        # commit changes
        db.commit()

        commonRecords(inputList1,inputList2,outputList) # call to function that process common data records in both db tables

        otherListOneRecords(inputList1,inputList2,outputList) # call to function that process data records that only exist in inputDB1

        otherListTwoRecords(inputList1,inputList2,outputList) # call to function that process data records that only exist in inputDB2


        db = sqlite3.connect(sys.argv[3]) # connect to the output database
        curs3 = db.cursor() # create a new cursor

        curs3.execute("create table accounts (username text, home_directory text, password text)") # create accounts table in output database

        curs3.executemany("insert into accounts(username,home_directory,password) values(?,?,?)",outputList)

        print("Data merged successfully!")

        db.commit()
        db.close() # close connection to DB


    else:
        print("Invalid file types in input!")
        exit()




# Initial database setup and data insertion code

#db = sqlite3.connect("inputDB1.db")
#curs = db.cursor()


#curs.execute("insert into accounts (username,home_directory,password) values ('fred','/home/fred','ksdfjsl')") # use MD5 encyption in final program
#curs.execute("insert into accounts (username,home_directory,password) values ('richard','/home/richard','f8jrst1')")
#curs.execute("insert into accounts (username,home_directory,password) values ('system1','None','ksdfst9')")
#curs.execute("insert into accounts (username,home_directory,password) values ('anne','/home/anne','psdf5er')")

#inputList1 = [["prince","/home/prince","mfh67p42"],["system2","None","ljd45g1w"],
#              ["rose","/home/rose","kih75we3"],["system3","None","ji9rt4w"],["arthur","/home/arthur","hi92r4yu"]] #creating inputList1 for inserting records in inputDB1

#curs.executemany("insert into accounts (username,home_directory,password) values (?,?,?)",inputList1) # inserting list data into inputDB1

#db.commit()
#db.close()

#db = sqlite3.connect("inputDB2.db")

#curs = db.cursor()

#curs.execute("create table accounts (username text, home_directory text, password text)")

#curs.execute("insert into accounts (username,home_directory,password) values ('chris','/home/chris','ksdfjsl')") # use MD5 encyption in final program
#curs.execute("insert into accounts (username,home_directory,password) values ('system2','None','f8jrsu1')")
#curs.execute("insert into accounts (username,home_directory,password) values ('richard','/home/richard','ksdfst1')")
#curs.execute("insert into accounts (username,home_directory,password) values ('tracy','/home/tracy','psdf9er')")

#inputList2 = [["roger","/home/roger","uih3rw1"],["system6","None","yu0i123f"],["tina","/home/tina","hiy3dt5"],
#              ["rose","/home/rose","kih75we3"],["arthur","/home/arthur","hi92r4yu"]] #creating inputList2 for inserting records in inputDB2

#curs.executemany("insert into accounts (username,home_directory,password) values (?,?,?)",inputList2) # inserting list data into inputDB2

#db.commit()
#db.close()

#db = sqlite3.connect("output.db")

#curs = db.cursor()

#curs.execute("create table accounts (username text, home_directory text, password text)")

#db.commit()
#db.close()
