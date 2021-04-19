FROM python:3.9
WORKDIR /bot

COPY requirements.txt /bot/requirements.txt
RUN pip install -r requirements.txt

COPY . /bot
CMD ["python", "PrincessPaperplane/bootstrap.py"]