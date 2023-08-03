### Python Programming 1
### March 25, 2023
### Created By: Esl Kim (Elsie)
### Assignemt Title: Final Programming Assignment - Extension

### Importing Libraries

import requests
from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup


######### Part 1. Asking User to name a short story by path #########


class get_shortstory:

    def __init__(self):
        self.storyname = storyname
        self.path = path
        self.url = url
        self.storycontent = storycontent
        self.vocablist = vocablist

    while True:
        # User Prompt: Name a short story
        storyname = str(input("Please Name a Short Story: "))
        path = str(storyname.lower())
        
        # Website that will working on this assignment
        url = f'http://classicshorts.com/stories/{path}.html'

        try:
            
            # Accessing URL with User's input
            user_response = urlopen(url)
            # Read URL contents
            storycontent = user_response.read()
            # Empty Vocablist
            vocablist = []
            # Parse the HTML content using BeautifulSoup
            user_soup = BeautifulSoup(storycontent, 'html.parser')
            # Grab a content from the story paragraph
            # <div class="StoryPara"> : Every start of story paragraph
            for each_paragraph in user_soup.find_all('div', attrs={'class': "StoryPara"}):
                content = each_paragraph.text
                vocabs = content.lower().split()

                for each_vocab in vocabs:
                    vocablist.append(each_vocab)
                    num_terms = len(vocablist)

            print(f'Story is found. {num_terms} vocabulary terms are in {storyname} Short Story.')
            break

        except HTTPError as e:
            print("Short Story is not found. HTTP Error code:", e.code)
            print("Please Enter a Name of Short Story again.\n")
            pass


######### Part 2. Asking User to Update the Word's Definition #########

# Eliminate Duplicates in the lists
clean_vocablist = get_shortstory.vocablist
digit = '[0-9]'

for i in digit:
    clean_vocablist = [s. replace(i,"") for s in clean_vocablist]
    
special_char = ['',',', '.',':', ';', '"', '@', '#', '$','%', '^', '&', '*', '!', '--',' ',""] # Remove all special characters

for item in special_char:
    clean_vocablist = [s. replace(item,"") for s in clean_vocablist]
    
    if(len(item) == 0):
        clean_vocablist.remove(item)


unique_vocablist = list(set(clean_vocablist))
unique_vocablist.sort()
unique_num_terms = len(unique_vocablist)

print(f'There are {unique_num_terms} unique vocabular words.')

longestwordlength = len(max(unique_vocablist, key = len)) # length of the longest word in a content
space = int(longestwordlength) # change ino integer so later, file format spacing        

update_list = [] # user's update word-definition list

count = 0
# User Prompt for asking updating words and definition
while True:
    try:
        update_word = str(input('\nWould you like to update a definition (Y/N)? '))

        if update_word == 'Y' or update_word == 'y':

            

            term = str(input('Term: ')).lower()

            if term in unique_vocablist:
                
                # Accessing Dictionary.com
                dict_url = f"https://www.dictionary.com/browse/{term}"
                check_url = requests.get(dict_url)

                if check_url.status_code == 200:
                    
                    dict_response = urlopen(dict_url)
                    
                    dict_content = dict_response.read()
                    dict_soup = BeautifulSoup(dict_content, 'html.parser')
                    # <meta name = "description", content=".."> : Definition
                    for lines in dict_soup.find_all("meta", attrs = {"name":"description"}):
                        dict_def = dict_soup.find("meta", attrs = {"name":"description"}).get("content")
                        print(dict_def)

                    print('\nThe term is found in the story.\n')
                    print(f'Current Definition is: {dict_def} in Dictionary.com\n')
                    definition = str(input('Definition: '))
                    
                    
                    
                    update = f'{term:<{space}} : {definition:<}' # Update Vocab - Definition format

                    update_list.append(update) # put separate updated word- definition

                   
                    unique_vocablist.remove(term) # remove duplicate term
                    update_list.sort()
                    unique_vocablist.sort()
                    count +=1
                else:
                    wikipedia_url =f"https://en.wikipedia.org/wiki/{term}"
                    print('Please Search in Wikipedia')
                    pass

                
            else:
                print('ERROR! Term is not found in the story.')
                pass

            
                          
        else:
            print("You decide to Not Update a definition further.")
            print(f'Total {count} Definition is saved! ')
            break
    except:
        break
                          
                
######### Part 3. Asking User to Save the Vocabulary in a file #########
    

filename = input('\nWhat would you like to save the file as? (name.txt) ')

report = open(filename, 'w')

header = f'Term{":":>{space-2}} Definition'
report.write(header)

unique_list = unique_vocablist + update_list
unique_list.sort()

for item in unique_list:

    if item in update_list:
            report.write(f'{item:<{space}}\n')

    elif item == '':
        report.write(f'{item}\n')

    else:   
        report.write(f'{item:<{space}} : \n')


result = ""
with open(filename, "r+") as report:
    for line in report:
        if not line.isspace():
            result += line
    report.seek(0)
    report.write(result)

print('File saved! Please check your file')
report.close()
