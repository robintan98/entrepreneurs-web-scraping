###For a brief description of this file, please see the README.

###Imports##############################################################################################################
#Packages to manually install: urllib3, requests, google, selenium, time
import csv
import os
import shutil
import time
from get_html_data import *
from find_wikipedia_page import *
from find_wikipedia_page_ID import *
from get_founders_education import *
from get_founders_majors import *
from get_founders_net_worth import *
from get_founders_occupations import *
from get_founders_ethnicities import *
from get_Fortune500_companies import *

###Parameters###########################################################################################################
current_dir = 'C:\\Users\\Robin\\Documents\\Robin\\Entrepreneurs_Web_Scraping\\Main_Programming\\Wikipedia\\Data'
company_list_name = 'IncomeDiary_5' #Folder name
company_list_type = 'Excel' #Acceptable: 'Individual','Fortune500', 'Excel'. Default is 'Individual'
company_name = 'Apple' #For individual company ("Individual")
website_list_file = 'C:\\Users\\Robin\\Documents\\Robin\\Entrepreneurs_Web_Scraping\\Main_Programming\\IncomeDiary' \
                    '\\Entrepreneurs_List.csv'#For Alexa, TechCrunch, etc. ("Excel")
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

def write_csv(path,data,name,header,num):
    data_temp = ''
    if num == 0:
        if os.path.exists(current_dir + '\\' + name + '.csv') == True:
            os.remove(current_dir + '\\' + name + '.csv')
        f = open(path, 'w')
    if num == 1:
        f = open(path, 'a')
    csv = open(current_dir + '\\' + name + '.csv', 'a')
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

def convert_list_to_string(list):
    string = ''
    count = 1
    for i in list:
        if count != len(list):
            string = string + i + ' - '
            count = count + 1
        else:
            string = string + i
    return string


###Body#################################################################################################################

if company_list_type == 'Fortune500':
    website_list = get_Fortune500_companies(chromedriver_path,num_of_companies_Fortune500)
elif company_list_type == 'Excel':
    website_list = open_csv_file(website_list_file)
else:
    website_list = [company_name]
print('Entrepreneur list created.')
current_dir = create_dir(current_dir,company_list_name)
print('Directory created.')
print('Beginning entrepreneur scraping.')

website_list = website_list[98:]#
csv_name = 'Entrepreneurs Data'
cooldown_countdown = 1

flat_file_header_list = []
flat_file_header_list.append('')
flat_file_header_list.append('Education')
flat_file_header_list.append('Majors')
flat_file_header_list.append('Net Worth')
flat_file_header_list.append('Occupations')
flat_file_header_list.append('Ethnicities')
write_csv(current_dir + '\\' + 'Income Diary Flat File' + '.csv', flat_file_header_list, 'Income Diary Flat File',
          '', 1)

for i in website_list:
    try:
        if type(i) is list:
            entrepreneur_name = i[0]
        else:
            entrepreneur_name = i
        entrepreneur_name_header = 'Entrepreneur:,'
        write_txt(current_dir + '\\' + entrepreneur_name + '.txt', 'Entrepreneur: "' + str(entrepreneur_name) + '"', 1)
        write_csv(current_dir + '\\' + entrepreneur_name + '.csv', entrepreneur_name, entrepreneur_name,
                  entrepreneur_name_header, 1)
        write_csv(current_dir + '\\' + entrepreneur_name + '.csv', entrepreneur_name, csv_name, entrepreneur_name_header, 1)
        print('Entrepreneur: "' + str(entrepreneur_name) + '"')

        entrepreneur_wiki_url = find_wikipedia_page_ID(entrepreneur_name)
        entrepreneur_wiki_url_header = 'Wikipedia url:,'
        write_txt(current_dir + '\\' + entrepreneur_name + '.txt', 'Wikipedia url: ' + str(entrepreneur_wiki_url), 1)
        write_csv(current_dir + '\\' + entrepreneur_name + '.csv', entrepreneur_wiki_url, entrepreneur_name,
                  entrepreneur_wiki_url_header, 1)
        write_csv(current_dir + '\\' + entrepreneur_name + '.csv', entrepreneur_wiki_url, csv_name, entrepreneur_wiki_url_header, 1)
        print('Wikipedia url: ' + entrepreneur_wiki_url)

        entrepreneur_wiki_html_data = get_html_data(entrepreneur_wiki_url)

        entrepreneurs_education_list = get_founders_education(entrepreneur_wiki_html_data)
        entrepreneurs_education_list_new = []
        if entrepreneurs_education_list == ['-']:
            entrepreneurs_education_list_new = ['-No education found-']
        else:
            entrepreneurs_education_list_new = entrepreneurs_education_list
        entrepreneurs_education_header = entrepreneur_name + '\'s education:,'
        write_txt(current_dir + '\\' + entrepreneur_name + '.txt', entrepreneur_name + '\'s education: '
                  + str(entrepreneurs_education_list_new), 1)
        write_csv(current_dir + '\\' + entrepreneur_name + '.csv', entrepreneurs_education_list_new, entrepreneur_name,
                  entrepreneurs_education_header, 1)
        write_csv(current_dir + '\\' + entrepreneur_name + '.csv', entrepreneurs_education_list_new, csv_name, entrepreneurs_education_header, 1)
        print(entrepreneur_name + '\'s education: ' + str(entrepreneurs_education_list_new))

        entrepreneurs_majors_list = get_founders_majors(entrepreneur_wiki_html_data)
        entrepreneurs_majors_list_new = []
        if entrepreneurs_majors_list == ['-']:
            entrepreneurs_majors_list_new = ['-No majors found-']
        else:
            entrepreneurs_majors_list_new = entrepreneurs_majors_list
        entrepreneurs_majors_header = entrepreneur_name + '\'s majors:,'
        write_txt(current_dir + '\\' + entrepreneur_name + '.txt', entrepreneur_name
                  + '\'s majors and areas of studies of interest: ' + str(entrepreneurs_majors_list_new), 1)
        write_csv(current_dir + '\\' + entrepreneur_name + '.csv', entrepreneurs_majors_list_new, entrepreneur_name,
                  entrepreneurs_majors_header, 1)
        write_csv(current_dir + '\\' + entrepreneur_name + '.csv', entrepreneurs_majors_list_new, csv_name, entrepreneurs_majors_header, 1)
        print(entrepreneur_name + '\'s majors and areas of studies of interest: ' + str(entrepreneurs_majors_list_new))

        entrepreneurs_net_worth = get_founders_net_worth(entrepreneur_wiki_html_data)
        entrepreneurs_net_worth_new = ''
        if entrepreneurs_net_worth == '$-':
            entrepreneurs_net_worth_new = '-No net worth found-'
        else:
            entrepreneurs_net_worth_new = entrepreneurs_net_worth.replace(',','')
            entrepreneurs_net_worth_new = 'USD' + entrepreneurs_net_worth_new
        entrepreneurs_net_worth_header = entrepreneur_name + '\'s net worth:,'
        write_txt(current_dir + '\\' + entrepreneur_name + '.txt', entrepreneur_name
                  + '\'s net worth (if known) is: ' + str(entrepreneurs_net_worth), 1)
        write_csv(current_dir + '\\' + entrepreneur_name + '.csv', entrepreneurs_net_worth_new, entrepreneur_name,
                  entrepreneurs_net_worth_header, 1)
        write_csv(current_dir + '\\' + entrepreneur_name + '.csv', entrepreneurs_net_worth_new, csv_name, entrepreneurs_net_worth_header, 1)
        print(entrepreneur_name + '\'s net worth (if known) is: ' + entrepreneurs_net_worth)

        entrepreneurs_occupations_list = get_founders_occupations(entrepreneur_wiki_html_data)
        entrepreneurs_occupations_list_new = []
        if entrepreneurs_occupations_list == ['-']:
            entrepreneurs_occupations_list_new = ['-No occupations found-']
        else:
            entrepreneurs_occupations_list_new = entrepreneurs_occupations_list
        entrepreneurs_occupations_header = entrepreneur_name + '\'s occupations:,'
        write_txt(current_dir + '\\' + entrepreneur_name + '.txt', entrepreneur_name
                  + '\'s occupations and interests are: ' + str(entrepreneurs_occupations_list_new), 1)
        write_csv(current_dir + '\\' + entrepreneur_name + '.csv', entrepreneurs_occupations_list_new, entrepreneur_name,
                  entrepreneurs_occupations_header, 1)
        write_csv(current_dir + '\\' + entrepreneur_name + '.csv', entrepreneurs_occupations_list_new, csv_name,
                  entrepreneurs_occupations_header, 1)
        print(entrepreneur_name + '\'s occupations and interests are: ' + str(entrepreneurs_occupations_list_new))

        entrepreneurs_ethnicities_list = get_founders_ethnicities(entrepreneur_wiki_html_data)
        entrepreneurs_ethnicities_list_new = []
        if entrepreneurs_ethnicities_list == ['-']:
            entrepreneurs_ethnicities_list_new = ['-No ethnicities found-']
        else:
            entrepreneurs_ethnicities_list_new = entrepreneurs_ethnicities_list
        entrepreneurs_ethnicities_header = entrepreneur_name + '\'s ethnicities:,'
        write_txt(current_dir + '\\' + entrepreneur_name + '.txt', entrepreneur_name
                  + '\'s ethnicity(s)/country(s) of origin are: ' + str(entrepreneurs_ethnicities_list_new), 1)
        write_csv(current_dir + '\\' + entrepreneur_name + '.csv', entrepreneurs_ethnicities_list_new, entrepreneur_name,
                  entrepreneurs_ethnicities_header, 1)
        write_csv(current_dir + '\\' + entrepreneur_name + '.csv', entrepreneurs_ethnicities_list_new, csv_name,
                  entrepreneurs_ethnicities_header, 1)
        print(entrepreneur_name + '\'s ethnicity(s)/country(s) of origin are: ' + str(entrepreneurs_ethnicities_list_new))

        flat_file_data_temp = []
        flat_file_data_temp.append(entrepreneur_name)
        entrepreneurs_education_string_new_ff = convert_list_to_string(entrepreneurs_education_list_new)
        flat_file_data_temp.append(entrepreneurs_education_string_new_ff)
        entrepreneurs_majors_string_new_ff = convert_list_to_string(entrepreneurs_majors_list_new)
        flat_file_data_temp.append(entrepreneurs_majors_string_new_ff)
        flat_file_data_temp.append(entrepreneurs_net_worth_new)
        entrepreneurs_occupations_string_new_ff = convert_list_to_string(entrepreneurs_occupations_list_new)
        flat_file_data_temp.append(entrepreneurs_occupations_string_new_ff)
        entrepreneurs_ethnicities_string_new_ff = convert_list_to_string(entrepreneurs_ethnicities_list_new)
        flat_file_data_temp.append(entrepreneurs_ethnicities_string_new_ff)
        write_csv(current_dir + '\\' + 'Income Diary Flat File' + '.csv', flat_file_data_temp,
                  'Income Diary Flat File','', 1)

        # time.sleep(2)
        cooldown_countdown = cooldown_countdown + 1
        print(cooldown_countdown)
        # if cooldown_countdown%5 == 0:
        #     print('cooling')
        #     time.sleep(180)

    except ValueError:
        continue
    except IndexError:
        continue
    # except urllib3.error.HTTPError:
    #     continue



###Print Status#########################################################################################################
print('Run complete.')