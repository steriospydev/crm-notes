
navbar 
## FRONTEND

### Pages
- User main dashboard.html (widgets and tables)
- User main
- Contact Pages
## BACKEND
- User Profile 

- create 100 users x 100 contacts/user x 40 notes/per contact using Fake and commands/
### Authentication

### User
- User Info
- Preferences(subject)

- Dashboard Pages

### Note
- make subject separate model Subject


### Alarm
- IMPLEMENT: ALARM SYSTEM USER

# COMPLETED
- Fix UI/UX login page DONE
- Fix footer DONE
- Make subject choice DONE
- FIlter data DONE
- Search data DONE 
- Add note identifier DONE
- Add NoteManager for filtering and search DONE
- Create ContactForm (2F) Done
- remove "Ολοκληρωθηκε" from note.status(2F) DONE
- Add create client form in modal(4B), (6B) DONE
## Dummy Data 



## Database
psql --version
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl status postgresql
sudo -u postgres psql

CREATE USER myuser WITH PASSWORD 'mypassword';
CREATE DATABASE mydb OWNER myuser;
ALTER ROLE noteAdmin SET client_encoding TO 'utf8';
ALTER ROLE noteAdmin SET default_transaction_isolation TO 'read committed';
ALTER ROLE noteAdmin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;


# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
