import json
import csv
import redis
import os
import errno
from datetime import datetime


def connect():
    r = redis.StrictRedisRedis("redis", 6379)
    return r


def datestr_to_ts(datestr):
    dt = datetime.strptime(datestr, "%Y-%m-%d")
    ts = int(dt.strftime('%s'))*1000
    return ts

def date_fields_to_ts(full_date, in_time):
    datestr = full_date + ":" + in_time
    dt = datetime.strptime(datestr, "%Y%m%d:%H%M%S")
    ts = int(dt.strftime('%s'))*1000
    return ts

def convert_csv_to_json(datafile, target_datafile):
    # read the csv and add the data to a dictionary

    arr = []

    with open(datafile) as csvFile:
        csvReader = csv.DictReader(csvFile)
        # print(csvReader)
        for csvRow in csvReader:
            arr.append(csvRow)

    # print(arr)

    # write the data to a json file
    if not os.path.exists(os.path.dirname(target_datafile)):
        try:
            os.makedirs(os.path.dirname(target_datafile))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(target_datafile, "w") as jsonFile:
        jsonFile.write(json.dumps(arr, separators=(',', ':')))

    csvFile.close()
    jsonFile.close()


def load_json_to_db(con, datafile, timeseries):
    # print("entering load_json_to_db with datafile=" + datafile)
    i = 0
    try:
        data = json.loads(open(datafile, "r").readline())
        create_command = "TS.CREATE " + timeseries
        pipe = con.pipeline()
        pipe.delete(timeseries)
        # print(create_command)
        # con.execute_command(create_command)
        # print(data)
        for t in data:
            just_date = data[i]["<DATE>"]
            just_time = data[i]["<TIME>"]
            closing_string = data[i]["<CLOSE>"]
            closing = float(closing_string)
            # print("i=" + str(i) + " date=" + just_date + " time=" + just_time + " closing=" + closing_string)
            ts = date_fields_to_ts(just_date,just_time)
            pipe.execute_command("TS.ADD", timeseries, ts, closing)
            i += 1
        pipe.execute()
    except Exception as e:
        print("Ignore exceptions " + str(e) + " in file=" + datafile)
    return i


def load_csv_to_db_with_labels(con, datafile, instrument_id, risk_group, account_id):
    #  label_string = "labels={'Account':'" + account_id + "','RiskGroup':'" + risk_group +
    #            "','Instrument':'" + instrument_id + "'}"
    label_string = "LABELS Account " + account_id + " RiskGroup " + risk_group + " Instrument " + instrument_id
    # print("label string is " + label_string)

    hash_key = "NAV:" + account_id + ':' + risk_group + ':' + instrument_id
    # print("hash_key is " + hash_key)
    load_csv_to_db(con, datafile, hash_key, label_string)


def load_csv_to_db(con, datafile, hash_key, label_string):
    # clean up by deleting existing key
    con.delete(hash_key)
    create_command = "TS.CREATE " + hash_key + " " + label_string
    print(create_command)
    con.execute_command(create_command)
    with open(datafile) as csv_file:
        # file is comma delimited
        csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONE)
        idx = 0
        fields = next(csv_reader, None)
        #  go through all rows in the file
        for row in csv_reader:
            idx += 1
            # file columns
            # 0)Date 1)Open 2)High 3)Low 4)Close 5)Adj close 6)Volume
            ts = datestr_to_ts(row[0])
            adjusted_close = str(row[5])
            #  some files have values with the word null so ignore those
            if adjusted_close != "null":
                add_command = "TS.ADD " + hash_key + " " + str(ts) + " " + str(row[5])
                print(add_command)
                con.execute_command(add_command)
        csv_file.close()
