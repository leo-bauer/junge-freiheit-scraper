# junge-freiheit-scraper
Python Scraper for the archive of German weekly Junge Freiheit

The file 01_scraper.py contains the scraper. As it is now, the scraper stores all articles of a given volume that are accessible via a URL and records data for three variables: date, article title, article URL and article text. The archive of Junge Freiheit is freely accessible and contains all volumes since 1997.  

The scraper utilizes the Selenium WebDriver package to scrape webpages via a browser. To scrape I used Firefox browser (v.84, 64-bit) which requires downloading the geckodriver to work with Selenium. Download geckodriver from https://github.com/mozilla/geckodriver/releases, save the geckodriver.exe file in a local file directory and enter the path in the scraper.py file under '# test geckodriver and selenium'. 

The scraper is built to download one volume of the newspaper at a time. As such, certain parameters in the code need to be changed before scraping the individual volumes. As uploaded here, the scraper is set to scrape the 2020 volume of the newspaper. To scrape a volume, start with entering the URL of that volume under '# download website'. To obtain the volume's URL, visit https://jungefreiheit.de/archiv/, right click on the volume (i.e., year) you want to scrape, select 'Open in new tab' and copy the URL of that page. Next, enter this URL again under '# store urls'. Having entered the URL twice, run the scraper until '# scrape href attributes from all issues of that year'. 

The last len() function returns the number of issues of the volume you want to scrape. As the number of issues per volume varies across years, pay attention to the number and enter it in the range() function as the number after 0 under '# scrape href attributes from all issues of that year'. Next, run the whole for loop and the code that follows until '# append all list items to get complete urls'. Under '# append all list items to get complete urls' you need to insert once again the URL of the volume you want to scrape. After inserting, run the three lines of code and check the number that is returned by the len() function. This count of all articles in the volume (which of course also varies across volumes) then needs to be inserted in the next range() function (under # retrieve text data) as the number after 0. Next, run the whole code under 'retrieve text data', which scrapes all the individual articles from the volume. 

As Junge Freiheit has a small circulation and thus probably not , I included a sleep function in the for loop to not exhaust server resources with the scraping effort. Thus, scraping a full volume may take up to 9 hours, at least on my computer. To make the computer usable for other tasks during scraping, I also suppressed the opening of automated Firefox browser windows, which can be changed in the beginning of the file under 'suppress geckodriver window', if you want to monitor progress with article scraping. After scraping of the volume is finished, use the code under '# create data frame' to bring the data into a tabular form. Finally, use the function under '# export to csv' to store the volume locally as a .csv file. As a last point, in certain volumes only partial dates are retrieved for some articles. To correct for this, execute the code under one of the two '# add missing...' sections. I noted the volumes to which the functions apply respectively.

Shortcomings: As it is, the scraper does not capture the author name in a separate variable. This is due to the fact that I could not (thus far) find a reliable method to retrieve this information. In addition, the title variable only stores part of the title in many cases (and the title was not important for my project): The title tag contains both date and title separated by a slash, yet some titles contain slashes inside of them, leading to the split function only retrieving the last part of the article's title. However, this could be changed by removing the split function from the block of code that retrieves the title variable so that the full title tag is stored in the title variable. It would be up to you to then remove the dates from all titles. 

Lastly, the file 02_create_single_data_set.py is there to concat the individual data sets of the volumes to form one large data set with all scraped articles, remove duplicates, create a date variable in datetime format from the original string date variable and sort the full data set by date, before storing it yet again in a .csv file.
