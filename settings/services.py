from settings.models import Currency


def create_currency(code, desc, cost):
    return Currency.objects.create(
        code=code,
        desc=desc,
        cost=cost
    )


def update_currency(initial_currency, code, desc, cost):
    return Currency.objects.filter(id=initial_currency.id).update(
        code=code,
        desc=desc,
        cost=cost
    )
