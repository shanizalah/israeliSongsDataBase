
import sys
import json
import csv

reload(sys)
sys.setdefaultencoding('utf-8')

##
# Convert to string keeping encoding in mind...
##
def to_string(s):
    try:
        return str(s).strip().encode('UTF8')
    except:
        # Change the encoding type if needed
        return str(s).decode('UTF8')


def reduce_item(key, value):
    global reduced_item

    # Reduction Condition 1
    if type(value) is list:
        i = 0
        for sub_item in value:
            reduce_item(key + '_' + to_string(i), sub_item)
            i = i + 1

    # Reduction Condition 2
    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:
            reduce_item(key + '_' + to_string(sub_key), value[sub_key])

    # Base Condition
    else:
        key = key.split("_")[1]
        reduced_item[to_string(key)] = to_string(value)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print ("\nUsage: python jsonToCsv.py <json_in_file_path> <csv_out_file_path>\n")
    else:
        # Reading arguments
        node = "songs"
        json_file_path = sys.argv[1]
        csv_file_path = sys.argv[2]

        fp = open(json_file_path, 'r')
        json_value = fp.read()
        raw_data = json.loads(json_value)

        try:
            data_to_be_processed = raw_data[node]
        except:
            data_to_be_processed = raw_data

        processed_data = []
        header = []
        for item in data_to_be_processed:
            if item:
                reduced_item = {}
                reduce_item(node, item)

                header += reduced_item.keys()
                if reduced_item:
                     processed_data.append(reduced_item)

        header = list(set(header))
        order=['ID',"SongName","Performer","CivilDate","HebrewDate","Composer","Poet","MusicalAdapter","Others",
               "PlaceOfPublication","NameOfPublisher"]
        header = sorted(header, key=order.index)

        with open(csv_file_path, 'wb') as f:
            writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for row in processed_data:
                    writer.writerow(row)

        print ("Just completed writing csv file with %d columns" % len(header))
