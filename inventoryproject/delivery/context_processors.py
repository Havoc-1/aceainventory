from .models import Delivery

def delivery(request):
    return {'delivery': Delivery(request)}          # makes the delivery class global (also under context processor of settings / EXPERIMENTAL)