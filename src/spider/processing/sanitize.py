"""
Module includes functions that are useful for processing the data from the listings
Specifically, check_values aims to identify attributes such as purity, unit type, drug origin, and other specific drug classifications

***Messy and still in development***
"""

import re

from keywords import drug_list, measurement_list, unit_list, percent_list

def check_drug_type(string):
    string = string.lower()
    for drug_type in drug_list:
        for definition in drug_type:
            if definition in string:
                return drug_type[0]
    return "Other"

def isfloat(value): #also will check if it can be an int
    value = value.replace(',', '.') #change 6,0 --> 6.0
    try:
        float(value)
        return True
    except ValueError:
        return False

def isInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def check_value(string, value_list):
    string = string.lower()
    string = re.split(r'[ )[/(\]\+\-]+', string) #split string by spaces, brackets, + --> consider adding "x" --> 100x50mg --> maybe add quantity of order ie *100* pills of mgs to scrapy items
    extracted_values = [(None, None)]
    number_list = [] #individual numbers collected

    for word in string:
        word = word.strip(',.;:!*)([]""''')
        for items in value_list:
            for value in items:
                if value == word[-len(value):]: #if last part of the word is a measurement --> "25.6mg" or "mg"
                    if isfloat(word[:-len(value)]): #when 25.6mg
                        extracted_values.append((word[:-len(value)].replace(',','.'), items[0]))

                    elif isfloat(string[string.index(word)-1]): #when 25.6 mg --> get previous value in sentence
                        extracted_values.append((string[string.index(word)-1].replace(',','.'), items[0]))

                    elif string[string.index(word)-1] == 'half': #half an oz
                        extracted_values.append((0.5, items[0]))

                    elif string[string.index(word)-1] == 'quarter':
                        extracted_values.append((0.25, items[0]))

    # pass in 'x' as value, tabs, bars, pills, --> "5677 pills of MDMA"
        if value == 'x':
            done = False
            if isInt(word):
                try:
                    for key_word in unit_list:
                        if string[string.index(word)+1] == key_word:
                            extracted_values.append((int(word), 'x'))
                        else:

                            #TODO: make this better
                            for measurements in measurement_list:
                                if string[string.index(word)+1] in measurements:
                                    done = True
                                    break

                            if string[string.index(word)+1] in percent_list or done == False:
                                extracted_values.append((int(word), 'x'))
                except:
                    pass
            
            #x10
            if word[0] == 'x':
                if isInt(word[1:]):
                    extracted_values.append((int(word[1:]), 'x')) #if word starts with x, check if rest of word is an int, return that value

            if isInt(word):
                number_list.append(int(word))

    #get only unique extractions in list
    extracted_values = list(dict.fromkeys(extracted_values))
    if len(extracted_values)==2: #only one extracted value, return that value
        return extracted_values[1]

    #return single number if quantity is requested and no other options exist
    elif len(number_list)==1 and len(extracted_values)==1 and value_list == [['x']]:
        return (number_list[0], 'x')
    
    print("Unable to extract info from: ")
    print(string)
    print(extracted_values)
    print()
    return extracted_values[0] #no extracted values or too many, return None
