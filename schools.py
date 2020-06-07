# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:54:20 2020

@author: Kaitlin

1. Import libraries
    - pandas
    - selenium webdriver
2. Set up dataframes
    1. import schools from file
    2. columns (School, Type, Location)
3. Make searches
    1. For each row:
        1. create search term from school name
        2. google search for school
            1. If caught by captcha then save index number and quit
        3. navigate to wikipedia page
            1. Find school type (High School or University)
            2. Find location
        4. format and store type and location
4. Export data
    1. close webdriver and output file
    2. export updated school list to csv file
"""

#import libraries
import pandas as pd
from selenium import webdriver

#set up dataframe
try: schools = pd.read_csv('updatedschools.csv')
except: schools = pd.read_csv('schools.csv', names=['School', 'Type', 'Location'])

try:
    schools.drop(columns=['index'], inplace=True)
    schools.drop(columns=['level_0'], inplace=True)
except: pass

schools.drop_duplicates(inplace=True)
schools.reset_index(inplace=True)

print(schools.head())
print(len(schools))
f = open('output.txt', 'a')

#start index
start = 0
print(str(pd.datetime.now())+"\nSTARTING SCRAPE {} = INDEX {}\n".format(schools.School[start],start), file=f)

#make searches
exec_path = "C:\\WebDriver\\bin\\chromedriver.exe"
chrome = webdriver.Chrome(executable_path=exec_path)

for i in range(start, len(schools)):
    # create search query
    school = schools.School[i]
    school = school.replace(' ', '+')
    
    #navigate to google search
    chrome.get("https://www.google.com/search?q=" + school)
    
    #handle being sent to captcha
    try: chrome.find_element_by_id('result-stats')
    except:
        try: chrome.find_element_by_class_name('hide-focus-ring')
        except:
            print('\nSEARCH BLOCKED AT {} = INDEX {}\n'.format(schools.School[i],i), file=f)
            break
    
    #set variables
    schooltype = ""
    switch = 0
    location = ''
        
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
            except: print("Type from wiki failed: "+chrome.title, file=f)
    
        #handle location
        
        try:
            try: location = chrome.find_element_by_xpath('//tr[@class="adr"]').text
            except: location = chrome.find_element_by_xpath('//td[@class="adr"]').text
        
        except: print('Location failed: {}'.format(chrome.find_element_by_class_name('firstHeading').text), file=f)

    except: print("Wikipedia failed: "+schools.School[i], file=f)
    
    #properly type school based on switch value and names
    if 'high' in school.lower() or switch == 1: schooltype = 'High School'
    elif ('university' in school.lower() or 'college' in school.lower()) or switch ==2: schooltype = 'University'
    schools.Type[i] = schooltype
    
    #set location
    location = location.replace('\n', ', ')
    schools.Location[i] = location

#quit driver
print("Closing driver "+str(pd.datetime.now()), file=f)
chrome.quit()
f.close()

#export data
schools.to_csv('updatedschools.csv', index=False)
