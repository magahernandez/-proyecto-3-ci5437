import sys
import cnf
import os
from datetime import datetime, timedelta
import json

def translate_event(data):
    return [get_participant(data[0]),get_participant(data[1]),get_day(data[2]),get_hour(data[3])]

def get_participant(x):
    return data['participants'][x]

def get_day(x):
    obj_time = datetime.strptime(data['start_date'], '%Y-%m-%d') + timedelta(days=x)
    return str(obj_time).replace(" 00:00:00","")

def get_hour(x):
    obj_time = datetime.strptime(inf['start_hour'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=x*2)
    obj_time = str(obj_time).replace("1900-01-01 ","")
    return str(obj_time)

def create_file_ics(data_translate):
    os.makedirs('ics', exist_ok=True)
    name_ics = 'ics/'+sys.argv[1].replace(".json",".ics")
    with open(f'%s' %name_ics, 'w') as ics_file:
        ics_file.write("BEGIN:VCALENDAR\n")
        ics_file.write("VERSION:2.0\n")
        ics_file.write("PRODID:-//bobbin v0.1//NONSGML iCal Writer//EN\n")
        ics_file.write("CALSCALE:GREGORIAN\n")
        ics_file.write("METHOD:PUBLISH\n")

        for n in range(len(data_translate)):
            now = datetime.now()
            ics_file.write("BEGIN:VEVENT\n")
            iso_time = data_translate[n][2].replace("-","") + "T"+ data_translate[n][3].replace(":","") + "Z"
            ics_file.write("DTSTART:" + iso_time + '\n')
            iso_time = datetime.strptime(data_translate[n][3],'%H:%M:%S') + timedelta(hours=2)
            end_time = str(iso_time).replace("1900-01-01 ","")
            iso_time = data_translate[n][2].replace("-","") + "T"+ str(end_time.replace(":","")) + "Z"
            ics_file.write("DTEND:" + iso_time + '\n')
            iso_time = now.strftime("%Y%m%dT%H%M%SZ")
            ics_file.write("DTSTAMP:" + iso_time + "\n")
            ics_file.write("UID:"+data_translate[n][0]+data_translate[n][1]+"\n")
            ics_file.write("CREATED:" + iso_time + "\n")
            ics_file.write("DESCRIPTION:" + data_translate[n][0] + " VS " + data_translate[n][1] + "\n")
            ics_file.write("SEQUENCE:0\n")
            ics_file.write("STATUS:CONFIRMED\n")
            ics_file.write("SUMMARY:" + data_translate[n][0] + " VS " + data_translate[n][1] + "\n")
            ics_file.write("END:VEVENT\n")
        ics_file.write("END:VCALENDAR\n")
        ics_file.close()
    return

def create_ics_structure(list_values):
    list_values = list_values
    os.chdir('../../')
    global data
    global inf
    folder = 'test/'+sys.argv[1]
    with open(folder, "r") as fichero:
        data = json.load(fichero)
        fichero.close()
    inf = cnf.get_arguments(data)
    data_translate = list(map(translate_event, list_values))[:-1]
    create_file_ics(data_translate)
    return

def main(nameFile):
    list_values = cnf.get_valid_literals(nameFile)
    create_ics_structure(list_values)

if __name__ == "__main__":
    main(nameFile)