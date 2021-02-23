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
        " TutanakID int PRIMARY KEY AUTO_INCREMENT)")
    mycursor.execute(
        "CREATE TABLE Oturum (TutanakID int, FOREIGN KEY(TutanakID) REFERENCES Tutanak(TutanakID), OturumNo int,"
        " OturumID int PRIMARY KEY AUTO_INCREMENT)")
    mycursor.execute(
        "CREATE TABLE Milletvekili (MilletvekiliAdi varchar(30), MilletvekiliSehri varchar(15) ,"
        " MilletvekiliID int PRIMARY KEY AUTO_INCREMENT)")
    mycursor.execute(
        "CREATE TABLE Konusma (OturumID int, FOREIGN KEY(OturumID) REFERENCES Oturum(OturumID),"
        " MilletvekiliID int, FOREIGN KEY(MilletvekiliID) REFERENCES Milletvekili(MilletvekiliID),"
        " KonusmaSırası int, KonusmaID int PRIMARY KEY AUTO_INCREMENT)")
    return db


def storeTutanak(db, Donem, DonemYil, Tarih, BirlesimNo, TutanakURL):
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO Tutanak (Donem,DonemYil,Tarih,BirlesimNo,TutanakURL) VALUES (%s,%s,%s,%s,%s)",
                     (Donem, DonemYil, Tarih, BirlesimNo, TutanakURL))
    db.commit()
    TutanakID = mycursor.execute("SELECT TutanakID FROM Tutanak ORDER BY TutanakID DESC LIMIT 1")
    return TutanakID


def storeOturum(db, TutanakID, OturumNo):
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO Oturum (TutanakID, OturumNo) VALUES (%s,%s)",
                     (TutanakID, OturumNo))
    db.commit()
    OturumID = mycursor.execute("SELECT OturumID FROM Oturum ORDER BY OturumID DESC LIMIT 1")
    return OturumID


def storeKonusma(db, OturumID, MilletvekiliID, KonusmaSırası):
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO Konusma (OturumID, MilletvekiliID, KonusmaSırası) VALUES (%s,%s,%s)",
                     (OturumID, MilletvekiliID, KonusmaSırası))
    db.commit()
    KonusmaID = mycursor.execute("SELECT KonusmaID FROM Konusma ORDER BY KonusmaID DESC LIMIT 1")
    return KonusmaID


def storeMilletvekili(db, isim, sehir):
    mycursor = db.cursor()

    mycursor.execute(
        "SELECT MilletvekiliID FROM Milletvekili WHERE MilletvekiliAdi = %s AND MilletvekiliSehri = %s LIMIT 1",
        (isim, sehir))
    MilletvekiliID = mycursor.fetchone()
    if MilletvekiliID is None:
        mycursor.execute("INSERT INTO Milletvekili (MilletvekiliAdi,MilletvekiliSehri) VALUES (%s,%s)",
                         (isim, sehir))
        db.commit()
        mycursor.execute(
            "SELECT MilletvekiliID FROM Milletvekili ORDER BY MilletvekiliID DESC LIMIT 1")
        MilletvekiliID = mycursor.fetchone()
    return MilletvekiliID[0]


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
deleteDB("testdatabase")
database = createDB("testdatabase")
# printAllTables(database)
# storeTutanak(database, 1, 2, "Tarih", 2, "TutanakURL")
# storeOturum(database, 1, 2)
print(storeMilletvekili(database, "isim1", "sehir1"))
print(storeMilletvekili(database, "isim1", "sehir1"))
print(storeMilletvekili(database, "isim2", "sehir2"))
# storeKonusma(database, 1, 1, 2)
printAllDB(database)
"""
