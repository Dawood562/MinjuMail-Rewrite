import sqlite3


# Set variables to access the database
database = sqlite3.connect('./database/dB.db')
cursor = database.cursor()
