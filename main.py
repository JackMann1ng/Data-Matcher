# works for an even amount of students
# 4/1/2018 9:00:26,rcvelasco01@junk.com,Nike,Sports,Whatever I Can Find,Football,Gucci,Casual,Funny,Comedy,Dick's Sporting Goods,Hydroflask,Angevine,Engineering,Other,Barack/Michelle,Kim,hey I could've dropped my croissant,Brownies,Movies,Instagram,Black Coffee,LA,Humor,Indie / Folk,Hash Browns,Beach/Island,Face Swap,A,Summer,Boba,Chance,12th,,,,
#break up by grade level first

import csv
import json
import pandas as pd
import itertools

data = ('/Users/jackmanning/Downloads/DATA MATCH FORM (Responses) - Form Responses 1.csv')
csv_file = pd.read_csv(data)
# data cleaning stuff
emails = pd.read_csv(data,  usecols=['Email Address'])
emails = emails.values.tolist()
email_list = []
for i in emails:
    for l in i:
        email_list.append(l)

data_titles = csv_file.columns[2:-4]
data_points = pd.read_csv(data,  usecols=data_titles)
data_points = data_points.values.tolist()

data_dict = {

}
# gets dictionary with email as key and responses as value
for email in email_list:
    
    data_dict[email] = {'responses':data_points[email_list.index(email)], 'matches':None, 'email':email}

# empty list and dict to be used later
freshmen = {}
sophmores = {}
juniors = {}
senior = {}

for em in data_dict:
    dat = data_dict.get(em)
    resp = dat.get('responses')
    if resp[2] == 9:
        freshmen[em] = dat
    if resp[2] == 10:
        sophmores[em] = dat
    if resp[2] == 11:
        juniors[em] = dat
    if resp[2] == 12:
        senior[em] = dat



matches = {}
used = []
print(len(sophmores))
# get's match for each student
def get_matches(grade):
    for email in grade:
        if email not in used:
            c_match = {
                'leader': None,
                'score': 0
            }
            g = data_dict.get(email)
            e_responses = g.get('responses')[2:]
            # gets every other students responses and grade
            for student in grade:
                if student not in used:
                    score = 0
                    z = data_dict.get(student)
                    s_responses = z.get('responses')[2:]
                        #for response in s_responses:
                    for a_r, b_r in zip(e_responses, s_responses):
                        if a_r == b_r and student != email:
                            score += 1
                        if score > c_match.get('score'):
                            c_match['leader'] = student
                            c_match['score'] = score
                # check if student is the last in list, if it is then scrap not in used clasue and give it two partners
                x = [i for i in grade]
                test = x.index(student)
                
                
                if len(grade) == test and len(grade)%2==0:
                    
                    score = 0
                    z = data_dict.get(student)
                    s_responses = z.get('responses')[2:]
                        #for response in s_responses:
                    for a_r, b_r in zip(e_responses, s_responses):
                        if a_r == b_r and student != email:
                            score += 1
                        if score > c_match.get('score'):
                            score = 0
                            c_match['leader'] = student
                            c_match['score'] = score
                
                        
            if c_match.get('leader') in used:
                x = matches.get(c_match.get('leader'))
                matches[email] = [c_match.get('leader'), x]
                matches[c_match.get('leader')] = [email, x]
                matches[str(x)] = [email, c_match.get('leader')]
                used.append(email)
                
            else:
                
                matches[email] = c_match.get('leader')
                matches[c_match.get('leader')] = email

                used.append(c_match.get('leader'))
    
    return matches


get_matches(juniors)

get_matches(freshmen)

df = pd.DataFrame.from_dict(matches, orient='index')

df.to_csv('/Users/jackmanning/Documents/Student Valentine Match /match.csv', index = True)
