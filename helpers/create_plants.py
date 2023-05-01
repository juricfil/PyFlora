import sqlite3

def create_connection(db_file):
    """
    New connection to DB
    """
    db_connection = None
 
    try:
        db_connection = sqlite3.connect(db_file)
        return db_connection
    except sqlite3.Error as error:
        print(error)
 
    return db_connection

def close_connection(db_connection):
    """
    Close connection
    """
    if db_connection:
        db_connection.close()

def create_plant(db_connection, plant):
    """
    Create new plant
    """
    query = """INSERT INTO plants (name, image, humidity, light, substrate) VALUES (?, ?, ?, ?, ?)"""
    try:
        cursor = db_connection.cursor()
        cursor.execute(query, plant)
        db_connection.commit()
        return cursor.lastrowid
    except sqlite3.Error as error:
        print(error)
 
    return None

# Function for Convert Binary Data 
# to Human Readable Format
def convertToBinaryData(filename):
    """
    Convert binary format to images or files data
    """
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

db_file = '/home/filip/PyFlora/instance/flaskr.sqlite'
pic1 = convertToBinaryData('/home/filip/PyFlora/helpers/Alocasia-1.jpg')
pic2 = convertToBinaryData('/home/filip/PyFlora/helpers/Saintpaulia-Ionantha.jpg')
plant1 = ('African Mask',pic1,60,10,None)
plant2 = ('African Violet',pic2,80,10,'fertilizer')

connection = create_connection(db_file=db_file)
create_plant(connection, plant1)
create_plant(connection, plant2)
close_connection(connection)