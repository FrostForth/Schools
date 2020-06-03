# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:54:20 2020

@author: Kaitlin

1. Import libraries
    - os
    - pandas
    - selenium
2. Set up dataframes
    1. import schools from file
    2. add and name columns (School, Type, Location)
3. Make searches
    1. For each row:
        1. google search for school
        2. navigate to wikipedia page
        3. return grade level/type, location
        4. store values in proper columns
4. Export data
    1. standardize values
    2. export to csv file
"""

#import libraries
import os
import pandas as pd
from selenium import webdriver

#set up dataframes
x = 50
schools = pd.read_csv(os.getcwd()+'\schools.csv', names=['School', 'Type', 'Location'])
randschools = schools.sample(n=x).reset_index(drop=True)
print(randschools.School)
f = open('output.txt', 'w')


#make searches
exec_path = "C:\\WebDriver\\bin\\chromedriver.exe"
chrome = webdriver.Chrome(executable_path=exec_path)

for i in range(len(randschools)):
    # create search query
    school = randschools.School[i]
    school = school.replace(' ', '+')
    
    #navigate to google search
    chrome.get("https://www.google.com/search?q=" + school)
    
    #set variables
    schooltype = ""
    switch = 0
    location = ''
    """city = ''
    state = ''
    country = ''"""
        
    try: #select wikipedia link
        
        wiki = chrome.find_element_by_xpath('//a[contains(@href, "wikipedia")]').get_attribute('href')
        chrome.get(wiki)
        
        #handle grade: if grade section then high school, if undergrad or grad section then college
        
        try: #check if high school
                chrome.find_element_by_xpath('//th[text()="Grades"]')
                switch = 1
        except:
            try:
                chrome.find_element_by_xpath('//a[text()="Undergraduates"]')
                switch = 2
            except: print("Failed to find type from "+chrome.title, file=f)
    
        #handle location
        
        try:
            try: location = chrome.find_element_by_xpath('//tr[@class="adr"]').text
            except: location = chrome.find_element_by_xpath('//td[@class="adr"]').text
        
        except: print('Failed to identify location for {}'.format(chrome.find_element_by_class_name('firstHeading').text), file=f)

    except: print(":( "+chrome.title, file=f)
    
    if 'high' in school.lower() or switch == 1: schooltype = 'High School'
    elif ('university' in school.lower() or 'college' in school.lower()) or switch ==2: schooltype = 'University'
    randschools.Type[i] = schooltype
    #randschools.Location[i] = '{}, {}, {}'.format(city, state, country)
    location = location.replace('\n', ', ')
    randschools.Location[i] = location

print(randschools.Type.head())    
print(randschools.Location.head())
randschools.to_csv('randschools.csv')
f.close()

#driver.quit()
    
#export data