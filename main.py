import csv
import pandas as pd
import itertools
# data must be csv
data = ('/path/to/data')
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

data_dict = {}
# gets dictionary with email as key and responses as value
for email in email_list:
    
    data_dict[email] = {'responses':data_points[email_list.index(email)], 'matches':None}

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
# to make sure people don't get multiple matches
used = []
used_2 = []

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
                        if a_r == b_r and student != email and student not in used:
                            score += 1
                        if score > c_match.get('score'):
                            c_match['leader'] = student
                            c_match['score'] = score
                
                x = [i for i in grade]
                last_student = x.index(student)
                
                # if last student of grade level is in an uneven 
                if (len(grade) - 1) == last_student and len(grade)%2!=0:
                
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
                
                
                   
            if c_match.get('leader') in used and c_match.get('leader') not in used_2:
                x = matches.get(c_match.get('leader'))
                matches[email] = [c_match.get('leader'), x]
                matches[c_match.get('leader')] = [email, x]
                matches[str(x)] = [email, c_match.get('leader')]
                used.append(email)
                used_2.append(c_match.get('leader'))
                used_2.append(x)

                
            if c_match.get('leader') not in used:
                y = c_match.get('leader')
                matches[email] = y
                matches[y] = email

                used.append(c_match.get('leader'))
                used.append(email)

#gets match for each class
get_matches(freshmen)
get_matches(sophmores)
get_matches(juniors)
get_matches(senior)

df = pd.DataFrame.from_dict(matches, orient='index')


df.to_csv('path/to/file/for/matches', index = True)

