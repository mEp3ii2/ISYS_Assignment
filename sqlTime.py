import getpass
import os
import readCsv
import time
import mysql.connector
from prettytable import PrettyTable

# attempts to login to the mysql database
def login():
    os.system('clear')
    password = getpass.getpass("Enter your password: ") # get user to enter the password
    try:
        db_config = {
            "host": "localhost",
            "user": "me",
            "password": password,
            "database": "dswork",
            "charset" :"utf8mb4"
        }
        connection = mysql.connector.connect(**db_config) # connect to mysql
    except mysql.connector.Error as e:
        print("Error connecting to MySQL: " + str(e))
        print("Please restart the application and try again")
    else:
        print("Connected to MySQL")
        return connection

# takes a list of sql statements and runs them 1 at a time
def execute_sql_statements(cursor, sql_statements):
    for sql_statement in sql_statements:
        if sql_statement.strip():  # Check if the statement is not empty
            cursor.execute(sql_statement)
            row = cursor.fetchone()
            while row is not None: # if we somehow get a return
                print(row)
                row = cursor.fetchone()
            for result in cursor.stored_results(): #just in case
                for row in result.fetchall():
                    print(row)

# loads in sql scripts for tables, procedures triggers
# then loads the data and calls the menu for the user to use
def driver():
    connection = login()
    if connection:
        cursor = connection.cursor()
        delTables = "sql/delTables.sql"
        tables = "sql/nobelTables.sql"
        delprocs = "sql/delProc.sql"
        procedure = "sql/procedures.sql"
        trigger = "sql/triggers.sql"
        views = "sql/views.sql"
        delop = "sql/delOps.sql"
        indexes = "sql/indexes.sql"
        fileLoader(cursor,delTables)
        fileLoader(cursor,tables)
        fileLoader(cursor, delprocs)
        loadMultiStatementFiles(cursor,trigger)
        loadMultiStatementFiles(cursor, procedure)
        fileLoader(cursor,views)
        fileLoader(cursor,delop)
        fileLoader(cursor,indexes)
        readCsv.enterData(cursor)
        question(cursor)
        connection.commit()
        cursor.close()
        connection.close()

# read a sql script into a list and exports to the execute func
def fileLoader(cursor, sourceFile):
    with open(sourceFile, 'r') as file:
        sqlCommand = file.read()

    sql_statements = sqlCommand.split(';') # split on a semi colon for end of query
    for sql_statement in sql_statements:
        if sql_statement.strip():  # Check if the statement is not empty
            sql_statement=sql_statement+";" # add back the semi colon cause spliting on the semi colon means its not included
    execute_sql_statements(cursor, sql_statements)

# read a sql script into a list and exports to the execute func
# but for sql scripts that have a multi statement
def loadMultiStatementFiles(cursor,sourceFile):
    with open (sourceFile,'r') as file:
        sqlCommand = file.read()
    sql_statements = sqlCommand.split('-- end here') # split on this so that commands with multiple ; are not broken apart
    execute_sql_statements(cursor, sql_statements)   

# displays a menu to the user
# takes a user input and runs a question 
# or does a database operation
def question(cursor):
    os.system('clear')
    questions ="sql/questions.sql"
    with open (questions,'r') as file:
        sqlCommand = file.read() #read in the question queries 
    sql_statements = sqlCommand.split('-- ends here')
    run = True    
    while run:
        print("""Select a query to run:                     
              1: How many physics awards have been given out 
              2: The different categories of the nobel prize
              3: Average age of a nobel laureate
              4: Amount of women who have won a nobel prize per category
              5: Rankings of the top ten affiliates
              6: Organisations by category
              7: Summary of nobel prizes for the last year of awards
              8: Youngest and oldest nobel prize winner by cat
              9: All current living nobel prize winners
              10: Top five winners count 
              11: Database Operations 
              x : to exit""") # print menu to the user 
        sel = input("Selection: ") # prompt for user to input selection
        if(numChecker(sel)): # validate input 
            sel = int(sel)
            if(sel != 11):
                os.system('clear')
                sel = int(sel) -1
                if (sel != 0):
                    cursor.execute(sql_statements[sel]) # execute the chose question 
                    result = cursor.fetchall()
                    headers = [header[0] for header in cursor.description] # use pretty tables to display results nicely
                    tables = PrettyTable(headers)
                    for row in result:
                        tables.add_row(row)
                    print(tables)
                    time.sleep(1) # add a litte delay
                else:
                    outVal = None
                    cursor.execute("CALL CountPhysicsAwards(@physicsAwardCount);") # yes is yucky but it works
                    cursor.execute("SELECT @physicsAwardCount;") # get the return val 
                    outVal = cursor.fetchone()[0]
                    table = PrettyTable() # display results
                    table.field_names =["Physics Award Count"]
                    table.add_row([outVal])
                    table.align["Physics Award Count"] = "1"
                    print(table)   
            else:  # user wihses to perform database operations
                os.system('clear')
                dbOps(cursor)
        elif(sel == 'x'): #user has chosen to exit 
            run = False
        else:
            os.system('clear')
            print("Invalid Input")

# was originally designed to allow the user to interact 
# with all the tables but this proved to ambitious
# code has been left commented out for later versions to hopefully be re implemented
# just calls the tableOps function using the individual table
def dbOps(cursor):
    # cursor.execute("""SELECT TABLE_NAME
    #                 FROM information_schema.tables
    #                 WHERE TABLE_SCHEMA = 'dswork'  -- Replace with your actual database name
    #                 AND TABLE_TYPE = 'BASE TABLE';
    #                 """)
    # result = cursor.fetchall()
    # run = True
    # while run:
    #     print("Select a table to modify: ")
    #     for table in result:
    #         print(table[0])
    #     sel = input("Enter the table you want to operate with: ")
    #     tableNames = [table[0] for table in result]
    #     if sel in tableNames:
    tableOps(cursor, 'Individual')
        # elif(sel == 'x'):
        #     print("returning to previous menu")
        #     run = False
        # else:
        #     print("Invalid Selection try again")
        # time.sleep(2)
        # run= False

# prompts the user for an input from 1-3 to pick there databse operation on the table
def tableOps(cursor, tableName):
    print("""What would you like to do to the indivdual table:
            1. Insert 
            2. Delete
            3. Update""") # display options to the user 
    sel = input("Selection: ") # get the users input for selection
    try:
        sel =int(sel) # atempt to cast to int 
        if(1<= sel <= 3): # check input within range for the valid options
            if sel == 1:
                tabInsert(cursor,tableName) 
            elif sel == 2:
                tabDel(cursor,tableName)
            elif sel == 3:
                tabUp(cursor,tableName)
        else:
            raise ValueError("Value must be between 1-3")
    except Exception as e:
        print(f"Error: {e}")

# takes user inputs for a new entry into the table and inserts it   
def tabInsert(cursor,tableName):
    vals =[]
    try:
        cursor.execute(f"DESC {tableName}") # get table columns
        columns = cursor.fetchall()
        print(F"Insert values into {tableName}")
        for column in columns:
            print("Enter value")
            sel = input(f"{column[0]}: ") # print the column name to indicate to user what value to provide for insertion
            vals.append(sel)
        vals =readCsv.replaceEmptyWithNull(vals) #convert empty strings to None value
        proc = getIns(tableName)
        cursor.callproc('insertRecipient',(vals[0],'I')) # insert
        cursor.callproc(str(proc),vals)
        print(f"{vals[1]} has been insert Successfull\n")
    except mysql.connector.Error as e:
        print(f"A SQL error occured {e}")
    except Exception as e:
        print(f"An error occured {e}")

# takes a user input id to delete the matching entry in the table
def tabDel(cursor, tableName):
    vals=[]
    primaryKeys = getPrimaryKeys(cursor,tableName) # get the primary key of the table were deleting from
    try:
        for key in primaryKeys:
            print(f'Enter: {key}') # promt the user to enter value for the primary key attributes so that the entry can be selected
            vals.append(input())
        proc = getDel(tableName)
        statement = "SELECT Name FROM Individual WHERE ID = %s" #find entry if exist and get name
        cursor.execute(statement,(vals[0],))
        result = cursor.fetchall()
        if result: # if entry found delete
            cursor.callproc(proc,vals)
            print(f"{result} has been deleted")
        else: # if not found display error message
            print(f"No entry found with {primaryKeys} = {vals}. No Entry to delete")
    except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}\n try again")
    except Exception as e:
        print(f"Error {e}\n try again")  

# updates a created test value using the user input
def tabUp(cursor, tableName):
    # create test entry
    values = (9999, "John Smith", "M", "1901-10-10", "2000-10-10", "Perth", "Australia", "Oceania", "Perth", "Australia", "Oceania")

    cursor.callproc('insertRecipient', (9999, 'I'))
    cursor.callproc('insertInd', values) #insert test entry

    cursor.execute("SELECT * FROM Individual WHERE ID = 9999") # display test entry to the user
    result = cursor.fetchall()
    headers = [header[0] for header in cursor.description]
    tables = PrettyTable(headers)
    for row in result:
        tables.add_row(row)
    print("Individual before update\n")
    print(tables)
    try:
        newName = input("Enter a new name: ") # get new name to update
        UPDATEq = "UPDATE Individual SET Name = %s WHERE ID = 9999;" # update entry
        cursor.execute(UPDATEq, (newName,))

        cursor.execute("SELECT * FROM Individual WHERE ID = 9999")
        result = cursor.fetchall()
        headers = [header[0] for header in cursor.description] # dispay the entry after update to the user 
        tables = PrettyTable(headers)
        for row in result:
            tables.add_row(row)
        print("Individual after update \n")
        print(tables)
        print("Many changes much wow")
    except mysql.connector.Error as e:
        print("Error connecting to MySQL: " + str(e))
    except Exception as e:
        print(f"Unknown error occurred! {e}")

    cursor.execute("DELETE FROM Recipient WHERE ID = 9999;") # remove test entry once done

# get the matching insert Procedure for the table 
def getIns(tableName):
    proc = ""
    if(tableName == "Recipient"):
        proc = 'insertRecipient'
    elif(tableName == "Organisation"):
        proc = 'insertOrg'
    elif(tableName == "Individual"):
        proc = 'insertInd'
    elif(tableName == "Affiliate"):
        proc = 'insertAff'
    elif(tableName == "AffiliatedTo"):
        proc = 'insertAffTo'
    elif(tableName == "Prize"):
        proc = 'insertPrize'
    elif(tableName == "AwardedTo"):
        proc = 'insertAwardTo'
    return proc

# gets the matching del procedure for the table
def getDel(tableName):
    proc =''
    if(tableName == "Recipient"):
        proc = 'DeleteRecipient'
    elif(tableName == "Organisation"):
        proc = 'DeleteOrganisation'
    elif(tableName == "Individual"):
        proc = 'DeleteOrganisation'
    elif(tableName == "Affiliate"):
        proc = 'DeleteAffiliate'
    elif(tableName == "Prize"):
        proc = 'DeletePrize'
    return proc

# get the primary keys of the passed table
def getPrimaryKeys(cursor,tablename):
    query =f""" SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = 'dswork'
        AND TABLE_NAME = '{tablename}'
        AND CONSTRAINT_NAME = 'PRIMARY';
    """
    cursor.execute(query)
    result = cursor.fetchall()
    prmyKey = [row[0] for row in result]
    return prmyKey

#  checks that the passsed value is between 1-11
def numChecker(sel):
    try:
        sel = int(sel)
        if 1 <= sel <= 11:
            return True
        else:
            return False
    except ValueError:
        return False

def main():
    driver()

if __name__== "__main__":
    main()


