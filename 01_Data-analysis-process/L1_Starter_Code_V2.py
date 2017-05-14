## Load data from csvs
import unicodecsv

## Longer version of code (replaced with shorter, equivalent version below)

# enrollments = []
# f = open('enrollments.csv', 'rb')
# reader = unicodecsv.DictReader(f)
# for row in reader:
#     enrollments.append(row)
# f.close()

with open('enrollments.csv', 'rb') as f:
    reader = unicodecsv.DictReader(f)
    enrollments = list(reader)



#####################################
#                 1                 #
#####################################

## Read in the data from daily_engagement.csv and project_submissions.csv 
## and store the results in the below variables.
## Then look at the first row of each table.

with open('daily_engagement.csv', 'rb') as f:
    reader = unicodecsv.DictReader(f)
    daily_engagement = list(reader)
with open('project_submissions.csv', 'rb') as f:
    reader = unicodecsv.DictReader(f)
    project_submissions = list(reader)
print(daily_engagement[0])
print(project_submissions[0])

## Alternative
def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)
daily_engagement = read_csv('daily_engagement.csv')
project_submissions = read_csv('project_submissions.csv')


## Fixing data types
from datetime import datetime as dt

# Takes a date as a string, and returns a Python datetime object. 
# If there is no date given, returns None
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')
    
# Takes a string which is either an empty string or represents an integer,
# and returns an int or None.
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

# Clean up the data types in the enrollments table
for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])
    
enrollments[0]


# Clean up the data types in the engagement table
for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])
    
daily_engagement[0]


# Clean up the data types in the submissions table
for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

project_submissions[0]


## Investigating the data
#####################################
#                 3                 #
#####################################

## Rename the "acct" column in the daily_engagement table to "account_key".
for engagement in daily_engagement:
    engagement['account_key'] = engagement['acct']
    del engagement['acct']
print(daily_engagement[0]['account_key'])


#####################################
#                 2                 #
#####################################

## Find the total number of rows and the number of unique students (account keys)
## in each table.
def unique_values(table, value):
    unique_values = set()
    for row in table:
        unique_values.add(row[value])
    return unique_values

enrollment_num_rows = len(enrollments)
enrollment_num_unique_students = len(unique_values(enrollments, 'account_key'))
print(enrollment_num_rows)
print(enrollment_num_unique_students)

engagement_num_rows = len(daily_engagement)
engagement_num_unique_students = len(unique_values(daily_engagement, 'account_key'))
print(engagement_num_rows)
print(engagement_num_unique_students)

submission_num_rows = len(project_submissions)
submission_num_unique_students = len(unique_values(project_submissions, 'account_key'))
print(submission_num_rows)
print(submission_num_unique_students)


## Problems in the data

## Missing engagement records
#####################################
#                 4                 #
#####################################

## Find any one student enrollments where the student is missing from the daily engagement table.
## Output that enrollment.
i = 0
missings = set()
while i < enrollment_num_rows:
    if enrollments[i]['account_key'] not in unique_values(daily_engagement, 'account_key'):
       #missings.add(enrollments[i]['account_key'])
        missings.add(i)
    i += 1
print(missings)

#### print(list(missings)[:5])
for i in range(len(missings)):
    print(enrollments[i])
    


## Checking for more problem records
#####################################
#                 5                 #
#####################################

## Find the number of surprising data points (enrollments missing from
## the engagement table) that remain, if any.
missing_but_remains = set()
for i in list(missings):
    if enrollments[i]['days_to_cancel'] >= 1 or enrollments[i]['days_to_cancel'] == None:
        missing_but_remains.add(i)
print missing_but_remains
print(len(missing_but_remains))

for i in list(missing_but_remains):
    print(enrollments[i])
    
    
## Trackin down the remaining problems
# Create a set of the account keys for all Udacity test accounts
udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_accounts.add(enrollment['account_key'])
len(udacity_test_accounts)

# Given some data with an account_key field, removes any records corresponding to Udacity test accounts
def remove_udacity_accounts(data):
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data

# Remove Udacity test accounts from all three tables
non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)

print len(non_udacity_enrollments)
print len(non_udacity_engagement)
print len(non_udacity_submissions)


## Refining the question
#####################################
#                 6                 #
#####################################

## Create a dictionary named paid_students containing all students who either
## haven't canceled yet or who remained enrolled for more than 7 days. The keys
## should be account keys, and the values should be the date the student enrolled.

paid_students = {}
for enrollment in non_udacity_enrollments:
    if enrollment['days_to_cancel'] == None or enrollment['days_to_cancel'] > 7:
        account_key = enrollment['account_key']
        enrollment_date = enrollment['join_date']
        #temp = {'account_key': enrollment['account_key'], 'enrollment_date': enrollment['join_date']}
        #paid_students.append(temp)
        if account_key not in paid_students or enrollment_date > paid_students[account_key]:
            paid_students[account_key] = enrollment_date
            
print paid_students
#print len(unique_values(paid_students, 'account_key'))
print len(paid_students)


## Getting data from first week
# Takes a student's join date and the date of a specific engagement record,
# and returns True if that engagement record happened within one week
# of the student joining.
def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    #return time_delta.days < 7
    return time_delta.days < 7 and time_delta.days >= 0

#####################################
#                 7                 #
#####################################

## Create a list of rows from the engagement table including only rows where
## the student is one of the paid students you just found, and the date is within
## one week of the student's join date.

paid_engagement_in_first_week= []
for engagement in daily_engagement:
    key_temp = engagement['account_key']
    if key_temp in set(paid_students):
        if within_one_week(paid_students[key_temp], engagement['utc_date']):
            #temp = {'account_key': key_temp, 'utc_date': engagement['utc_date']}
            paid_engagement_in_first_week.append(engagement)

#print paid_engagement_in_first_week
print paid_engagement_in_first_week[:5]
print len(paid_engagement_in_first_week)


## Exploring student engagement
from collections import defaultdict

# Create a dictionary of engagement grouped by student.
# The keys are account keys, and the values are lists of engagement records.
engagement_by_account = defaultdict(list)
for engagement_record in paid_engagement_in_first_week:
    account_key = engagement_record['account_key']
    engagement_by_account[account_key].append(engagement_record)
    
#print engagement_by_account

# Create a dictionary with the total minutes each student spent in the classroom during the first week.
# The keys are account keys, and the values are numbers (total minutes)
total_minutes_by_account = {}
for account_key, engagement_for_student in engagement_by_account.items():
    total_minutes = 0
    for engagement_record in engagement_for_student:
        total_minutes += engagement_record['total_minutes_visited']
    total_minutes_by_account[account_key] = total_minutes
    
import numpy as np

# Summarize the data about minutes spent in the classroom
total_minutes = total_minutes_by_account.values()
print 'Mean:', np.mean(total_minutes)
print 'Standard deviation:', np.std(total_minutes)
print 'Minimum:', np.min(total_minutes)
print 'Maximum:', np.max(total_minutes)

print total_minutes_by_account.values()[:10]


## Debugging data analysis code
#####################################
#                 8                 #
#####################################

## Go through a similar process as before to see if there is a problem.
## Locate at least one surprising piece of data, output it, and take a look at it.
#account_anomalies = []
#for account in set(total_minutes_by_account):
#    if total_minutes_by_account[account] > 10000:
#        account_anomalies.append(account)

#for engagement in daily_engagement:
#    if engagement['account_key'] in account_anomalies:
#        print engagement

## Find student with maximum minutes
student_with_max_minutes = None
max_minutes = 0
for student, total_minutes in total_minutes_by_account.items():
    if total_minutes > max_minutes:
        max_minutes = total_minutes
        student_with_max_minutes = student

print max_minutes

for engagement_record in paid_engagement_in_first_week:
    if engagement_record['account_key'] == student_with_max_minutes:
        print engagement_record
        
        
total_lessons_completed_by_account = {}
for account_key, engagement_for_student in engagement_by_account.items():
    lessons_completed = 0
    for engagement_record in engagement_for_student:
        lessons_completed += engagement_record['lessons_completed']
    total_lessons_completed_by_account[account_key] = lessons_completed

total_lessons_completed = total_lessons_completed_by_account.values()
print 'Mean:', np.mean(total_lessons_completed)
print 'Standard deviation:', np.std(total_lessons_completed)
print 'Minimum:', np.min(total_lessons_completed)
print 'Maximum:', np.max(total_lessons_completed)



## OPTION 1
def sum_grouped_items_v2(grouped_data, field_name):
    summed_data = {}
    for key, data_points in grouped_data.items():
        total = 0
        for data_point in data_points:
            if data_point[field_name] >= 1:
                total += 1
        summed_data[key] = total
    return summed_data

total_num_courses_visited = sum_grouped_items_v2(engagement_by_account, 'num_courses_visited')
print total_num_courses_visited


for account_key, engagement_for_student in engagement_by_account.items():
    for engagement_record in engagement_for_student:
        engagement_record['has_visited'] = 0
        if engagement_record['num_courses_visited'] >= 1:
            engagement_record['has_visited'] = 1
         
def group_data(data, key_name):
    grouped_data = defaultdict(list)
    for data_point in data:
        key = data_point[key_name]
        grouped_data[key].append(data_point)
    return grouped_data

def sum_grouped_items(grouped_data, field_name):
    summed_data = {}
    for key, data_points in grouped_data.items():
        total = 0
        for data_point in data_points:
            total += data_point[field_name]
        summed_data[key] = total
    return summed_data            

submissions_by_account = group_data(non_udacity_submissions, 'account_key')

subway_project_lesson_keys = ['746169184', '3176718735']

passing_engagement = []
for key in engagement_by_account:    
    if key in set(submissions_by_account):
        for submissions in submissions_by_account[str(key)]:
            for i in range(1, len(submissions)):
                print submissions[i]
                
                
                if submission['lesson_key'] in subway_project_lesson_keys:
                    if submission['assigned_rating'] == "PASSED":
                        passing_engagement.append(submission)

non_passing_engagement = []
for key in engagement_by_account:    
    if key in set(submissions_by_account):
        for submission in submissions_by_account[str(key)]:
            if submission['lesson_key'] in subway_project_lesson_keys:
                if submission['assigned_rating'] != "PASSED":
                    non_passing_engagement.append(submission)