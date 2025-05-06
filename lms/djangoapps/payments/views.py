from dataclasses import dataclass

from common.djangoapps.edxmako.shortcuts import render_to_response
from .models import Order

from .processors import PayFort


# def get_tenant_processor():
#     """
#     Hardcoded, should use tenant configs.
#     :return:
#     """
#
#     processor = PayFort()


@dataclass
class Processor:
    title: str
    slug: str
    link: str


def start_order(request):
    sku = request.GET['sku']

    return render_to_response('payments/start_order.html', {
        'sku': sku,
        'item': 'REGA SREI Course',
        'methods': [
            Processor(title='Credit Card with PayFort', slug='payfort', link='/payment/pay/payfort'),
            Processor(title='Mada Card with HyperPay', slug='mada', link='#'),
            Processor(title='PayPal', slug='paypal',
                      link='https://www.paypal.com/donate/?hosted_button_id=L2PPE7SZ52FUG'),
        ],
    })


def payment_form(request, provider):

    processor = PayFort()

    order = Order(

    )

    return processor.payment_view(
        order=order,
        request=request,
        use_client_side_checkout=False,
    )


def callback(request):
    pass


def webhook(request):
    pass


def invoice(request):
    pass
