# README

## Basic Design

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
    
## Design

After importing the list, either from the output of previous trials or the original list if it is the first trial, the program makes sure that the dataframe is set up correctly with its three columns: School, Type, and Location. Then, it opens up a Chrome window and attempts to make a Google search for each school, starting from a specific index. If it cannot find confirmation that search results were found, it assumes that it has been caught by captcha, exports all data it has already scraped, prints the failed index, and quits. If it does find results, it finds and navigates to the corresponding Wikipedia page. From there the program sees if it can identify the school's type from the presence of either a "grades" element or an "undergraduates" element. It then extracts all text from the location section of the page. From here it checks the title for type clues then sets the type for the school. It also formats and sets the location. It repeats this process for each school on the list. Finally, once it either finishes or runs into an error, it quits the driver and exports the gathered data to the .csv file.

There are two large issues I ran into while writing this code. My solution of manually entering the starting point each run to evade Captcha would not be great for larger sets of data. While there are methods to get around this trap, I did not think any of them were necessary for this small project as I could just manually set the starting point and retry the scrape without much effort. This is not the best long-term solution and would not be great for longer lists of data but it worked fine for this project.

The other problem I ran into was the method for scraping the location data. Since the web elements were not constant between schools, it was difficult to find a way to extract only the state and country for each school. It was much simpler to just extract all the text from the location parent element than to track all of the different ids and class names for the more specific target elements. This resulted in an uneven location column as many articles did not include every aspect of location or changed the display order.
