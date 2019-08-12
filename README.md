# entrepreneurs-web-scraping
Entrepreneurs Web Scraping Project
Summer 2018
=======================================
=: Description: A Python programming project I pursued during the summer of 2018 
in which I web-scraped popular websites like Wikipedia, TechCrunch, and IncomeDiary to
automate obtaining relevant information on rising entrepreneurs as well as founders 
and CEO's of successful companies. I was able to web-scrape information online using 
tools such as BeautifulSoup and Selenium. Near the end of the project, I explored 
improving the accuracy of the information mining as well as how to implement more 
sophisticated NLP methods.

=: main_Grabber.py: The main file for scraping Wikipedia for the information on the 
education (i.e. university attended, major studied) of a list of inputted entrepreneurs.
This program can output the information of a single entrepreneur or export the information 
of multiple entrepreneurs to Excel. Additionally, I used two types of simple NLP methods: 
a 'Bank' mode, where a bank of keywords is used, and a 'Fragment' mode, where sentence 
fragments are analyzed. I also created a simple UI as a visual component for users.

=: main_TechCrunch.py: The script I used to scrape a website (i.e. TechCrunch) for a list of 
startups/entrepreneurs. I used the Python urllib3 and requests package to request extraction of 
html data.

=: main_Wikipedia.py: The script I used to scrape Wikipedia for biographical information of 
founders of notable companies (i.e. on the Fortune 500 list).

=: main_Forbes.py: The script I used to scrape the Forbes Billionaires list in 
order to compile the age, education, marital status, number of children, and place 
of residence of the world's wealthiest billionaires. This program can output the 
information of a single billionaire or export the information of multiple billionaires 
to Excel.

=: main_IncomeDiary.py: The script I used to scrape the IncomeDiary list of entrepreneurs
in order to compile information of entrepreneur's educational, occupational, and biological 
data. This program can output the information of a single entreprenur or export the 
information of multiple entrepreneurs to Excel.
