import sqlite3

conn = sqlite3.connect('paychecks.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS Earnings(Date TEXT, RegHours REAL, OtHours REAL, TotalHours REAL, EarnTotal REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS Withholdings(Date TEXT, Social_Security REAL, Medicare REAL, FedTax REAL, PA_unemployment REAL, PATax REAL, YCity_LYOY2 REAL, YCity_YRKCY REAL, TaxTotal REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS CheckTotal(Date TEXT, CheckTotal REAL)')

def data_entry():
    with conn:
        regpay = 15.00
        otpay = 22.50
        
        print('***EARNINGS***\n')
        date = input('Date of paycheck: ')
        reghours = float(input('Hours worked: '))
        othours = float(input('Overtime hours: '))
        totalhours = reghours + othours
        earntotal = (reghours * regpay) + (othours * otpay)
        print('\n***WITHHOLDINGS***\n')
        ss = float(input('Social Security tax: '))
        med = float(input('Medicare tax: '))
        fed = float(input('Federal Income Tax: '))
        paincome = float(input('PA Income Tax: '))
        unemply = float(input('PA Unemployment Tax: '))
        yorktax1 = float(input('York City LYOY2 Tax: '))
        yorktax2 = float(input('York City YRKCY Tax: '))
        taxtotal = ss + med + fed + paincome + unemply + yorktax1 + yorktax2
        checktotal = earntotal - taxtotal
        c.execute("INSERT INTO Earnings (date, reghours, othours, totalhours, earntotal) VALUES (?, ?, ?, ?, ?)", 
                 (date, reghours, othours, totalhours, earntotal))
        c.execute("INSERT INTO Withholdings (date, Social_Security, Medicare, FedTax, PA_unemployment, PATax, YCity_LYOY2, YCity_YRKCY, TaxTotal) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                 (date, ss, med, fed, paincome, unemply, yorktax1, yorktax2, taxtotal))
        c.execute("INSERT INTO CheckTotal (date, checktotal) VALUES (?, ?)", 
                 (date, checktotal))
    c.close()
    conn.close()

create_table()
data_entry()

print('Database updated.')