from celery import Celery
from mail1 import send_mail
#app=Celery('tasks',broker='sqs://AKIAQQEMGEPYSZONMRGL:kLoSU06GVetJffPBXuZGnBeaIVfteT1Xny/frgDu@')
app=Celery('tasks')
app.config_from_object('celeryconfig')

@app.task
def mail(recipient):
    send_mail(recipient)
    return("mail sent")