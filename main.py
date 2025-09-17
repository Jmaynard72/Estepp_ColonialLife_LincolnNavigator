from sqlalchemy import create_engine
from datetime import datetime, date
import pandas as pd
import pyodbc 

import logging
import re 
import os 
import shutil

import send_mail as Email 



# Config
Serer = 'PSI-SQL'
Database = 'Millennium'
Driver = 'ODBC Driver 17 for SQL Server'
Co_List = '7220,7221'
Export_Path = 'C:/Users/jmaynard/OneDrive - PAYROLL SOLUTIONS/Shared/Colonial Life/Estepp-Navigator'

# Send notifications to
Sent_To = 'jmaynard@payrollsolutions.cc'

def format_company_filter(s) -> str:
    #fomrat company list into sql filter format
    formatted = ", ".join(f"'{item.strip()}'" for item in s.split(","))
    return formatted

def format_phone_number(s) -> str:
    # Extract only digits
    digits = re.sub(r'\D','', s)

    # Check if the string as 10 digits
    if len(digits) == 10:
        # Format as 123-456-7890
        return f'{digits[:3]}-{digits[3:6]}-{digits[6:]}'
    else:
        return ''
    
def create_export_directory(path: str):
    try:
        os.makedirs(path,exist_ok=True)
    except Exception as e:
        logging.error(f'Error creating direcotry {path}: {e}')

   
def main():
    # Get sql formatted list
    company_list = format_company_filter(Co_List)

    # Step 1 Create Log
    logging.basicConfig(filename= './log.txt',filemode='a',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Script started')

    # Step 2 Pull data from Millennium

    # Connect to database
    try:
        connection_string = f'mssql+pyodbc://@{Serer}/{Database}?trusted_connection=yes&driver={Driver}'
        engine = create_engine(connection_string, fast_executemany=True)
        conn = engine.connect()

        query = f"SELECT * FROM JDM_ColonialLife_LincolnNavigator_Demographics_V01 WHERE co IN ({company_list}) ORDER BY lastname,firstname"
        df = pd.read_sql(query,conn)

        logging.info('Successfully pulled data from Millennium.')
    except Exception as e:
        logging.error(f'Error pulling data from Millennium: {e}')
    finally:
        try:
            conn.close()
        except:
            conn = ''

    
    # Step 3 Rename column headers in data frame
    df.rename(columns={'ssn':'Employee SSN','lastname':'Last Name','firstname':'First Name'},inplace=True)
    df.rename(columns=({'birthDate':'Date of Birth','sex':'Gender','hireDate':'Hire Date'}),inplace=True)
    df.rename(columns=({'annualSalary':'Annual Base Salary','address1':'Address 1','address2':'Address 2'}),inplace=True)
    df.rename(columns=({'city':'City','state':'State','zip':'Zip Code'}),inplace=True)
    df.rename(columns=({'title':'Job Title','cc1':'Department','emailAddress':'Email'}),inplace=True)
    df.rename(columns=({'homePhone':'Phone Number'}),inplace=True)
    df.rename(columns=({'payFrequency':'Pay Frequency'}),inplace=True)

    # Step 4 Drop un-needed columns
    df.drop(columns=['co','cc2','cc3','cc4','cc5'],inplace=True)

    # Step 5 Save file to CSV
    try:
        today = date.today().strftime('%Y%m%d')
        filename = f'Estepp_Energy-{today}.csv'
        create_export_directory(Export_Path)
        df.to_csv(Export_Path + '/' + filename,index=False,encoding='utf-8')
        logging.info(f'Successfuly save data to {filename}')        

        # Step 6 Send email notification
        message = f'Data sucessfully exported to file {filename} and uploaded to shared folder {Export_Path}'
        subject = '[SUCCESS] Estepp Colonial Life : Lincoln Navigator Demographics File'
        Email.send_message(Sent_To,subject,message)
    except Exception as e:
        logging.error(f'Error saving csv file: {e}')
        message = f'Failed to export data sucessfully to file {filename}. Check log file in script directory.'
        subject = '[FAILURE] Estepp Colonial Life : Lincoln Navigator Demographics File'
        Email.send_message(Sent_To,subject,message)


    

if __name__ == '__main__':
    main()






