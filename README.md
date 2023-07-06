Scrapeinator - SERP program that scrapes google search results given a search query and the number of results desired.

This program makes use of the requests, BeautifulSoup, re, and csv modules of python to scrape the required search query
and store the results in a .csv file. The YouTube Data API is also uesd to get channel details.

To run the program, go into the Code Folder and run scrapeinator.py file.
Make sure the required dependencies are installed before executing the file.

The data scraped from my run of the code is stored in data.csv, inside the Code folder.
It contains the link of the search result, the link to the YouTube channel that posted the video, the name of the YouTube Channel,
and the title of the uploaded video.

This data contains only 219 out of the required 10,000 results as google does not return any further results beyond result number
220. The 220th result itself is a page saying that no further results were found for the given search query.

This may be due to Google blocking further automated requests. If this is the case, the ways I can think of combatting this are:
- To either use the Google Custome Search JSON API, but this would require me to spend $5 to get the desired number of requests
- Another option is to possibly rotate IP addresses, but this also leads to the same issue as when searching for results beyind result
  220 once again returns with Google saying that there are no more results.

Link to the Scraper in Action :
https://drive.google.com/file/d/1ToqabYg83E1ejsgEYjub6fENSTPxhYXy/view?usp=sharing
