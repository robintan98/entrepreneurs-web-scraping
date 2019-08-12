###For a brief description of this file, please see the README.

###Imports##############################################################################################################
#Packages to manually install: urllib3, requests, google, selenium, time
import csv
import os
import shutil
import time
from get_html_data import *
from find_wikipedia_page import *
from get_company_founders import *
from get_company_industries import*
from get_founders_education import *
from get_founders_majors import *
from get_founders_net_worth import *
from get_founders_occupations import *
from get_founders_ethnicities import *
from get_Fortune500_companies import *

###Parameters###########################################################################################################
current_dir = 'C:\\Users\\Robin\\Documents\\Robin\\Entrepreneurs_Web_Scraping\\Main_Programming\\Wikipedia\\Data'
company_list_name = 'Fortune500_6' #Folder name
company_list_type = 'Fortune500' #Acceptable: 'Individual','Fortune500', 'Excel'. Default is 'Individual'
company_name = 'Apple' #For individual company ("Individual")
website_list_file = 'C:\\Users\\Robin\\Documents\\Robin\\Entrepreneurs_Web_Scraping\\Main_Programming\\Companies' \
                    '\\Alexa_Top_Sites.csv'#For Alexa, TechCrunch, etc. ("Excel")
chromedriver_path = 'C:\\Users\\Robin\\Documents\\Robin\\Entrepreneurs_Web_Scraping\\Main_Programming\\selenium' \
                        '\\chromedriver_win32\\chromedriver.exe' #For Fortune500 ("Fortune500")
num_of_companies_Fortune500 = 500 #For Fortune500

###Defining Functions###################################################################################################

def write_txt(path,data,num):
    if num == 0:
        if os.path.exists(current_dir + '\\' + company_name + '.txt') == True:
            os.remove(current_dir + '\\' + company_name + '.txt')
        f = open(path, 'w')
    if num == 1:
        f = open(path,'a')
    data_str = str(data.encode('utf-8'))
    f.write(data_str[2:-1])
    f.write('\n')
    f.close()

def write_csv(path,data,header,num):
    data_temp = ''
    if num == 0:
        if os.path.exists(current_dir + '\\' + company_name + '.csv') == True:
            os.remove(current_dir + '\\' + company_name + '.csv')
        f = open(path, 'w')
    if num == 1:
        f = open(path, 'a')
    csv = open(current_dir + '\\' + company_name + '.csv', 'a')
    data_temp = data_temp + header

    if (str(type(data)) == '<class \'str\'>'):
        data_temp = data_temp + data
        data_temp = data_temp + '\n'
    elif (str(type(data)) == '<class \'list\'>'):
        for i in range(len(data)):
            data_temp = data_temp + str(data[i]) + ','
        data_temp = data_temp + '\n'
    csv.write(data_temp)
    f.close()

def create_dir(path,company_list_name):
    company_list_name = company_list_name.replace(' ','_')
    folder_name = company_list_name + '_Data'
    if os.path.exists(path + '\\' + folder_name) == True:
        shutil.rmtree(path + '\\' + folder_name, ignore_errors=True)
        os.mkdir(path + '\\' + folder_name)
    else:
        os.mkdir(path + '\\' + folder_name)
    current_dir = path + '\\' + folder_name
    return current_dir

def open_csv_file(path):
    if os.path.exists(path) == False:
        return ['-']
    website_list = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, quotechar='|')
        for row in reader:
            website_list.append(row)
    return website_list

###Body#################################################################################################################

if company_list_type == 'Fortune500':
    website_list = get_Fortune500_companies(chromedriver_path,num_of_companies_Fortune500)
elif company_list_type == 'Excel':
    website_list = open_csv_file(website_list_file)
else:
    website_list = [company_name]
print('Website or website list created.')
current_dir = create_dir(current_dir,company_list_name)
print('Directory created.')
print('Beginning company scraping.')

website_list = website_list[380:]#
cooldown_countdown = 1
for i in website_list:
    try:
        if type(i) is list:
            company_name = i[0]
        elif type(i) is str:
            company_name = i
        company_name_header = 'Company:,'
        write_txt(current_dir + '\\' + company_name + '.txt', 'Company: "' + str(company_name) + '"', 0)
        write_csv(current_dir + '\\' + company_name + '.csv', company_name, company_name_header, 0)
        print('Company: "' + str(company_name) + '"')

        company_wiki_url = find_wikipedia_page(company_name)
        company_wiki_url_header = 'Wikipedia url:,'
        write_txt(current_dir + '\\' + company_name + '.txt', 'Wikipedia url: ' + str(company_wiki_url), 1)
        write_csv(current_dir + '\\' + company_name + '.csv', company_wiki_url, company_wiki_url_header, 1)
        print('Wikipedia url: ' + company_wiki_url)

        company_wiki_html_data = get_html_data(company_wiki_url)

        company_founders_list = get_company_founders(company_wiki_html_data)
        print(company_founders_list)
        company_founders_list_new = []
        if company_founders_list == ['-']:
            company_founders_list_new = ['-No founders found-']
        else:
            for i in range(len(company_founders_list)):
                company_founders_list_new.append(company_founders_list[i][0])
        company_founders_list_header = 'Company founders:,'
        write_txt(current_dir + '\\' + company_name + '.txt', 'Company founders: ' + str(company_founders_list_new), 1)
        write_csv(current_dir + '\\' + company_name + '.csv', company_founders_list_new, company_founders_list_header, 1)
        print('Company founders: ' + str(company_founders_list_new))

        company_industries_list = get_company_industries(company_wiki_html_data)
        company_industries_list_new = []
        if company_industries_list == ['-']:
            company_industries_list_new = ['-No industries found-']
        else:
            company_industries_list_new = company_industries_list
        company_industries_list_header = 'Company industries:,'
        write_txt(current_dir + '\\' + company_name + '.txt', 'Company industries: ' + str(company_industries_list_new), 1)
        write_csv(current_dir + '\\' + company_name + '.csv', company_industries_list_new, company_industries_list_header, 1)
        print('Company industries: ' + str(company_industries_list_new))

        for founder in company_founders_list:
            founders_wiki_url = founder[1]
            founders_wiki_html_data = get_html_data(founders_wiki_url)

            founders_education_list = get_founders_education(founders_wiki_html_data)
            founders_education_list_new = []
            if founders_education_list == ['-']:
                founders_education_list_new = ['-No education found-']
            else:
                founders_education_list_new = founders_education_list
            founders_education_header = founder[0] + '\'s education:,'
            write_txt(current_dir + '\\' + company_name + '.txt', founder[0] + '\'s education: '
                      + str(founders_education_list_new), 1)
            write_csv(current_dir + '\\' + company_name + '.csv', founders_education_list_new, founders_education_header, 1)
            print(founder[0] + '\'s education: ' + str(founders_education_list_new))

            founders_majors_list = get_founders_majors(founders_wiki_html_data)
            founders_majors_list_new = []
            if founders_majors_list == ['-']:
                founders_majors_list_new = ['-No majors found-']
            else:
                founders_majors_list_new = founders_majors_list
            founders_majors_header = founder[0] + '\'s majors:,'
            write_txt(current_dir + '\\' + company_name + '.txt', founder[0]
                      + '\'s majors and areas of studies of interest: ' + str(founders_majors_list_new), 1)
            write_csv(current_dir + '\\' + company_name + '.csv', founders_majors_list_new, founders_majors_header, 1)
            print(founder[0] + '\'s majors and areas of studies of interest: ' + str(founders_majors_list_new))

            founders_net_worth = get_founders_net_worth(founders_wiki_html_data)
            founders_net_worth_new = ''
            if founders_net_worth == '$-':
                founders_net_worth_new = '-No net worth found-'
            else:
                founders_net_worth_new = founders_net_worth.replace(',','')
                founders_net_worth_new = 'USD' + founders_net_worth_new
            founders_net_worth_header = founder[0] + '\'s net worth:,'
            write_txt(current_dir + '\\' + company_name + '.txt', founder[0]
                      + '\'s net worth (if known) is: ' + str(founders_net_worth), 1)
            write_csv(current_dir + '\\' + company_name + '.csv', founders_net_worth_new, founders_net_worth_header, 1)
            print(founder[0] + '\'s net worth (if known) is: ' + founders_net_worth)

            founders_occupations_list = get_founders_occupations(founders_wiki_html_data)
            founders_occupations_list_new = []
            if founders_occupations_list == ['-']:
                founders_occupations_list_new = ['-No occupations found-']
            else:
                founders_occupations_list_new = founders_occupations_list
            founders_occupations_header = founder[0] + '\'s occupations:,'
            write_txt(current_dir + '\\' + company_name + '.txt', founder[0]
                      + '\'s occupations and interests are: ' + str(founders_occupations_list_new), 1)
            write_csv(current_dir + '\\' + company_name + '.csv', founders_occupations_list_new,
                      founders_occupations_header, 1)
            print(founder[0] + '\'s occupations and interests are: ' + str(founders_occupations_list_new))

            founders_ethnicities_list = get_founders_ethnicities(founders_wiki_html_data)
            founders_ethnicities_list_new = []
            if founders_ethnicities_list == ['-']:
                founders_ethnicities_list_new = ['-No ethnicities found-']
            else:
                founders_ethnicities_list_new = founders_ethnicities_list
            founders_ethnicities_header = founder[0] + '\'s ethnicities:,'
            write_txt(current_dir + '\\' + company_name + '.txt', founder[0]
                      + '\'s ethnicity(s)/country(s) of origin are: ' + str(founders_ethnicities_list_new), 1)
            write_csv(current_dir + '\\' + company_name + '.csv', founders_ethnicities_list_new,
                      founders_ethnicities_header, 1)
            print(founder[0] + '\'s ethnicity(s)/country(s) of origin are: ' + str(founders_ethnicities_list_new))
            time.sleep(2)
            cooldown_countdown = cooldown_countdown + 1
            print(cooldown_countdown)
            if cooldown_countdown%5 == 0:
                print('cooling')
                time.sleep(180)
    except ValueError:
        continue
    except IndexError:
        continue
    # except urllib.HTTPError:
    #     continue



###Print Status#########################################################################################################
print('Run complete.')