# Script to fill in level and location of schools from Google results

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
    
So basically after importing the list, either from the output of previous trials or the original list if it is the first trial, we make sure the dataframe is set up correctly with its three columns: School, Type, and Location. Then, we open up a Chrome window and attempt to make a Google search for each school, starting from a specific index. If it cannot find confirmation that search results were found, it will assume that it has been caught by captcha, export all data it has already scraped, print the failed index, and quit. If it does find results, it will find and navigate to the corresponding Wikipedia page. From there it will see if it can identify the school's type from the presence of either a "grades" element or an "undergraduates" element. It then extracts all text from the location section of the page. From here it checks the title for type clues then sets the type for the school. It also formats and sets the location. It repeats this process for each school on the list. Finally, once it either finishes or runs into an error, it quits the driver and exports the gathered data to the .csv file.

There are two large issues I ran into while writing this code, however. My solution of manually entering the starting point each run to evade Captcha is not great for larger sets of data. While there are methods to get around this trap, I did not think any of them were necessary for this small project as I could just manually set the starting point and retry the scrape. This is not the best long-term solution and would not be great for longer lists of data but it worked fine for this project.

The other problem I ran into was the method for scraping the location data. Since the web elements were not constant between schools, it was difficult to find a way to extract only the state and country for each school. It was much simpler to just extract all the text from the "adr" parent element than to track all of the different ids and class names for the more specific target elements. This resulted in an uneven and not uniform location column as many articles did not include every aspect of location or changed the display order.
