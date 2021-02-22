import mysql.connector


def deleteDB(dbname):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="metehan199",
        auth_plugin="mysql_native_password",
        database=dbname
    )
    if not db.is_connected():
        return
    mycursor = db.cursor()
    mycursor.execute("DROP DATABASE {0}".format(dbname))
    print("Database \"{0}\" deleted.".format(dbname))


def createDB(dbname):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="metehan199",
        auth_plugin="mysql_native_password"
    )
    mycursor = db.cursor()
    mycursor.execute("CREATE DATABASE {0}".format(dbname))
    print("MySql database \"{0}\" created.".format(dbname))
    return createCollumns(dbname)


def connectToDB(dbname):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="metehan199",
        auth_plugin="mysql_native_password",
        database=dbname
    )
    return db


def createCollumns(dbname):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="metehan199",
        auth_plugin="mysql_native_password",
        database=dbname
    )
    mycursor = db.cursor()
    mycursor.execute(
        "CREATE TABLE Tutanak (Donem int, DonemYil int, Tarih varchar(10), BirlesimNo int, TutanakURL varchar(70),"
        " TutanakID int PRIMARY KEY)")
    mycursor.execute(
        "CREATE TABLE Oturum (TutanakID int, FOREIGN KEY(TutanakID) REFERENCES Tutanak(TutanakID), OturumNo int,"
        " OturumID int PRIMARY KEY)")
    mycursor.execute(
        "CREATE TABLE Milletvekili (MilletvekiliAdi varchar(30), MilletvekiliSehri varchar(15) ,"
        " MilletvekiliID int PRIMARY KEY)")
    mycursor.execute(
        "CREATE TABLE Konusma (OturumID int, FOREIGN KEY(OturumID) REFERENCES Oturum(OturumID),"
        " MilletvekiliID int, FOREIGN KEY(MilletvekiliID) REFERENCES Milletvekili(MilletvekiliID),"
        " KonusmaSırası int, KonusmaID int PRIMARY KEY)")
    return db


def storeTutanak(db, Donem, DonemYil, Tarih, BirlesimNo, TutanakURL, TutanakID):
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO Tutanak (Donem,DonemYil,Tarih,BirlesimNo,TutanakURL,TutanakID) VALUES (%s,%s,%s,%s,%s,%s)",
                     (Donem, DonemYil, Tarih, BirlesimNo, TutanakURL,TutanakID))
    db.commit()


def storeOturum(db, TutanakID, OturumNo,OturumID):
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO Oturum (TutanakID, OturumNo, OturumID) VALUES (%s,%s,%s)",
                     (TutanakID, OturumNo, OturumID))
    db.commit()


def storeKonusma(db, OturumID, MilletvekiliID, KonusmaSırası, KonusmaID):
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO Konusma (OturumID, MilletvekiliID, KonusmaSırası, KonusmaID) VALUES (%s,%s,%s,%s)",
                     (OturumID, MilletvekiliID, KonusmaSırası, KonusmaID))
    db.commit()


def storeMilletvekili(db, isim, sehir, MilletvekiliID):
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO Milletvekili (MilletvekiliAdi,MilletvekiliSehri, MilletvekiliID) VALUES (%s,%s,%s)",
                     (isim, sehir, MilletvekiliID))
    db.commit()


def printAllTables(db):
    dbcursor = db.cursor(buffered=True)

    dbcursor.execute("SELECT database()")
    db_name = dbcursor.fetchone()[0]
    print("All tables in ", db_name, ":")

    dbcursor.execute("SHOW TABLES")
    for table in dbcursor:
        print(" ", table[0], end=": ")
        tablecursor = db.cursor(buffered=True)
        tablecursor.execute("DESCRIBE {0}".format(table[0].capitalize()))
        for info in tablecursor:
            print(info[0], info[1], info[3], end=", ")
        print()
    print()


def printAllDB(db):
    dbcursor = db.cursor(buffered=True)

    dbcursor.execute("SELECT DATABASE()")
    db_name = dbcursor.fetchone()[0]
    print("All data in ", db_name, ":")

    dbcursor.execute("SHOW TABLES")
    for table in dbcursor:
        print(table[0], ":")
        printTable(db, table[0].capitalize())
    print()


def printTable(db, tableName):
    tablecursor = db.cursor()
    sql = "SELECT * FROM {0}".format(tableName)
    tablecursor.execute(sql)
    for info in tablecursor:
        print(info)


"""
deleteDatabase("testdatabase")
database = createDatabase("testdatabase")
printAllTables(database)
storeTutanak(database, 1, 2, "Tarih", 2, "TutanakURL")
storeOturum(database, 1, 2)
storeMilletvekili(database, "isim", "sehir")
storeKonusma(database, 1, 1, 2)
printAllDatabase(database)
"""
