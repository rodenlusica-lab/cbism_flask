import mysql.connector

db = mysql.connector.connect(
    host="centerbeam.proxy.rlwy.net",
    user="root",
    password="TdNzCohxzHUnHnrmXGtVyEaXrkFKwlXo",
    database="railway",
    port=33286
)

cursor = db.cursor(dictionary=True)