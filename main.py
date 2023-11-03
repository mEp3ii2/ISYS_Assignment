import subprocess

# runs the passed bash file
def runScript(scriptName):
    ran = True
    try:
        subprocess.run(["bash",scriptName],check=True)
    except subprocess.CalledProcessError as e:
        print("Error running script"+str(e))
        ran = False
    return ran

# runs some bash scripts first to install some necessary packages 
def main():
    try:
        if runScript("unicodeSetup.bash"): # get rid of funny characters
            if runScript("mysqlConnSetup.bash"): # connect to the sql (thanks for the mess around there (; ))
                if runScript("prettytables.bash"): # make the sql output look nice in python
                    subprocess.run(["python3","sqlTime.py"],check=True) # run the python file now
    except Exception as e:
        print(f"Error occured during operation: {e}")
if __name__ == "__main__":
    main()





