from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Define the start and end dates
# start_date = 
# end_date = 

# Generate a date between the start and end dates

faker_date = fake.date_time_between(start_date='-100y', end_date='-19y')
# startdate = fake.date_between(start_date='today', end_date='+3d')
# enddate = fake.date_between(start_date='+3y', end_date='+30y')

print(faker_date)
