# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from collections import defaultdict
import codecs
import json
from collections import OrderedDict
from gzip import GzipFile
import xmltodict
import re


path = 'shir1.xml.gz'
if len(sys.argv) != 2:
    print "\nUsage: python Main.py <pathName>\n"
    exit()
else:
# Reading arguments
  path = sys.argv[1]


def cleanStr(str):
    for c in "[]()*&^%$#@!:,\/<>":
        str = str.replace(c, "")
    return str

def getDate(str):
    str = re.sub('[^0-9]', ' ', str)
    date = [int(s) for s in str.split() if s.isdigit()]
    if date:
        for x in date:
            if x>1903 and x<2020:
                return x
    return None

def getHebrewDate(str):

    str = re.sub('[0-9]', '', str)
    str = re.sub('[a-zA-Z]', '', str)
    str=cleanStr(str)
    str.replace("\\","")
    str.replace(".","")
    str.replace("-", "")
    str.replace("?", "")
    index=str.find('תש',0,len(str))
    if (index == -1):
        return None
    string=str[index:index+12]
    if string != "":
        string.re.sub('\\', '', str)
        return string
    return None




doc = xmltodict.parse(GzipFile(path))

allRecords = doc[u'collection'][u'record']
othersfile = "songs.json"
otherDict = defaultdict(lambda: [])
print 'finish reading'
num = 0
for index, record in enumerate(allRecords):
    print(str(index)+" / 29366")
    entityEntry = defaultdict(lambda: "")


    try:
        for control in record['controlfield']:

            if control['@tag'] == '001':
                # mark control field
                entryID = control['#text']
                entityEntry["ID"] = entryID

        for dataF in record['datafield']:
            entry = {}
            items = dataF['subfield']
            items = [items] if not isinstance(items, list) else items
            tag = dataF['@tag']
            if tag == "100" or tag == "110" or tag == "700" or tag == "710":  # multiple field
                person = ''
                flage = False
                for item in items:
                    code = item[u'@code']
                    if code == 'a':
                        person = item['#text'].strip()
                        person = cleanStr(person)
                        person=person.replace("להקה","")
                        print(person)
                    elif code == 'e':
                        flage = True
                        role = item['#text'].strip().encode('UTF8')
                        if role == "מלחין":
                            if not person == '':
                                if person not in entityEntry["Composer"]:
                                    if( entityEntry["Composer"]!=""):
                                        entityEntry["Composer"] += ", "
                                    entityEntry["Composer"] += str(person)
                        if role == "מחבר":
                            if not person == '':
                                if person not in entityEntry["Poet"]:
                                    if( entityEntry["Poet"]!=""):
                                        entityEntry["Poet"] += ", "
                                    entityEntry["Poet"] += str(person)
                        if role == "singer" or role == "זמר" or role == "performer" or role == "מבצע":
                            print("enter0")
                            if not person == '':
                                print("enter1")
                                if person not in entityEntry["Performer"]:
                                    print("enter3")
                                    if( entityEntry["Performer"]!=""):
                                        print("enter4")
                                        entityEntry["Performer"] += ", "
                                    entityEntry["Performer"] +=  str(person)
                        if role == "מעבד מוזיקלי":
                            if not person == '':
                                if person not in entityEntry["MusicalAdapter"]:
                                    if( entityEntry["MusicalAdapter"]!=""):
                                        entityEntry["MusicalAdapter"] += ", "
                                    entityEntry["MusicalAdapter"] +=  str(person)

                if not flage:
                    if not person == '':
                        if person not in entityEntry["Others"]:
                            if (entityEntry["Others"] != ""):
                                entityEntry["Others"] += ", "
                            entityEntry["Others"] += str(person)


            elif tag == "245":  # multiple field
                for item in items:
                    code = item[u'@code']
                    if code == 'a':
                        entityEntry["SongName"] = (cleanStr(item['#text'].strip()))

                #entityEntry["SongName"].append(value)

            elif tag == "260":  # multiple field
                if 'CivilDate' not in entityEntry:
                    for item in items:
                        code = item[u'@code']
                        if code == 'c':
                            item1 = item['#text'].strip().encode('UTF8')
                            date = getDate(item1)
                            if date:
                                entityEntry["CivilDate"] = (str(date))
                            else:
                                flagDigit = False
                                for c in "1234567890-?":
                                    if c in item['#text'].strip():
                                        flagDigit = True
                                        break
                                if(not flagDigit):
                                    entityEntry["HebrewDate"] = (cleanStr(item['#text'].strip()))

                        elif code=='a':
                            name = cleanStr(item['#text'].strip())
                            if (entityEntry["PlaceOfPublication"] != ""):
                                entityEntry["PlaceOfPublication"] += ", "
                            entityEntry["PlaceOfPublication"] += str(name)
                        elif code == 'b':
                            name = cleanStr(item['#text'].strip())
                            if (entityEntry["NameOfPublisher"] != ""):
                                entityEntry["NameOfPublisher"] += ", "
                            entityEntry["NameOfPublisher"] +=str(name)
                        else:
                            print "unhandled code: 260 " + code

            elif tag == "518":
                if 'CivilDate' not in entityEntry:
                    for item in items:
                        code = item[u'@code']
                        if code == 'a':
                            item1 = item['#text'].strip().encode('UTF8')
                            date = getDate(item1)

                            if date:
                                entityEntry["CivilDate"] = (str(date))
                        else:
                            print "unhandled code: 518 " + code

                #entityEntry["Date"].append(value)

            #song date
            elif tag == "773":
                    for item in items:
                        if 'CivilDate' not in entityEntry:
                            code = item[u'@code']
                            if code == 'a':
                                item1 = item['#text'].strip().encode('UTF8')
                                date = getDate(item1)
                                if date:
                                    entityEntry["CivilDate"] = (str(date))
                                else:
                                    entityEntry["HebrewDate"] = (str(getHebrewDate(item1).decode('utf-8)')))

                            elif code == 't':
                                item1 = item['#text'].strip().encode('UTF8')
                                date = getDate(item1)
                                if date:
                                    entityEntry["CivilDate"] = (str(date))
                                else:
                                    hebYear = getHebrewDate(item1)
                                    if(hebYear is not None):
                                        entityEntry["HebrewDate"] = str(hebYear)
                            else:
                                print "unhandled code: 773 " + code
                        else:
                            break
    except:
        print "no go for this record" + " " + entryID

    otherDict["songs"].append(entityEntry)



# sort_order = ['ID', 'SongName', 'Performer', 'CivilDate',"HebrewDate","Composer","Poet","Others","PlaceOfPublication","MusicalAdapter","NameOfPublisher"]
# allsites_ordered = [OrderedDict(sorted(item.iteritems(), key=lambda (k, v): sort_order.index(k)))
#                     for item in otherDict["songs"]]


outputfile = codecs.open(othersfile, 'w', encoding="utf-8")
outputfile.write(json.dumps(otherDict, indent=4, ensure_ascii=False, encoding="utf-8"))
outputfile.close()