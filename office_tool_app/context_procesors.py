from datetime import datetime


def data(request):
    date = datetime.now()
    return {'date': date}