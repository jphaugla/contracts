import json
import csv
import redis
from datetime import datetime
from loadFiles import load_csv_to_db_with_labels, load_csv_to_db, connect

con = connect()
load_directory = "./data/"
load_csv_to_db_with_labels(con, load_directory + "DJI.csv", "DJI", "RG1", "ACCT1")
load_csv_to_db_with_labels(con, load_directory + "BTC-USD.csv", "BTC", "RG1", "ACCT1")
load_csv_to_db_with_labels(con, load_directory + "GSPC.csv", "GSPC", "RG1", "ACCT1")
load_csv_to_db_with_labels(con, load_directory + "IXIC.csv", "IXIC", "RG2", "ACCT1")
load_csv_to_db_with_labels(con, load_directory + "N225.csv", "N225", "RG2", "ACCT1")
load_csv_to_db_with_labels(con, load_directory + "TNX.csv", "TNX", "RG2", "ACCT1")

load_csv_to_db_with_labels(con, load_directory + "DJI.csv", "DJI", "RG1", "ACCT2")
load_csv_to_db_with_labels(con, load_directory + "BTC-USD.csv", "BTC", "RG1", "ACCT2")
load_csv_to_db_with_labels(con, load_directory + "GSPC.csv", "GSPC", "RG1", "ACCT2")
load_csv_to_db_with_labels(con, load_directory + "IXIC.csv", "IXIC", "RG2", "ACCT2")
load_csv_to_db_with_labels(con, load_directory + "N225.csv", "N225", "RG2", "ACCT2")
load_csv_to_db_with_labels(con, load_directory + "TNX.csv", "TNX", "RG2", "ACCT2")

load_csv_to_db(con, load_directory + "AAPL.csv", "APPL", "LABELS ticker AAPL")
load_csv_to_db(con, load_directory + "GOOG.csv", "GOOG", "LABELS ticker GOOG")
load_csv_to_db(con, load_directory + "IBM.csv", "IBM", "LABELS ticker IBM")
load_csv_to_db(con, load_directory + "TSLA.csv", "TSLA", "LABELS ticker TSLA")

print("successful completion")







