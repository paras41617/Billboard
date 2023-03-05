from .models import Bid


def get_max():
    bids = Bid.objects.all()
    if len(bids) == 0:
        return None, 0
    else:
        message = ""
        max_price = 0
        for bid in bids:
            if bid.price > max_price:
                max_price = bid.price
                message = bid.message
        return message, max_price
