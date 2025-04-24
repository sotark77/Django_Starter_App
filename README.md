#-----STEPS TO USE THE APPLICATION------

1. Install Python (Obviously)

2. Clone the repository

3. Cteare a virtual environment (Windows: py -m venv .venv)

4. Activate the virtual environment (Windows: .venv\Scripts\activate) Upgrade pip if needed (Windows: python -m pip install --upgrade pip)

5. Install the requirements in the requirements.txt file (Windows: pip install -r requirements.txt)

6. Make migrations

7. Migrate

8. Create a superuser

9. Run the server

10. Done. Feel customize application to your needs and liking.


#------Information------------

1. Among many others thing, the main focal point in this starter app is that it contains a custom user model which uses the email address of the user as the username, email address can be used to login on the admin panel and using the front-end HTML template. The app does have a user_name field, but it is not mandatory and I decided to include it, in case users don't want to display their real name or email address.

2. For the data ID (PK) it uses a UUIDFIELD

3. It contains a custom auth views: Login & registration. The registration view, send automatic email verifications to user when they register and accounts are not set to "is_active" until the email is verified. All views have error handling, so its easy to see what error(s) are blocking.




Please note. I'm far far far very far from calling myself a proficient/efficient developer. So, I’m sure you will find mistakes or a better way of performing some of the tasks carried out, better code structuring, etc. So please be easy on me.

Hope you enjoy!!!!!

Sotark77
