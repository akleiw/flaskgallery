# Flaskgallery
Public facing gallery for albums stored on Google Photos


## Set up
Log in via gphotospy, put photoslibrary_v1.token and gphotos.json in app folder
```bash
flask db upgrade
#create user "username" with password "password" and role admin
flask create-user username password admin
#create role "family"
flask create-role family
flask create-user mom momspass family
```
