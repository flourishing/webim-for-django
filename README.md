# webim-for-django

WebIM for Django

## Run

```
virtualenv venv

source venv/bin/activate

pip install Django

python manage.py runserver
```

## Develop

1. Import 'install.sql' to database

2. Copy 'webim' folder to your project

3. Configure settings and urls of your project to add 'webim.urls'

4. Coding webim/plugin.py to integrate with users of your site

6. Insert javascript to footer of your site:

```
<script src="webim/boot" type="text/javascript"></script>
```

## Author

NexTalk.IM


