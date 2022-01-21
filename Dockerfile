FROM python:3
ADD . /code
WORKDIR /code
RUN pip install redis datetime pymongo requests beautifulsoup4
CMD [ "python", "./scrapper_assignment.py" ]