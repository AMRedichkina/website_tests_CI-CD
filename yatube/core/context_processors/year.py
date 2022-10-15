import datetime


# Добавляет переменную с текущим годом. Для шаблона подвала
def year(request):
    return {
        'year': int(datetime.datetime.now().strftime('%Y')),
    }
