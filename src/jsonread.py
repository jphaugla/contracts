import os,json
from redisearch import Client

client = Client('member')
print("connect successful")
base_directory = "../data/"
cnt = 0
for (dirpath, dirnames, filenames) in os.walk(base_directory):
    print("dirpath=" + dirpath)
    for file in filenames:
        # print("file=" + file)
        if ("json" in file):
            shortname = file.replace(".json", "")
            print("shortname is" + shortname)
            openname = dirpath + "/" + file
            print("openname is " + openname)
            data = json.loads(open(openname, "r").readline())
            print("data is ")
            print(data['data'])
            print("members is")
            print(data['data']['members'])
            for member in data['data']['members']:
                print("the id is", member['id'])
                keyname="member:" + str(member['id'])
                id1=""
                id2=""
                id3=""
                id4=""
                for identifier in member['identifiers']:
                    if identifier['type']=='ID1': id1 = identifier['value']
                    if identifier['type']=='ID2': id2 = identifier['value']
                    if identifier['type']=='ID3': id3 = identifier['value']
                    if identifier['type']=='ID4': id4 = identifier['value']
                client.add_document(keyname, id=member['id'], firstName=member['firstName'],
                                        lastName=member['lastName'], dependentSequence=member['dependentSequence'],
                                        id1=id1, id2=id2, id3=id3, id4=id4)
