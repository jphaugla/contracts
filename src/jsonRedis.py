import os, json, redis

r = redis.StrictRedis("localhost", 6379)
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
                memberId = str(member['id'])
                keyname="memberHash:" + memberId
                id1=""
                id2=""
                id3=""
                id4=""
                for identifier in member['identifiers']:
                    if identifier['type']=='ID1':
                        id1 = identifier['value']
                        r.sadd("id1:" + id1, memberId)
                    if identifier['type']=='ID2':
                        id2 = identifier['value']
                        r.sadd("id2:" + id2, memberId)
                    if identifier['type']=='ID3':
                        id3 = identifier['value']
                        r.sadd("id3:" + id3, memberId)
                    if identifier['type']=='ID4':
                        id4 = identifier['value']
                        r.sadd("id4:" + id4, memberId)
                r.hmset(keyname, {'id': member['id'], 'firstName': member['firstName'], 'lastName': member['firstName'],
                                  'dependentSequence': member['dependentSequence'], 'id1': id1, 'id2': id2, 'id3': id3,
                            'id4': id4, })
