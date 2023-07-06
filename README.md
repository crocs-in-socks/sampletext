Scrapeinator - SERP program that scrapes google search results given a search query and the number of results desired.

This program makes use of the Selenium, BeautifulSoup, re, and csv modules of python to scrape the required search query
and store the results in a .csv file.

To run the program, go into the Code Folder and run scrapeinator.py file.
Make sure the required dependencies are installed before executing the file.

The data scraped from my run of the code is stored in data.csv, inside the Code folder.
It contains the link of the search result, the link to the YouTube channel that posted the video, the name of the YouTube Channel,
and the title of the uploaded video.

The pre-existing data.csv contains the first 10,000 results of the google search query : "site:youtube.com openinapp.co"

For better performance, make sure to add the "headless" argument to the web-driver. This has been left on to record the video of the
scraper in action.

Link to the Scraper in Action :
https://drive.google.com/file/d/1ToqabYg83E1ejsgEYjub6fENSTPxhYXy/view?usp=sharing
