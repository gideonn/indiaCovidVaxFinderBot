# indiaCovidVaxFinderBot
Bot to keep querying for vaccination slots by pin code or district code for different age groups and alerting the user when the results are found.

Please note that the COWIN API is only accessible from Indian IPs, so you'll have to use a VPN 
(if you're not in India and want to run it for someone else).   
This should work fine with Indian IP address.  

Inputs:
* Age group: 18-45 or 45+
* Search by Pin code OR Search by District code (lookup table is saved as state_district.txt in the same directory as this file)
* Pin code/District Code

This bot will first build a data file (`state_district.txt`) with state codes and district codes for ease of search. 
Note that this is only generated on first run when the lookup file doesn't exist. 

Sample data:  
######################  
State ID	State Name  
######################  
1		Andaman and Nicobar Islands  
######################  
District ID	District Name  
######################  
3		Nicobar  
1		North and Middle Andaman  
2		South Andaman  


Then it'll search for all available vaccine slots every 60s (based on user inputs) and once it finds it, 
it saves the results in a file, and the computer/laptop will start generating alert sounds to notify you that it found results.

After that, the window can be safely closed, and the results can be seen in the file `results.txt` saved in the same directory as the main file.  
Conversely, if no results are found, the bot will retry after pausing for 60s.

The result has the following fields:
1. Date available
2. Fee type: Free/Paid
3. Center name, district, address of center, and State.
4. Vaccine name and count in the center
5. Available slots

Results Sample:  
################## Session Details: ##################  
Date Available: 05-05-2021. Fee type: Free  
Center name: KEM Hospital 1, District: Mumbai, Address: Acharya Donde Marg parel mumbai, Maharashtra  
Vaccine Name: COVISHIELD, Vaccine count: 126.  
Available Slots: ['11:30AM-01:30PM', '01:30PM-03:30PM', '03:30PM-05:30PM', '05:30PM-08:00PM']  
################## Session Details: ##################  
Date Available: 05-05-2021. Fee type: Free  
Center name: AKURLI MATERNITY KANDIVALI, District: Mumbai, Address: Akurli Road Kandivali East, Maharashtra  
Vaccine Name: COVISHIELD, Vaccine count: 2.  
Available Slots: ['12:00PM-01:00PM', '01:00PM-02:00PM', '02:00PM-03:00PM', '03:00PM-05:00PM']   

