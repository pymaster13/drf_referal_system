# Django Rest Framework Referal System

This project have realized as test task (2022). 

## Getting Started
Python version: 3.9.10

Clone project:
```
git clone https://github.com/pymaster13/drf_referal_system.git && cd drf_referal_system
```

Create and activate virtual environment:
```
python3 -m venv venv && source venv/bin/activate
```

Install libraries:
```
python3 -m pip install -r requirements.txt
```

Migrations:
```
cd referal_system && python3 manage.py makemigrations person && python3 manage.py migrate
```

Run:
```
python3 manage.py runserver
```

Functional:
- Authorization by phone number.
Step 1 - Enter your phone number. Simulate sending a 4-digit authorization code (delay
on the server 1-2 seconds).
Step 2 - to enter the code. If the user has not previously authorized, then record it in the database.
- Request for a user profile.
- The user needs to be assigned a randomly generated 6-digit invite code (numbers and symbols) at the first authorization.
- In the profile, the user should be able to enter someone else's invite code (when entering, check for existence). In your profile, you can activate only 1 invite code, if the user has already activated the invite code, then you need to display it in the appropriate field in the request for the user profile.
- The profile API should display a list of users (phone numbers) who entered the invite code of the current user.


URLs:
- get_code/ - first authorization step is entering phone number to get code by sms;
- authorize/ - second step is entering accepted sms-code and getting authorization jwt tokens;
- profile/ - get information about user (phone, invite_code, invited users, activated foreign invite code) (only for authorized users);
- implement_invite/ - try to realize foreign invite code (only for authorized users);
- admin/ - get admin page;
- schema/ - get file 'schema.yaml';
- doc/ - get project documentation with all endpoints.


Pythonanywhere: http://pymaster13.pythonanywhere.com/ (user database is SQLite because PGSQL is only allowed in paid account).
