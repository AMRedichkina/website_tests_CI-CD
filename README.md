# Social Network project

Social network for publishing personal diaries. A site where you can create your page. 
If you go to it, you can see all the posts of the author. 
Users will be able to visit other people's pages, subscribe to authors and comment on their posts. 
The author can choose a name and a unique URL for their page. 
It is possible to moderate entries and block users if they start sending spam. Recordings can be sent to the community and see the records of different authors there.

**Technologies:**
 - _[Python 3.9](https://docs.python.org/3/)_
 - _[Django 2.2.16](https://docs.djangoproject.com/en/2.2/)_
 - _[Pytest 6.2.4](https://docs.pytest.org/en/7.1.x/announce/release-6.2.4.html)_

**To start the project, run the following commands:**
```
git clone <...>
cd <...>
python -m venv env
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
