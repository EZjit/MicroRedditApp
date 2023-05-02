 MicroRedditApp
Blog app with reduced reddit-like functionality

This project:
1) Built on django
2) Has an API created with DRF
3) Tested with pytest
4) Dockerized
5) Seed available


Installation (docker):
1) Make sure you have docker and docker compose packages installed
2) Download source code of this repo
3) cd to project directory
4) $ docker compose up
5) $ docker compose exec web python manage.py migrate
6) (optional) $ docker compose exec web python manage.py createsuperuser
7) (optional) $ docker compose exec web python manage.py seed

This command seeding database with some test data. Don't worry if command is running for a long time.
Seeding database will take a few minutes. Most of the time command will dynamically create 11000 comments.
If you don't want to wait, you can change {number} values inside micro_reddit/core/management/commands/seed.py {run_seed} function.

8) Go to localhost:8000 and feel free to play around! :)
