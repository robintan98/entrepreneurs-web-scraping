###For a brief description of this file, please see the README.

###Imports##############################################################################################################
#Packages to manually install: urllib3, requests, google, selenium
import shutil
import time
from get_html_data import *
from find_forbes_page import *
from get_age import *
from get_billionaires_list import*
from get_education import *
from get_fun_facts import *
from get_marital_status import *
from get_net_worth import *
from get_num_of_children import *
from get_residence import *
from get_source_of_wealth import*
from get_title import*

###Parameters###########################################################################################################
current_dir = 'C:\\Users\\Robin\\Documents\\Robin\\Entrepreneurs_Web_Scraping\\Main_Programming\\Forbes\\Data'
folder_name = 'Forbes_Billionaires' #Folder name
billionaires_list_type = 'Excel' #Acceptable: 'Individual','Forbes','Excel'. Default is 'Individual'
billionaire_name = 'Sergey Brin' #For individual billionaire ("Individual")
chromedriver_path = 'C:\\Users\\Robin\\Documents\\Robin\\Entrepreneurs_Web_Scraping\\Main_Programming\\selenium' \
                        '\\chromedriver_win32\\chromedriver.exe' #For Forbes ("Forbes")
num_of_billionaires = 200 #For Forbes
billionaires_list_file = 'C:\\Users\\Robin\\Documents\\Robin\\Entrepreneurs_Web_Scraping\\Main_Programming\\Forbes' \
                        '\\Forbes_Billionaires_200.csv'

###Defining Functions###################################################################################################

def write_txt(path,data,num):
    if num == 0:
        if os.path.exists(current_dir + '\\' + billionaire_name + '.txt') == True:
            os.remove(current_dir + '\\' + billionaire_name + '.txt')
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
        if os.path.exists(current_dir + '\\' + billionaire_name + '.csv') == True:
            os.remove(current_dir + '\\' + billionaire_name + '.csv')
        f = open(path, 'w')
    if num == 1:
        f = open(path, 'a')
    csv = open(current_dir + '\\' + billionaire_name + '.csv', 'a')
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

def create_dir(path,folder_name):
    folder_name = folder_name.replace(' ','_')
    folder_name = folder_name + '_Data'
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

age_data = []
age_data_index = []
education_data = []
education_data_index = []
marital_status_data = []
marital_status_data_index = []
noc_data = []
noc_data_index = []
residence_data = []
residence_data_index = []

if billionaires_list_type == 'Forbes':
    billionaires_list = get_billionaires_list(chromedriver_path,num_of_billionaires)
    print(billionaires_list)
elif billionaires_list_type == 'Excel':
    billionaires_list = open_csv_file(billionaires_list_file)
    billionaires_list = billionaires_list[158:]###
else:
    billionaires_list = [billionaire_name]
print('Billionaire or Billionaires list created.')
current_dir = create_dir(current_dir,folder_name)
print('Directory created.')
print('Beginning billionaires scraping.')

countdown = 0

for i in billionaires_list:

    if str(type(i)) == '<class \'list\'>':
        billionaire_name = i[0]
    else:
        billionaire_name = i

    billionaire_name_header_t = 'Billionaire: "'
    billionaire_name_header_c = 'Billionaire:,'
    write_txt(current_dir + '\\' + billionaire_name + '.txt', billionaire_name_header_t
              + str(billionaire_name) + '"', 0)
    write_csv(current_dir + '\\' + billionaire_name + '.csv', billionaire_name, billionaire_name_header_c, 0)
    print(billionaire_name_header_t + str(billionaire_name) + '"')

    billionaire_Forbes_url = find_forbes_page(billionaire_name)
    billionaire_Forbes_url_header_t = 'Forbes url: '
    billionaire_Forbes_url_header_c = 'Forbes url:,'
    write_txt(current_dir + '\\' + billionaire_name + '.txt', billionaire_Forbes_url_header_t
              + str(billionaire_Forbes_url), 1)
    write_csv(current_dir + '\\' + billionaire_name + '.csv', billionaire_Forbes_url
              , billionaire_Forbes_url_header_c, 1)
    print(billionaire_Forbes_url_header_t + billionaire_Forbes_url)

    billionaire_Forbes_html_data = get_html_data(billionaire_Forbes_url)

    billionaire_title = get_title(billionaire_Forbes_html_data)
    billionaire_title_header_t = billionaire_name + '\'s title: '
    billionaire_title_header_c = billionaire_name + '\'s title:,'
    write_txt(current_dir + '\\' + billionaire_name + '.txt', billionaire_title_header_t + str(billionaire_title), 1)
    billionaire_title_c = str(billionaire_title).replace(',',' -')
    write_csv(current_dir + '\\' + billionaire_name + '.csv', billionaire_title_c
              , billionaire_title_header_c, 1)
    print(billionaire_title_header_t + billionaire_title)

    billionaire_net_worth = get_net_worth(billionaire_Forbes_html_data)
    billionaire_net_worth_header_t = billionaire_name + '\'s net worth: '
    billionaire_net_worth_header_c = billionaire_name + '\'s net worth:,'
    write_txt(current_dir + '\\' + billionaire_name + '.txt', billionaire_net_worth_header_t
              + str(billionaire_net_worth)
              , 1)
    write_csv(current_dir + '\\' + billionaire_name + '.csv', billionaire_net_worth
              , billionaire_net_worth_header_c, 1)
    print(billionaire_net_worth_header_t + billionaire_net_worth)

    billionaire_age = get_age(billionaire_Forbes_html_data)
    billionaire_age_header_t = billionaire_name + '\'s age: '
    billionaire_age_header_c = billionaire_name + '\'s age:,'
    write_txt(current_dir + '\\' + billionaire_name + '.txt', billionaire_age_header_t + str(billionaire_age), 1)
    write_csv(current_dir + '\\' + billionaire_name + '.csv', billionaire_age
              , billionaire_age_header_c, 1)
    print(billionaire_age_header_t + billionaire_age)

    billionaire_education = get_education(billionaire_Forbes_html_data)
    billionaire_education_header_t = billionaire_name + '\'s education: '
    billionaire_education_header_c = billionaire_name + '\'s education:,'
    write_txt(current_dir + '\\' + billionaire_name + '.txt', billionaire_education_header_t
              + str(billionaire_education), 1)
    billionaire_education_c = billionaire_education.replace(',',' -')
    billionaire_education_c = billionaire_education_c.replace(';',',')
    write_csv(current_dir + '\\' + billionaire_name + '.csv', billionaire_education_c
              , billionaire_education_header_c, 1)
    print(billionaire_education_header_t + str(billionaire_education))

    billionaire_sow = get_source_of_wealth(billionaire_Forbes_html_data)
    billionaire_sow_header_t = billionaire_name + '\'s source of wealth: '
    billionaire_sow_header_c = billionaire_name + '\'s source of wealth:,'
    write_txt(current_dir + '\\' + billionaire_name + '.txt', billionaire_sow_header_t + str(billionaire_sow), 1)
    billionaire_sow_c = billionaire_sow.replace(',', ' -')
    write_csv(current_dir + '\\' + billionaire_name + '.csv', billionaire_sow_c
              , billionaire_sow_header_c, 1)
    print(billionaire_sow_header_t + billionaire_sow)

    billionaire_residence = get_residence(billionaire_Forbes_html_data)
    billionaire_residence_header_t = billionaire_name + '\'s residence: '
    billionaire_residence_header_c = billionaire_name + '\'s residence:,'
    write_txt(current_dir + '\\' + billionaire_name + '.txt', billionaire_residence_header_t
              + str(billionaire_residence), 1)
    billionaire_residence_c = billionaire_residence.replace(',',' -')
    write_csv(current_dir + '\\' + billionaire_name + '.csv', billionaire_residence_c
              , billionaire_residence_header_c, 1)
    print(billionaire_residence_header_t + billionaire_residence)
    
    billionaire_marital_status = get_marital_status(billionaire_Forbes_html_data)
    billionaire_marital_status_header_t = billionaire_name + '\'s marital status: '
    billionaire_marital_status_header_c = billionaire_name + '\'s marital status:,'
    write_txt(current_dir + '\\' + billionaire_name + '.txt', billionaire_marital_status_header_t
              + str(billionaire_marital_status), 1)
    write_csv(current_dir + '\\' + billionaire_name + '.csv', billionaire_marital_status
              , billionaire_marital_status_header_c, 1)
    print(billionaire_marital_status_header_t + billionaire_marital_status)

    billionaire_noc = get_num_of_children(billionaire_Forbes_html_data)
    print(billionaire_noc)
    billionaire_noc_header_t = billionaire_name + '\'s number of children: '
    billionaire_noc_header_c = billionaire_name + '\'s number of children:,'
    write_txt(current_dir + '\\' + billionaire_name + '.txt', billionaire_noc_header_t + str(billionaire_noc), 1)
    write_csv(current_dir + '\\' + billionaire_name + '.csv', billionaire_noc
              , billionaire_noc_header_c, 1)
    print(billionaire_noc_header_t + billionaire_noc)
    
    billionaire_fun_facts = get_fun_facts(billionaire_Forbes_html_data)
    billionaire_fun_facts_header_t = billionaire_name + '\'s fun facts: '
    billionaire_fun_facts_header_c = billionaire_name + '\'s fun facts:,'
    write_txt(current_dir + '\\' + billionaire_name + '.txt', billionaire_fun_facts_header_t
              + str(billionaire_fun_facts), 1)
    billionaire_fun_facts_c = ''
    for i in billionaire_fun_facts:
        billionaire_fun_facts_c_temp = i.replace(',','-')
        billionaire_fun_facts_c = billionaire_fun_facts_c + ',' + billionaire_fun_facts_c_temp
    billionaire_fun_facts_c = billionaire_fun_facts_c[1:]
    write_csv(current_dir + '\\' + billionaire_name + '.csv', billionaire_fun_facts_c
              , billionaire_fun_facts_header_c, 1)
    print(billionaire_fun_facts_header_t + str(billionaire_fun_facts))

    if billionaire_age not in age_data:
        age_data.append(billionaire_age)
        age_data_index.append(1)
    else:
        age_data_index[age_data.index(billionaire_age)] = age_data_index[age_data.index(billionaire_age)] + 1

    billionaire_education_d = billionaire_education[billionaire_education.find(',')+2:]
    if billionaire_education_d not in education_data:
        education_data.append(billionaire_education_d)
        education_data_index.append(1)
    else:
        education_data_index[education_data.index(billionaire_education_d)] \
            = education_data_index[education_data.index(billionaire_education_d)] + 1
    
    if billionaire_marital_status not in marital_status_data:
        marital_status_data.append(billionaire_marital_status)
        marital_status_data_index.append(1)
    else:
        marital_status_data_index[marital_status_data.index(billionaire_marital_status)] \
            = marital_status_data_index[marital_status_data.index(billionaire_marital_status)] + 1
    
    if billionaire_noc not in noc_data:
        noc_data.append(billionaire_noc)
        noc_data_index.append(1)
    else:
        noc_data_index[noc_data.index(billionaire_noc)] = noc_data_index[noc_data.index(billionaire_noc)] + 1

    billionaire_residence_d = billionaire_residence[billionaire_residence.find(',') + 2:]
    if billionaire_residence_d not in residence_data:
        residence_data.append(billionaire_residence_d)
        residence_data_index.append(1)
    else:
        residence_data_index[residence_data.index(billionaire_residence_d)] \
            = residence_data_index[residence_data.index(billionaire_residence_d)] + 1

    print('Age Data: ' + str(age_data))
    print('Age Data Index: ' + str(age_data_index))
    print('Education Data: ' + str(education_data))
    print('Education Data Index: ' + str(education_data_index))
    print('Marital Status Data: ' + str(marital_status_data))
    print('Marital Status Data Index: ' + str(marital_status_data_index))
    print('Number of Children Data: ' + str(noc_data))
    print('Number of Children Data Index: ' + str(noc_data_index))
    print('Residence Data: ' + str(residence_data))
    print('Residence Data Index: ' + str(residence_data_index))

    # time.sleep(5)
    countdown = countdown + 1
    print('Finished scraping Billionaire #' + str(countdown) + '.')
    # if countdown%4 == 0:
    #     time.sleep(300)

###Print Status#########################################################################################################
print('Run complete.')