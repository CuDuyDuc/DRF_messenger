
# How to set up project

Requires:

    Using Virtualenv or Python environment, etc.






## The way to run project

- Step1: pip install django djangorestframework-simplejwt

- Step2: pip install -U drf-yasg
- Step3: pip install channels-redis==2.4.2 channels==3.0.3
- Step4: pip install websockets wsproto
- Step5: pip install psycopg2
- Step6: python manage.py makemigrations
- Step7: python manage.py migrate
- Step8: python manage.py collectstatic --noinput
- Step9: pip install uvicorn 'uvicorn[standard]'
- Step10: uvicorn message_be.asgi:application --port 8080 --host 0.0.0.0 --reload
- Visit website: Go to visit on the website api local: http://127.0.0.1:8080/docs

