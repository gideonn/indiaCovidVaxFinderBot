#!/usr/bin/env python3

import datetime
import json
import time
import requests
import os
import certifi

os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

def util_beep():
    for i in range(1000):
        time.sleep(0.5)
        print('\a', end='', flush=True)


def util_get_states():
    STATE_DISTRICT_LOOKUP_FILE = "state_district.txt"
    if os.path.isfile(STATE_DISTRICT_LOOKUP_FILE) and os.path.getsize(STATE_DISTRICT_LOOKUP_FILE) > 0:
        # file already present. Skip generating the lookup table.
        return
    else:
        print("Building state district data file. Please refer to state_district.txt when searching by district id.")
        state_district_file = open(STATE_DISTRICT_LOOKUP_FILE, "a")

    response = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states')
    json_data = json.loads(response.text)

    for state in json_data['states']:
        state_district_file.write('\n###########################\n' + 'State ID\tState Name\n' + '############################\n')
        state_district_file.write(str(state['state_id']) + '\t\t' + state['state_name'])
        state_district_file.write('\n############################\n' + 'District ID\tDistrict Name\n' + '############################\n')
        for district in util_get_districts_by_state(state['state_id']):
            state_district_file.write(str(district['district_id']) + '\t\t' + district['district_name'] + '\n')

    state_district_file.close()


def util_get_districts_by_state(state_id):
    response = requests.get("https://cowin.gov.in/api/v2/admin/location/districts/{}".format(state_id))
    json_data = json.loads(response.text)
    return json_data['districts']


def util_get_current_formatted_date():
    # The API expects date in this format
    return datetime.datetime.now().strftime("%d-%m-%Y")


def process_response(response, age_group):
    slot_found = False
    json_data = json.loads(response.text)
    for center in json_data['centers']:
        for session in center['sessions']:
            if session['min_age_limit'] == age_group and session['available_capacity'] > 0:
                # clear data of old file
                if not slot_found:
                    open("results.txt", "w").close()
                    # open same file in append mode
                    results_file = open("results.txt", "a")

                print("\n################## Session Details: ##################\n")
                print("Date Available: {}. Fee type: {} \n".format(session['date'], center['fee_type']))
                print("Center name: {}, District: {}, Address: {}, {} \n".format(center['name'], center['district_name'], center['address'], center['state_name']))
                print("Vaccine Name: {}, Vaccine count: {}. \nAvailable Slots: {} \n".format(session['vaccine'], session['available_capacity'], session['slots']))

                results_file.write("################## Session Details: ##################\n")
                results_file.write("Date Available: {}. Fee type: {} \n".format(session['date'], center['fee_type']))
                results_file.write("Center name: {}, District: {}, Address: {}, {} \n".format(center['name'], center['district_name'], center['address'], center['state_name']))
                results_file.write("Vaccine Name: {}, Vaccine count: {}. \nAvailable Slots: {} \n".format(session['vaccine'], session['available_capacity'], session['slots']))

                # mark slot as found for alert and clearing file content
                slot_found = True

    if slot_found:
        results_file.close()
        print("\n##########################################################################################\n Results saved. You can close this window. Please check results.txt for vaccine slots! \n##########################################################################################\n")
        util_beep()
    else:
        print("No results found! Retrying after 60s")


def get_7day_vaccination_info_by_pin(age_group, formatted_date, pincode):
    url = 'https://cowin.gov.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}'
    response = requests.get(url.format(pincode, formatted_date))
    process_response(response, age_group)


def get_7day_vaccination_info_by_district(age_group, formatted_date, dist_id):
    url = 'https://cowin.gov.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}'
    response = requests.get(url.format(dist_id, formatted_date))
    process_response(response, age_group)


def search_vaccine():
    print("\n##########################################################################################\n Your results will be saved as results.txt in the same directory as this file! \n##########################################################################################\n")

    age_group = int(input('Please specify min age (Enter "18" for 18-45, "45" for 45+): '))
    search_method = int(input('Find vaccine by pin code OR by district code? Enter 1 for pin, 2 for district: '))

    if age_group == 18:
        print('Searching 7-days vaccine slot for min age 18')
    elif age_group == 45:
        print('Searching 7-days vaccine slot for min age 45')
    else:
        exit('Invalid input! Please run again with valid inputs!')

    if search_method == 1:
        print('Searching for vaccine by pin code...')
        pincode = int(input('Enter the pin code: '))

        # keep looping until slot is found
        while True:
            get_7day_vaccination_info_by_pin(age_group, util_get_current_formatted_date(), pincode)
            time.sleep(60)
    elif search_method == 2:
        print('Searching for vaccine by district code...')
        dist_id = int(input('Enter the district id (refer the file state_district.txt): '))

        # keep looping until slot is found
        while True:
            get_7day_vaccination_info_by_district(age_group, util_get_current_formatted_date(), dist_id)
            time.sleep(60)
    else:
        exit('Invalid Input! Please run again with valid inputs!')


def main():
    util_get_states()
    search_vaccine()


if __name__ == "__main__":
    main()
