import pyodbc

for driver in pyodbc.drivers():
    print(driver)

cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=tcp:trimmerfarmmanagement.database.windows.net,1433;"
                      "Database=TFM Field Scouting;"
                      "Uid=chrism;"
                      "Pwd={[1Qa-2Ws]};"
                      "Encrypt=yes;"
                      "TrustServerCertificate=no;"
                      "Connection Timeout=30;")

