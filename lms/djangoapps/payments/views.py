from dataclasses import dataclass

from common.djangoapps.edxmako.shortcuts import render_to_response

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
            Processor(title='Payfort', slug='payfort', link='#'),
            Processor(title='Mada', slug='mada', link='#'),
            Processor(title='PayPal', slug='paypal', link='https://www.paypal.com/donate/?hosted_button_id=L2PPE7SZ52FUG'),
        ],
    })


def callback(request):
    pass


def webhook(request):
    pass


def invoice(request):
    pass
