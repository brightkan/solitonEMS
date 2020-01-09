from settings.models import Currency


def get_all_currencies():
    return Currency.objects.all()


def get_currency(currency_id):
    return Currency.objects.get(pk=currency_id)
