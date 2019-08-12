###For a brief description of this file, please see the README.

###Imports##############################################################################################################
#Packages to manually install: urllib3, requests
import csv
import urllib3
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

###Parameters###########################################################################################################
current_dir = 'C:\\Users\\Robin\\Documents\\Robin\\Entrepreneurs_Web_Scraping\\Main_Programming\\Companies'
website_url = 'https://techcrunch.com/startup-battlefield/' #Website url of list of companies
website_name = 'TechCrunch' #What you name the website
pre_website_tag = '"company_name":"' #tag before company name to identify/parse company name
post_website_tag = ' (' #tag after company name to identify/parse company name

###Defining Functions###################################################################################################
#create_csv(path): Creates .csv file in directory "path"
def create_csv(path):
    f = open(path,'w')
    f.close()

#write_txt(path,html_data): Creates .txt file and writes html data in directory "path"
def write_txt(path,html_data):
    f = open(path,'w')
    f.write(str(html_data.encode("utf-8")))
    f.close()

#remove_duplicates(list): Removes duplicates in "list" while maintaining original order
def remove_duplicates(list):
    new_list = []
    for i in list:
        if i not in new_list:
            new_list.append(i)
    return new_list

###Body#################################################################################################################
create_csv(current_dir + '\\' + website_name + '_Top_Sites.csv')

requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #Disables InsecureRequestWarning warning
http = urllib3.PoolManager() #"http" allows arbitrary requests + coordinating necessary connection pools
request = http.request('GET', website_url) #Requests extraction of html data of "website_url" from "http"
request_bytes2string = request.data.decode("utf-8") #Decodes extracted html data from (byte) to (string)
website_html = request_bytes2string

companies_list = []#Companies will be appended to "companies_list"

for character in range(len(website_html)):#Searches characters of "website_url"
    if(character < (len(website_html) - 18)): #Limits html data searching area
        if(website_html[character:character+len(pre_website_tag)] == pre_website_tag):#Websites are always preceded by "pre_website_tag"
            temp_html = website_html[character:]
            quote_position = temp_html.find(post_website_tag)#Websites are always succeeded by "post_website_tag"
            temp_company = temp_html[len(pre_website_tag):quote_position]#Parses website name
            companies_list.append(temp_company)#Appends website to "companies_list"
            companies_list = remove_duplicates(companies_list) #Removes duplicates in "companies_list"

#Opens "(website_name)_Top_Sites.csv", writes every element of "companies_list" to rows of .csv file
with open((website_name + '_Top_Sites.csv'),'w',newline='') as fp:
    a = csv.writer(fp,delimiter=',')
    for i in range(len(companies_list)):
        a.writerows(zip([companies_list[i]]))

#Creates "(website_name)_html_Entire_Page.txt", writes entire website html to .txt file
write_txt(current_dir + '\\' + website_name + '_html_Entire_Page.txt',website_html)

###Print Status#########################################################################################################
print('Run complete.')