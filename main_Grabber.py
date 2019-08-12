###For a brief description of this file, please see the README.

###Grabber##############################################################################################################
#Generalized grabber using fragments or bank

###Imports##############################################################################################################
#Necessary imports: google, requests, nltk, beautifulsoup4, graphics
import os
import csv
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from nltk import tokenize
from urllib import error
import urllib
from graphics import *
from get_education import *

###Parameters###########################################################################################################

###List of Toggles

#scrape_type: Scrapers either using 'Bank' or 'Fragment' method

#For "Fragment' mode
#info_isAlpha: Determines whether important information should be alphabetical or not

#For 'Bank' mode
#use_UI: Determines whether the program uses Grabber's UI or not

#toggle_write_csv: "1" if data is written to .csv, "0" if data is not written to .csv
#toggle_write_txt: "1" if data is written to .txt, "0" if data is not written to .txt

#Path of .csv file for the list of subjects (in this case, subjects = entrepreneurs) (for subject_input_type = 'List')
subjects_list_path = r'C:\Users\Robin\Documents\Robin\Entrepreneurs_Web_Scraping\Main_Programming\Grabber_Final\additional_files\Entrepreneurs_List.csv'
#Name of subject (for subject_input_type = 'Individual')
subject_name = 'Sergey Brin'
#Subject input type ('List' for list of subjects or 'Individual' for only one subject) (default)
subject_input_type = 'List'
#Path of current_dir (where the .csv file will be created)
current_dir = r'C:\Users\Robin\Documents\Robin\Entrepreneurs_Web_Scraping\Main_Programming\Grabber_Final\Grabber_Data'
#Path of .csv file containing most common words in English
most_common_words_path = r'C:\Users\Robin\Documents\Robin\Entrepreneurs_Web_Scraping\Main_Programming\Grabber_Final\Additional_Files\most_common_words.csv'
#Number of subjects from subjects list to be scraped
num_of_subjects = 100
#First subject in subjects list to be scraped
starting_subject = 0
#Number of important paragraphs to be written to .csv file
max_important_paragraphs = 3
#Name of .csv file to be created
csv_name = 'Grabbed_Entrepreneurs_Educations_1'
#Name of .txt file to be created
txt_name = 'Grabbed_Entrepreneurs_Education_1'
#List of keywords to find "important" paragraphs
necessary_keyword_list = ['University','College','School','Institute']
#List of auxiliary keywords("important" sentences must contain one of these)
specific_keyword_list_auxiliary = ['degree','Bachelor','Master','bachelor','master','B.S.',
                                   'MBA','M.S.','B.A.','PhD','Ph.D']
#List of important keywords to find information for fragments ("important" sentences must contain one of these)
specific_keyword_list_important_1 = ['receive','graduate','has','hold','attend','obtain','earn','acquire','studied',
                                     'major']
#If there is a common word that needs to be skipped
common_word_skip = '-No skip-' #'-No skip-' if there is no skip needed
#If there is a common word that needs to precede info
common_word_precede = '-Important-' #'-Important-' if the preceded word is the important word
#List of keywords for scrape type 'Bank'
bank_keyword_list = ['accounting','actuarial science','anthropology',
                      'archaeology','architectural engineering','architecture','biochemistry',
                      'bioengineering','biology','biophysics','biotechnology','business administration',
                      'chemical engineering','chemistry','civil engineering','computer engineering',
                      'computer science','design','earth science','economics','electrical engineering',
                      'environmental systems engineering','environmental science','film studies',
                      'finance','food science','forest science','general science','geography','geoscience',
                      'graphic design','horticulture','industrial engineering','information science',
                      'journalism','marine biology','marketing','mathematics','mechanical engineering',
                      'meteorology''microbiology','music','nuclear engineering','nursing','nutrition',
                      'philosophy','physics','physiology','political science','psychology','public relations',
                      'real estate','religious studies','sociology','communication','statistics',
                      'telecommunications','theater','women\'s studies', 'literature',
                      'operations','manufacturing engineering','aerospace engineering','engineering',
                      'English','history',' art ','politics',
                      'management','business','pre-law','applied physics','applied mathematics','materials science',
                      'information management','electrical and electronics engineering','commerce','East Asian studies',
                      'theoretical physics','econometrics','graphic design','industrial design','operations research',
                      'symbolic systems','epistemology','cognitive science','biomedical engineering',
                      'electronic engineering','software engineering','computational science','information systems',
                      'neoclassical social theory','management science','visual arts',
                      'MBA','J.D.','juris doctor','Juris Doctor']
#Each list-within-list takes first element, finds if middle elements are in sentence, and replaces first element with third element
bank_keyword_replace_list =  [['MBA','','business'],['J.D.','','law'],['juris doctor','','law'],
                              ['Juris Doctor','','law']]
#If the info needs to be letters only
info_isAlpha = True
#Determines number of sentences above and below important sentence (for scrape type 'Bank')
important_sentence_search_range = 1
#UI Window dimensions
win_width = 1200
win_height = 500
#Word to be searched along with ""http://en.wikipedia......" to find Wikipedia URL
google_wikipedia_search_word = 'entrepreneur'
#Determines if scrape type is 'Fragment' or 'Bank'
scrape_type = 'Bank'
#Determines whether to use UI or not (True to use, False to not use) (only for 'Bank')
use_UI = 1
#If use_UI = 0: Sets default confidence as high, medium or low
no_UI_options = 3 #3 means high confidence, 2 means medium confidence, 1 means low confidence, only works if use_UI = 0
#Toggles whether data will be written to .csv or .txt file (0 = no write, 1 = write) (0 is default)
toggle_write_csv = 0
toggle_write_txt = 0

#Writes a csv_header list for first row of headers for .csv file
csv_header = []
csv_header.append('Entrepreneur Number')
csv_header.append('Entrepreneur Name')
csv_header.append('Wikipedia URL')
for num in range(max_important_paragraphs):
    para_name_temp = 'Paragraph ' + str(num + 1)
    csv_header.append(para_name_temp)
csv_header.append('Important Sentences')
csv_header.append('Information')
csv_header.append('Education')

###Functions############################################################################################################
##open_csv_file(path):
#Input: path of .csv file ('str')
#Output: list of data in .csv file ('list')
def open_csv_file(path):
    if os.path.exists(path) == False: #Returns '-' if path does not exist
        return ['-']
    list = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, quotechar='|')
        for row in reader:
            list.append(row) #Appends data in row to "list"
    return list

##find_wikipedia_page(subject_name):
#Input: name of subject ('str')
#Output: Wikipedia URL of subject's wiki page ('str')
def find_wikipedia_page(entrpreneur_name):
    subject_wiki_url = ''
    for url in search('"en.wikipedia.org/wiki ' + entrpreneur_name + ' ' + google_wikipedia_search_word, stop=1):
        #Uses google's package to find wikipedia URL
        subject_wiki_url = url
        break
    if(subject_wiki_url == '' or subject_wiki_url.find('wikipedia') == -1):
        #Filters whether URL is from Wikipedia
        return ('-')
    else:
        return(subject_wiki_url)

##get_html_data(website_url):
#Input: Website URL of sujbect's Wikipedia URL ('str')
#Output: Raw HTML data requested from requests from website URL ('str')
def get_html_data(website_url):
    if(website_url == '-'): #Returns '-' if website URL does not exist
        return '-'
    else:
        page = requests.get(website_url) #Obtains byte data from website_url using requests
        html_contents = page.text #Converts page byte data to string
        return html_contents

##write_csv(website_url):
#Input: data that is to be inputted ('str'), name of file ('str'), header for first row ('str'), num for printing('int')
#Output: -
def write_csv(data,name,header,num):
    data_temp = '' #Data to be written to .csv
    if num == 0: #Switch 0: Removes existing file, then writes and opens new .csv file
        if os.path.exists(current_dir + '\\' + name + '.csv') == True:
            os.remove(current_dir + '\\' + name + '.csv')
        f = open(current_dir + '\\' + name + '.csv', 'w',encoding='UTF-8')
    if num == 1: #Switch 1: Writes and opens new .csv file
        f = open(current_dir + '\\' + name + '.csv', 'a')
    csv = open(current_dir + '\\' + name + '.csv', 'a',encoding='UTF-8')
    data_temp = data_temp + header #Adds a header to row

    if (str(type(data)) == '<class \'str\'>'): #If data is type 'str'
        data_temp = data_temp + data
        data_temp = data_temp + '\n'
    elif (str(type(data)) == '<class \'list\'>'): #If data is type 'list'
        for i in range(len(data)):
            data_temp = data_temp + str(data[i]) + ','
        data_temp = data_temp + '\n'
    csv.write(data_temp)
    f.close()

##write_txt(path,data,name,num):
#Input: path of .txt ('str'), data to be written ('str'), name of file ('str'), num for printing('int')
#Output: -
def write_txt(path,data,name,num):
    if num == 0:
        if os.path.exists(path + '\\' + name + '.txt') == True:
            os.remove(path + '\\' + name + '.txt')
        f = open(path + '\\' + name + '.txt', 'w', encoding='utf-8')
    else:
        f = open(path + '\\' + name + '.txt','a', encoding='utf-8')
    f.write(data)
    f.close()

##convert_list_to_string(list):
#Input: list to be converted to str ('list')
#Output: str of converted list, with dashes to separate elements ('str')
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

##replace_element_in_list(list,original_word,replace_word:
#Input: list that has element to be replaced('list'), original element ('str'), element that replaces original ('str')
#Output: list wiht replaced element ('str')
def replace_element_in_list(list,original_word,replace_word):
    for element in list:
        if element == original_word:
            list.remove(element)
            list.append(replace_word)
    return list

###Body#################################################################################################################
if scrape_type == 'Fragment': #'Fragment' mode
    print('Scrape type: "Fragment"')

    if subject_input_type == 'List': #(for subject_input_type = 'List')
        subjects_list = open_csv_file(subjects_list_path) #Creates subjects_list by opening subjects list.csv file
    else: #(for subject_input_type = 'Individual')
        subjects_list = [[subject_name]]

    subjects_list_new = [] #Filters list-within-list, duplicates in subjects_list
    for subject in subjects_list:
        if subject not in subjects_list_new:
            subjects_list_new.append(subject[0])
    subjects_list = subjects_list_new
    subjects_list = subjects_list[starting_subject:num_of_subjects]

    if toggle_write_csv == 1:
        write_csv(csv_header,csv_name,'',0) #Writes headers to first row of .csv file
    else:
        pass

    subject_count = 0
    httperror_cooldown_count = -1 #Helps when HTTPError is encountered
    for subject in subjects_list: #Iterates through each subject
        try:
            subject_count = subject_count + 1
            print('Subject #' + str(subject_count) + ' - ' + subject)
            subject_wiki_url = find_wikipedia_page(subject) #Gets Wikipedia URL of subject
            subject_wiki_html_data_raw = get_html_data(subject_wiki_url) #Get raw html data from subject's Wikipedia URL
            soup = BeautifulSoup(subject_wiki_html_data_raw, 'html.parser') #Parses raw html into soup
            subject_wiki_html_data = (soup.get_text()) #Converts byte data into 'str' from soup

            relevant_wiki_paragraphs_list = []
            relevant_wiki_text_paragraph_split = subject_wiki_html_data.split('\n') #Splits html into raw paragraphs
            for possible_paragraph in relevant_wiki_text_paragraph_split: #Processes paragraphs (>200 characters)
                if len(possible_paragraph) > 200:
                    relevant_wiki_paragraphs_list.append(possible_paragraph)

            specific_keyword_list = []  # Creates a specific keyword list containing all specific keywords
            specific_keyword_list.append(specific_keyword_list_auxiliary)
            specific_keyword_list.append(specific_keyword_list_important_1)

            important_paragraphs_list = []
            for keyword in necessary_keyword_list:  # Searches for important paragraphs from relevant paragraphs using keyword_list
                for relevant_paragraph in relevant_wiki_paragraphs_list:
                    if relevant_paragraph.find(keyword) > -1:
                        important_paragraphs_list.append(relevant_paragraph)

            important_paragraphs_list_new = []
            for important_paragraph in important_paragraphs_list:
                #Processes important paragraphs by replacing commas with dashes, filtering out standard Wiki html sentences
                try: #Passes that subject's important paragraph if UnicodeError occurs
                    if important_paragraph not in important_paragraphs_list_new \
                            and important_paragraph.find('window.RLQ=window.RL') == -1\
                            and important_paragraph.find('mw.loader.load') == -1:
                        important_paragraph = important_paragraph.replace(',','-')
                        important_paragraphs_list_new.append(important_paragraph)
                except UnicodeEncodeError: #In case a foreign character is encounetered
                    print('UnicodeError occured.')
                    pass
            important_paragraphs_list = important_paragraphs_list_new
            print(important_paragraphs_list)

            important_paragraphs_max_list = ['-']*max_important_paragraphs
            #important paragraph max list formats important paragraphs so that it can be written to .csv
            if len(important_paragraphs_list) >= max_important_paragraphs:
                important_paragraphs_max_list = important_paragraphs_list[0:max_important_paragraphs]
            else:
                important_paragraph_count = 0
                for important_paragraph in important_paragraphs_list:
                    important_paragraphs_max_list[important_paragraph_count] = important_paragraph
                    important_paragraph_count = important_paragraph_count + 1

            subjects_education = get_subjects_education(subject_wiki_html_data_raw) #Specialized

            html_data_sentence_split = tokenize.sent_tokenize(subject_wiki_html_data) #Tokenizes paragraphs into sentences
            sentence_count = 0
            for sentence in html_data_sentence_split:
                sentence_count = sentence_count + 1

            most_common_words_list = open_csv_file(most_common_words_path) #Creates most common word list by reading in .csv
            most_common_words_list_new = []
            for common_word in most_common_words_list: #Filters list-within-list, removes duplicates
                if common_word[0] not in most_common_words_list_new:
                    most_common_words_list_new.append(common_word[0])
            most_common_words_list = most_common_words_list_new

            important_sentence =  ''
            for sentence in html_data_sentence_split:
                #Finds important sentences (must contain one word from each specific keyword list)
                keyword_list_count_toggle = [0]*len(specific_keyword_list)
                keyword_list_count = 0
                keyword_list_index = 0
                for keyword_list in specific_keyword_list:
                    for keyword in keyword_list:
                        if sentence.find(keyword) > -1:
                            if keyword_list_count_toggle[keyword_list_index] == 0:
                                keyword_list_count = keyword_list_count + 1
                                break
                            keyword_list_count_toggle[keyword_list_index] = 1
                    keyword_list_index = keyword_list_index + 1
                if keyword_list_count == len(specific_keyword_list):
                    important_sentence = sentence
                    break

            important_sentence = important_sentence.replace(',',' -') #Replaces ',' with ' -' in important_sentence
            important_sentence = important_sentence.replace('.','')
            important_sentence_split = important_sentence.split(' ') #Splits important_sentence into words
            print(important_sentence_split)

            common_word_index_list = [0]*len(important_sentence_split)
            uncommon_word_index_list = [0] * len(important_sentence_split)
            word_index_count = 0
            for word in important_sentence_split:
                if word.lower() in most_common_words_list:
                    common_word_index_list[word_index_count] = 1 #Creates list of indices of common words (i.e. "and")
                else:
                    uncommon_word_index_list[word_index_count] = 1 #Creates list of indices of uncommon words (i.e. "math")
                word_index_count = word_index_count + 1

            ##Fragment:

            frag_important_list = specific_keyword_list_important_1 #Find location of the first important word
            frag_important_location = 0
            for word in important_sentence_split:
                for keyword in frag_important_list:
                    if word.find(keyword) > -1:
                        frag_important_location = important_sentence_split.index(word)
                        break

            if common_word_precede == '-Important-': #Precede location is important location if precede word is '-Important'
                frag_precede_location = frag_important_location
            else:
                #Finds precede location using common_word_precede
                word_index_counter = 0
                frag_precede_location = -1
                for word in important_sentence_split:
                    if word_index_counter > frag_important_location and word == common_word_precede:
                        if info_isAlpha == True:
                            if important_sentence_split[word_index_counter + 1].isalpha() == True:
                                frag_precede_location = word_index_counter
                                break
                        else:
                            frag_precede_location = word_index_counter
                            break
                    word_index_counter = word_index_counter + 1

            #Creates index list for common words
            word_index_counter = 0
            frag_common_word_index_list = []
            frag_common_word_index_counter = 0
            skip_switch = 0
            for word in important_sentence_split:
                if word_index_counter > frag_precede_location and frag_precede_location != -1:
                    if common_word_index_list[word_index_counter] == 1:
                        if common_word_skip == '-No skip-': #If no common word needs to be skipped
                            frag_common_word_index_list.append(word_index_counter)
                            frag_common_word_index_counter = frag_common_word_index_counter + 1
                        else:
                            if word == common_word_skip:
                                if skip_switch == 0:
                                    skip_switch = 1
                                else:
                                    frag_common_word_index_list.append(word_index_counter)
                                    frag_common_word_index_counter = frag_common_word_index_counter + 1
                            else:
                                frag_common_word_index_list.append(word_index_counter)
                                frag_common_word_index_counter = frag_common_word_index_counter + 1
                word_index_counter = word_index_counter + 1
            if frag_common_word_index_list == []:
                frag_common_word_index_list = [len(important_sentence_split)]

            #Finds important information using fragments built from important words
            word_index_counter = 0
            frag_information_list = []
            for word in important_sentence_split:
                if word_index_counter > frag_precede_location and word_index_counter > frag_common_word_index_list[0] \
                        and word_index_counter < frag_common_word_index_list[1]:
                    frag_information_list.append(word)
                word_index_counter = word_index_counter + 1

            #Processes important information
            frag_information = ''
            for word in frag_information_list:
                word.replace('.', '')
                word.replace('and', '-')
                word.replace(',', ' -')
                frag_information = frag_information + word + ' '
            frag_information = frag_information[:len(frag_information) - 1]
            print(subject + '\'s information: ' + frag_information)

            #Print all information into .csv via flat_file_data_temp
            flat_file_data_temp = []
            flat_file_data_temp.append(subject_count)
            flat_file_data_temp.append(subject)
            flat_file_data_temp.append(subject_wiki_url)
            for important_paragraph in important_paragraphs_max_list:
                flat_file_data_temp.append(important_paragraph)
            flat_file_data_temp.append(frag_information)
            flat_file_data_temp.append(convert_list_to_string(subjects_education))
            print(flat_file_data_temp)

            # Print all information into .txt
            txt_data_temp = ''
            txt_data_temp += 'Entrepreneur ' + str(subject_count) + ': ' + subject + '\n'
            txt_data_temp += 'Wikipedia URL: ' + subject_wiki_url + '\n'
            important_paragraph_count = 0
            for important_paragraph in important_paragraphs_max_list:
                important_paragraph_count = important_paragraph_count + 1
                txt_data_temp += 'Paragraph ' + str(important_paragraph_count) + ': ' + important_paragraph + '\n'
            txt_data_temp += 'Information: ' + frag_information + '\n'
            txt_data_temp += 'Education: ' + convert_list_to_string(subjects_education) + '\n'
            txt_data_temp += '\n'

            if toggle_write_txt == 1:  #Writes txt_data_temp into .txt file
                if subject_count == 1:
                    write_txt(current_dir, txt_data_temp, txt_name, 0)
                else:
                    write_txt(current_dir, txt_data_temp, txt_name, 1)
            else:
                pass

            if toggle_write_csv == 1: #Writes flat_file_data_temp into .csv file
                write_csv(flat_file_data_temp,csv_name,'',1) #Writes flat_file_data_temp into .csv file
            else:
                pass

        except urllib.error.HTTPError: #Catches HTTPError if error occurs
            print('HTTPError occured.')
            httperror_cooldown_count = httperror_cooldown_count + 1
            time.sleep(600 + httperror_cooldown_count*60) #Stops the program for 10 + x minutes to quell HTTPError

elif scrape_type == 'Bank':
    print('Scrape type: "Bank"')

    if subject_input_type == 'List': #(for subject_input_type = 'List')
        subjects_list = open_csv_file(subjects_list_path) #Creates subjects_list by opening subjects list.csv file
    else: #(for subject_input_type = 'Individual')
        subjects_list = [[subject_name]]

    subjects_list_new = [] #Filters list-within-list, duplicates in subjects_list
    for subject in subjects_list:
        if subject not in subjects_list_new:
            subjects_list_new.append(subject[0])
    subjects_list = subjects_list_new
    subjects_list = subjects_list[starting_subject:num_of_subjects]

    if toggle_write_csv == 1:
        write_csv(csv_header,csv_name,'',0) #Writes headers to first row of .csv file
    else:
        pass

    subject_count = 0
    httperror_cooldown_count = -1
    for subject in subjects_list: #Iterates through each subject
        try:
            subject_count = subject_count + 1
            print('Subject #' + str(subject_count) + ' - ' + subject)
            subject_wiki_url = find_wikipedia_page(subject) #Gets Wikipedia URL of subject
            subject_wiki_html_data_raw = get_html_data(subject_wiki_url) #Get raw html data from subject's Wikipedia URL
            soup = BeautifulSoup(subject_wiki_html_data_raw, 'html.parser') #Parses raw html into soup
            subject_wiki_html_data = (soup.get_text()) #Converts byte data into 'str' from soup

            relevant_wiki_paragraphs_list = []
            relevant_wiki_text_paragraph_split = subject_wiki_html_data.split('\n') #Splits html into raw paragraphs
            for possible_paragraph in relevant_wiki_text_paragraph_split: #Processes paragraphs (>200 characters)
                if len(possible_paragraph) > 200:
                    relevant_wiki_paragraphs_list.append(possible_paragraph)

            specific_keyword_list = []  # Creates a specific keyword list containing all specific keywords
            specific_keyword_list.append(specific_keyword_list_auxiliary)
            specific_keyword_list.append(specific_keyword_list_important_1)
            specific_keyword_list.append(necessary_keyword_list)

            important_paragraphs_list = []
            for keyword in necessary_keyword_list:  # Searches for important paragraphs from relevant paragraphs using keyword_list
                for relevant_paragraph in relevant_wiki_paragraphs_list:
                    if relevant_paragraph.find(keyword) > -1:
                        important_paragraphs_list.append(relevant_paragraph)

            important_paragraphs_list_new = []
            for important_paragraph in important_paragraphs_list:
                #Processes important paragraphs by replacing commas with dashes, filtering out standard Wiki html sentences
                try: #Passes that subject's important paragraph if UnicodeError occurs
                    if important_paragraph not in important_paragraphs_list_new \
                            and important_paragraph.find('window.RLQ=window.RL') == -1\
                            and important_paragraph.find('mw.loader.load') == -1:
                        important_paragraph = important_paragraph.replace(',','-')
                        important_paragraphs_list_new.append(important_paragraph)
                except UnicodeEncodeError:
                    print('UnicodeError occured.')
                    pass
            important_paragraphs_list = important_paragraphs_list_new

            important_paragraphs_max_list = ['-']*max_important_paragraphs
            #important paragraph max list formats important paragraphs so that it can be written to .csv
            if len(important_paragraphs_list) >= max_important_paragraphs:
                important_paragraphs_max_list = important_paragraphs_list[0:max_important_paragraphs]
            else:
                important_paragraph_count = 0
                for important_paragraph in important_paragraphs_list:
                    important_paragraphs_max_list[important_paragraph_count] = important_paragraph
                    important_paragraph_count = important_paragraph_count + 1

            subjects_education = get_subjects_education(subject_wiki_html_data_raw) #Specialized

            html_data_sentence_split = tokenize.sent_tokenize(subject_wiki_html_data) #Tokenizes paragraphs into sentences
            sentence_count = 0
            for sentence in html_data_sentence_split:
                sentence_count = sentence_count + 1

            # Creates index list for sentences in html_data_sentence_split
            sentence_split_index_list = range(len(html_data_sentence_split))

            most_common_words_list = open_csv_file(most_common_words_path) #Creates most common word list by reading in .csv
            most_common_words_list_new = []
            for common_word in most_common_words_list: #Filters list-within-list, removes duplicates
                if common_word[0] not in most_common_words_list_new:
                    most_common_words_list_new.append(common_word[0])
            most_common_words_list = most_common_words_list_new

            high_confidence_sentence_list = []
            medium_confidence_sentence_list = []
            low_confidence_sentence_list = []

            important_sentence_list = []
            important_sentence_index_list = []
            sentence_split_count = 0
            for sentence in html_data_sentence_split:
                #Finds important sentences (must contain one word from each specific keyword list)
                keyword_list_count_toggle = [0]*len(specific_keyword_list)
                keyword_list_count = 0
                keyword_list_index = 0
                for keyword_list in specific_keyword_list:
                    for keyword in keyword_list:
                        if sentence.find(keyword) > -1:
                            if keyword_list_count_toggle[keyword_list_index] == 0:
                                keyword_list_count = keyword_list_count + 1
                                break
                            keyword_list_count_toggle[keyword_list_index] = 1
                    keyword_list_index = keyword_list_index + 1
                if keyword_list_count == len(specific_keyword_list): #Collects "high confidence" sentences
                    high_confidence_sentence_list.append([sentence, 'High', sentence_split_count])
                if keyword_list_count == len(specific_keyword_list) - 1:
                    medium_confidence_sentence_list.append([sentence, 'Medium', sentence_split_count]) #Collects "medium confidence" sentences
                if keyword_list_count == len(specific_keyword_list) - 2:
                    low_confidence_sentence_list.append([sentence, 'Low', sentence_split_count]) #Collects "low confidence" sentences

                if keyword_list_count == len(specific_keyword_list):
                    important_sentence_list.append(sentence)
                    important_sentence_index_list.append(sentence_split_count)

                if use_UI == 0:
                    if no_UI_options == 3:
                        if keyword_list_count == len(specific_keyword_list):
                            important_sentence_list.append(sentence)
                            important_sentence_index_list.append(sentence_split_count)
                    elif no_UI_options == 2:
                        if keyword_list_count == len(specific_keyword_list) - 1:
                            important_sentence_list.append(sentence)
                            important_sentence_index_list.append(sentence_split_count)
                    elif no_UI_options == 1:
                        if keyword_list_count == len(specific_keyword_list) - 2:
                            important_sentence_list.append(sentence)
                            important_sentence_index_list.append(sentence_split_count)
                sentence_split_count = sentence_split_count + 1

            ###UI

            if use_UI == 1:

                high_confidence_sentences = [] #high confidence sentences
                medium_confidence_sentences = [] #high and medium confidence sentences
                low_confidence_sentences = [] #high, medium, and low confidence sentences

                for sentence in high_confidence_sentence_list:
                    high_confidence_sentences.append(sentence)

                for sentence in high_confidence_sentence_list:
                    medium_confidence_sentences.append(sentence)
                for sentence in medium_confidence_sentence_list:
                    medium_confidence_sentences.append(sentence)

                for sentence in high_confidence_sentence_list:
                    low_confidence_sentences.append(sentence)
                for sentence in medium_confidence_sentence_list:
                    low_confidence_sentences.append(sentence)
                for sentence in low_confidence_sentence_list:
                    low_confidence_sentences.append(sentence)

                confidence_switch = 1
                while confidence_switch == 1: #For "Back to Confidence Selection"

                    confidence_switch = 0

                    win_name = 'Grabber Tool User UI' #Creates window for UI
                    win = GraphWin(win_name, win_width, win_height)

                    UI_title = Text(Point(win_width / 2, win_height * 5 / 120), 'Grabber Tool - User UI') #Title of UI
                    UI_title.setStyle('bold')
                    UI_title.draw(win)

                    UI_subject_name = Text(Point(win_width / 12, win_height * 5 / 120), 'Subject: ' + subject) #Subject name
                    UI_subject_name.setStyle('bold')
                    UI_subject_name.draw(win)

                    confidence_question = Text(Point(win_width / 2, win_height * 15 / 120), #Choosing confidence level
                                               'Choose a minimum confidence level:')
                    confidence_question.draw(win)

                    confidence_option_1 = Text(Point(win_width / 2, win_height * 35 / 120), 'High Confidence') #High Confidence + box
                    confidence_option_1.draw(win)
                    confidence_option_1_box = Rectangle(Point(win_width / 4, win_height * 30 / 120),
                                                        Point(win_width * 3 / 4, win_height * 40 / 120))
                    confidence_option_1_box.draw(win)

                    confidence_option_2 = Text(Point(win_width / 2, win_height * 65 / 120), 'Medium Confidence') #Medium Confidence + box
                    confidence_option_2.draw(win)
                    confidence_option_2_box = Rectangle(Point(win_width / 4, win_height * 60 / 120),
                                                        Point(win_width * 3 / 4, win_height * 70 / 120))
                    confidence_option_2_box.draw(win)

                    confidence_option_3 = Text(Point(win_width / 2, win_height * 95 / 120), 'Low Confidence') #Low Confidence + box
                    confidence_option_3.draw(win)
                    confidence_option_3_box = Rectangle(Point(win_width / 4, win_height * 90 / 120),
                                                        Point(win_width * 3 / 4, win_height * 100 / 120))
                    confidence_option_3_box.draw(win)

                    confidence_choice = 'None' #When no choice is selected
                    confidence_none_message = Text(Point(win_width * 3 / 4, win_height * 100 / 120),
                                                   'No choice selected. Please try again.')

                    sentences_list = []
                    while confidence_choice == 'None':

                        confidence_none_message.undraw()

                        confidence_choice_click = win.getMouse()

                        #If High Confidence box is selected: Chooses "High", fills box with Green
                        if confidence_choice_click.getX() > win_width / 4 and confidence_choice_click.getX() < win_width * 3 / 4 \
                                and confidence_choice_click.getY() > win_height * 30 / 120 and confidence_choice_click.getY() < win_height * 40 / 120:
                            confidence_choice = 'High'
                            confidence_option_1_box.setFill('Green')
                            confidence_option_1.undraw()
                            confidence_option_1 = Text(Point(win_width / 2, win_height * 35 / 120),
                                                       'High Confidence - Selected')
                            confidence_option_1.draw(win)
                            sentences_list = high_confidence_sentences
                            time.sleep(1)

                        #If Medium Confidence box is selected: Chooses "Medium", fills box with Green
                        elif confidence_choice_click.getX() > win_width / 4 and confidence_choice_click.getX() < win_width * 3 / 4 \
                                and confidence_choice_click.getY() > win_height * 60 / 120 and confidence_choice_click.getY() < win_height * 70 / 120:
                            confidence_choice = 'Medium'
                            confidence_option_2_box.setFill('Green')
                            confidence_option_2.undraw()
                            confidence_option_2 = Text(Point(win_width / 2, win_height * 65 / 120),
                                                       'Medium Confidence - Selected')
                            confidence_option_2.draw(win)
                            sentences_list = medium_confidence_sentences
                            time.sleep(1)

                        #If Low Confidence box is selected: Chooses "Low", fills box with Green
                        elif confidence_choice_click.getX() > win_width / 4 and confidence_choice_click.getX() < win_width * 3 / 4 \
                                and confidence_choice_click.getY() > win_height * 90 / 120 and confidence_choice_click.getY() < win_height * 100 / 120:
                            confidence_choice = 'Low'
                            confidence_option_3_box.setFill('Green')
                            confidence_option_3.undraw()
                            confidence_option_3 = Text(Point(win_width / 2, win_height * 95 / 120), 'Low Confidence - Selected')
                            confidence_option_3.draw(win)
                            sentences_list = low_confidence_sentences
                            time.sleep(1)

                        #If no confidence is selected
                        else:
                            confidence_none_message.draw(win)
                            time.sleep(1)

                    #Undraw all confidence options and boxes
                    confidence_question.undraw()
                    confidence_option_1_box.undraw()
                    confidence_option_2_box.undraw()
                    confidence_option_3_box.undraw()
                    confidence_option_1.undraw()
                    confidence_option_2.undraw()
                    confidence_option_3.undraw()
                    confidence_none_message.undraw()

                    sentence_title = Text(Point(win_width / 2, win_height * 10 / 120), #Sets title for sentence selection
                                          'Confidence level chosen: ' + confidence_choice.upper())
                    sentence_title.setStyle('bold')
                    sentence_title.draw(win)

                    sentence_option_no = Text(Point(win_width / 3, win_height * 65 / 120), 'No') #"No" selection + box
                    sentence_option_no_box = Rectangle(Point(win_width * 2 / 9, win_height * 60 / 120),
                                                       Point(win_width * 4 / 9, win_height * 70 / 120))

                    sentence_option_yes = Text(Point(win_width * 2 / 3, win_height * 65 / 120), 'Yes') #"Yes" sleection + box
                    sentence_option_yes_box = Rectangle(Point(win_width * 5 / 9, win_height * 60 / 120),
                                                        Point(win_width * 7 / 9, win_height * 70 / 120))

                    sentence_done = Text(Point(win_width / 4, win_height * 110 / 120), 'All sentences chosen?') #"Done" selection + box
                    sentence_done_box = Rectangle(Point(win_width / 8, win_height * 105 / 120),
                                                  Point(win_width * 3 / 8, win_height * 115 / 120))
                    sentence_done_box.draw(win)
                    sentence_done_box.setFill('White')
                    sentence_done.draw(win)

                    sentence_back = Text(Point(win_width *3 / 4, win_height * 110 / 120), 'Back to confidence selection.') #"Back" selection + box
                    sentence_back_box = Rectangle(Point(win_width * 5 / 8, win_height * 105 / 120),
                                                  Point(win_width * 7 / 8, win_height * 115 / 120))
                    sentence_back_box.draw(win)
                    sentence_back_box.setFill('White')
                    sentence_back.draw(win)

                    sentence_none_message = Text(Point(win_width * 3 / 4, win_height * 100 / 120), #If no choice is selected
                                                 'No choice selected. Please try again.')

                    sentence_chosen_message = Text(Point(win_width / 2, win_height * 30 / 120), 'Sentence chosen.') #If a sentence is selected
                    sentence_chosen_message.setStyle('italic')

                    sentence_confidence = Text(Point(win_width / 2, win_height * 25 / 120), 'Sentence confidence: ')

                    sentence_question = Text(Point(win_width / 2, win_height * 20 / 120),'Is this a correct sentence?')

                    important_sentences = []
                    isFinished = False #If program still needs to run or not
                    sentence_choice_count = 0

                    if sentences_list == []:

                        sentence_error_message = Text(Point(win_width / 2, win_height * 40 / 120), 'No sentences found.') #If no sentences are found
                        sentence_error_message.setSize(15)
                        sentence_error_message.draw(win)

                        sentence_choice = 'None'
                        while sentence_choice == 'None':

                            sentence_choice_click = win.getMouse()

                            if sentence_choice_click.getX() > win_width / 8 and sentence_choice_click.getX() < win_width * 3 / 8 \
                                    and sentence_choice_click.getY() > win_height * 105 / 120 \
                                    and sentence_choice_click.getY() < win_height * 115 / 120:
                                sentence_done.undraw()
                                sentence_done = Text(Point(win_width / 4, win_height * 110 / 120),
                                                     'All sentences chosen? - Selected')
                                sentence_done.draw(win)
                                sentence_choice = 'Done'
                                time.sleep(1)
                                break

                            elif sentence_choice_click.getX() > win_width * 5 / 8 and sentence_choice_click.getX() < win_width * 7 / 8 \
                                    and sentence_choice_click.getY() > win_height * 105 / 120 \
                                    and sentence_choice_click.getY() < win_height * 115 / 120:
                                sentence_back.undraw()
                                sentence_back = Text(Point(win_width * 3 / 4, win_height * 110 / 120),
                                                     'Back to Confidence Selection - Selected')
                                sentence_back.draw(win)
                                confidence_switch = 1
                                time.sleep(1)
                                break

                            else:
                                pass

                    else:

                        for sentence in sentences_list:
                            if isFinished == False:

                                sentences_list_length = len(sentences_list)
                                sentence_choice_count = sentence_choice_count + 1

                                sentence_question.undraw()
                                sentence_question = Text(Point(win_width / 2, win_height * 20 / 120),
                                                         'Is this a correct sentence?' + ' (' + str(
                                                             sentence_choice_count) + ' of ' + str(sentences_list_length) + ')')
                                sentence_question.draw(win)

                                sentence_message = Text(Point(win_width / 2, win_height * 40 / 120), sentence[0])
                                sentence_message.setSize(10)
                                sentence_message.draw(win)

                                sentence_confidence.undraw()
                                sentence_confidence = Text(Point(win_width / 2, win_height * 25 / 120),
                                                           'Sentence confidence: ' + sentence[1])
                                sentence_confidence.draw(win)

                                sentence_choice = 'None'
                                while sentence_choice == 'None':

                                    sentence_choice = 'None'

                                    sentence_option_no_box.undraw()
                                    sentence_option_no_box.draw(win)
                                    sentence_option_no_box.setFill('')
                                    sentence_option_no.undraw()
                                    sentence_option_no.draw(win)
                                    sentence_option_yes_box.undraw()
                                    sentence_option_yes_box.draw(win)
                                    sentence_option_yes_box.setFill('')
                                    sentence_option_yes.undraw()
                                    sentence_option_yes.draw(win)
                                    sentence_none_message.undraw()

                                    sentence_choice_click = win.getMouse()

                                    if sentence_choice_click.getX() > win_width * 2 / 9 and sentence_choice_click.getX() < win_width * 4 / 9 \
                                            and sentence_choice_click.getY() > win_height * 60 / 120 \
                                            and sentence_choice_click.getY() < win_height * 70 / 120:
                                        sentence_choice = 'No'
                                        sentence_option_no_box.setFill('Red')
                                        sentence_option_no.undraw()
                                        sentence_option_no.draw(win)
                                        time.sleep(1)

                                    elif sentence_choice_click.getX() > win_width * 5 / 9 and sentence_choice_click.getX() < win_width * 7 / 9 \
                                            and sentence_choice_click.getY() > win_height * 60 / 120 \
                                            and sentence_choice_click.getY() < win_height * 70 / 120:
                                        sentence_choice = 'Yes'
                                        sentence_option_yes_box.setFill('Green')
                                        sentence_option_yes.undraw()
                                        sentence_option_yes.draw(win)
                                        important_sentences.append(sentence)
                                        sentence_chosen_message.draw(win)
                                        time.sleep(1)
                                        sentence_chosen_message.undraw()

                                    elif sentence_choice_click.getX() > win_width / 8 and sentence_choice_click.getX() < win_width * 3 / 8 \
                                            and sentence_choice_click.getY() > win_height * 105 / 120 \
                                            and sentence_choice_click.getY() < win_height * 115 / 120:
                                        sentence_done.undraw()
                                        sentence_done = Text(Point(win_width / 4, win_height * 110 / 120),
                                                             'All sentences chosen? - Selected')
                                        sentence_done.draw(win)
                                        isFinished = True
                                        time.sleep(1)
                                        break

                                    elif sentence_choice_click.getX() > win_width * 5 / 8 and sentence_choice_click.getX() < win_width * 7 / 8 \
                                            and sentence_choice_click.getY() > win_height * 105 / 120 \
                                            and sentence_choice_click.getY() < win_height * 115 / 120:
                                        sentence_back.undraw()
                                        sentence_back = Text(Point(win_width * 3 / 4, win_height * 110 / 120),
                                                             'Back to Confidence Selection - Selected')
                                        sentence_back.draw(win)
                                        confidence_switch = 1
                                        time.sleep(1)
                                        isFinished = True
                                        break

                                    else:
                                        sentence_none_message.draw(win)
                                        time.sleep(1)

                                sentence_message.undraw()
                            else:
                                break

                    win.close()

                    important_sentence_list = []
                    important_sentence_index_list = []
                    for sentence in important_sentences:
                        important_sentence_list.append(sentence[0])
                        important_sentence_index_list.append(sentence[2])

            else:
                pass

            ###Bank
            important_sentences_for_bank_list = [] #Searches around important sentences for more important sentences
            for index in important_sentence_index_list:
                if index - important_sentence_search_range > 0 \
                        and index + important_sentence_search_range < len(html_data_sentence_split):
                    important_sentences_for_bank_list.append(html_data_sentence_split[index])
                    important_sentences_for_bank_list.append(html_data_sentence_split \
                                                             [index - important_sentence_search_range])
                    important_sentences_for_bank_list.append(html_data_sentence_split \
                                                                 [index + important_sentence_search_range])
                    important_sentences_for_bank_list.append(html_data_sentence_split[index])
                else:
                    pass

            important_sentences_for_bank_list_new = [] #Processes important sentences further
            for sentence in important_sentences_for_bank_list:
                if sentence not in important_sentences_for_bank_list_new:
                    sentence = sentence.replace(',','-')
                    sentence = sentence.replace('\n',' - ')
                    important_sentences_for_bank_list_new.append(sentence)
            important_sentences_for_bank_list = important_sentences_for_bank_list_new
            print(important_sentences_for_bank_list)

            bank_search_list = []
            for sentence in important_sentences_for_bank_list: #Searches all important sentences for keywords
                for keyword in bank_keyword_list:
                    if sentence.lower().find(keyword.lower()) > -1:
                        bank_search_list.append(keyword)

            #Replaces some keyword in bank_keyword_list with others if trigger word is set off
            for keyword in bank_search_list:
                for replace_list in bank_keyword_replace_list:
                    original_word = replace_list[0]
                    trigger_words = replace_list[1:len(replace_list)-1]
                    replace_word = replace_list[-1]
                    if keyword == original_word:
                        for trigger_word in trigger_words:
                            if trigger_word == '':
                                bank_search_list = replace_element_in_list(bank_search_list,original_word,replace_word)
                            else:
                                for sentence in important_sentences_for_bank_list:
                                    if sentence.lower().find(trigger_word) > -1:
                                        bank_search_list = replace_element_in_list(bank_search_list, original_word,
                                                                                   replace_word)

            bank_search_list_new = []
            for keyword in bank_search_list: #Replaces duplicates in bank_search_list
                if keyword not in bank_search_list_new and keyword != '':
                    bank_search_list_new.append(keyword)
            bank_search_list = bank_search_list_new
            print(bank_search_list)

            #Print all information into .csv via flat_file_data_temp
            flat_file_data_temp = []
            flat_file_data_temp.append(subject_count)
            flat_file_data_temp.append(subject)
            flat_file_data_temp.append(subject_wiki_url)
            for important_paragraph in important_paragraphs_max_list:
                flat_file_data_temp.append(important_paragraph)
            flat_file_data_temp.append(convert_list_to_string(important_sentences_for_bank_list))
            flat_file_data_temp.append(convert_list_to_string(bank_search_list))
            flat_file_data_temp.append(convert_list_to_string(subjects_education))
            print(flat_file_data_temp)

            # Print all information into .txt
            txt_data_temp = ''
            txt_data_temp += 'Entrepreneur ' + str(subject_count) + ': ' + subject + '\n'
            txt_data_temp += 'Wikipedia URL: ' + subject_wiki_url + '\n'
            important_paragraph_count = 0
            for important_paragraph in important_paragraphs_max_list:
                important_paragraph_count = important_paragraph_count + 1
                txt_data_temp += 'Paragraph ' + str(important_paragraph_count) + ': ' + important_paragraph + '\n'
            txt_data_temp += 'Important Sentences: ' + convert_list_to_string(important_sentences_for_bank_list) + '\n'
            txt_data_temp += 'Information: ' + convert_list_to_string(bank_search_list) + '\n'
            txt_data_temp += 'Education: ' + convert_list_to_string(subjects_education) + '\n'
            txt_data_temp += '\n'

            if toggle_write_txt == 1: #Writes txt_data_temp into .txt file
                if subject_count == 1:
                    write_txt(current_dir, txt_data_temp, txt_name, 0)
                else:
                    write_txt(current_dir, txt_data_temp, txt_name, 1)
            else:
                pass

            if toggle_write_csv == 1: #Writes flat_file_data_temp into .csv file
                write_csv(flat_file_data_temp,csv_name,'',1) #Writes flat_file_data_temp into .csv file
            else:
                pass

        except urllib.error.HTTPError: #Catches HTTPError
            print('HTTPError occured.')
            httperror_cooldown_count = httperror_cooldown_count + 1
            time.sleep(600 + httperror_cooldown_count*60)
else:
    print('Scrape type not recognized.') #If no scrape type is recognized