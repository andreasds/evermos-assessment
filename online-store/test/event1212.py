import json
import requests
import threading
import time

endpoint_url = 'http://172.17.0.1:18001/'

def worker(customer, product, with_lock):
    for i in range(11):
        # add product into cart
        r = requests.post(
            ''.join([endpoint_url, 'cart/add']),
            json = {
                'customer_id': customer['id'],
                'product_id': product['id'],
                'quantity': 3,
            },
        )
        if r.status_code != 200:
            print(''.join([ customer['username'], ' ', json.loads(r.content)['Message'] ]))

        # order product
        r = requests.post(
            ''.join([endpoint_url, 'order/add']),
            json = {
                'customer_id': customer['id'],
                'with_lock': with_lock,
            },
        )
        if r.status_code != 200:
            print(''.join([ customer['username'], ' ', json.loads(r.content)['Message'] ]))

def run_threads(func, customers, product, with_lock):
    threads = []
    for customer in customers:
        args = (customer, product, with_lock)
        thread = threading.Thread(target=func, args=args)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    current_time = int(time.time())
    # create 10 customer
    customers = []
    for i in range(10):
        r = requests.post(
            ''.join([endpoint_url, 'customer/add']),
            json = {
                'username': ''.join(['customer', str(i+1), '_', str(current_time)])
            },
        )
        customers.append(json.loads(json.loads(r.content)['Data']))

    # create product with stock 299
    r = requests.post(
        ''.join([endpoint_url, 'product/add']),
        json = {
            'product_name': 'testing_product',
            'stock': 299,
        },
    )
    product = json.loads(json.loads(r.content)['Data'])

    ### brute force order without locking
    print()
    print()
    print('### Testing Problem')
    print('* There is a product with 299 stocks')
    print('* 10 customer will buy 3 pcs products for 11 times transaction at the same time')
    print()
    print('== 12.12 event...')
    run_threads(worker, customers, product, False)

    # get last stock
    r = requests.get(
        ''.join([endpoint_url, 'product/', str(product['id']) ]),
    )
    last_stock = json.loads(r.content)['Data']['stock']

    # get ordered quantity
    r = requests.get(
        ''.join([endpoint_url, 'order/product/', str(product['id']) ]),
    )
    ordered_qty = json.loads(r.content)['Data']

    print('')
    print('Expectation ==> Last stock = 2, Ordered qty = 297')
    print(''.join([ 'Result      ==> Last stock = ', str(last_stock), ', Ordered qty = ', str(ordered_qty) ]))

    # create another product with stock 299
    r = requests.post(
        ''.join([endpoint_url, 'product/add']),
        json = {
            'product_name': 'testing_product',
            'stock': 299,
        },
    )
    product = json.loads(json.loads(r.content)['Data'])

    # remove product in cart
    for customer in customers:
        r = requests.get(
            ''.join([endpoint_url, 'cart/', str(customer['id'])]),
        )
        for cart in json.loads(r.content)['Data']:
            if cart['out_of_stock']:
                r = requests.post(
                    ''.join([endpoint_url, 'cart/remove']),
                    json = {
                        'customer_id': cart['customer_id'],
                        'product_id': cart['product_id'],
                    },
                )

    ### brute force order with locking
    print()
    print()
    print('### Testing Handling Problem')
    print('* There is a product with 299 stocks')
    print('* 10 customer will buy 3 pcs products for 11 times transaction at the same time')
    print()
    print('== 12.12 event...')
    run_threads(worker, customers, product, True)

    # get last stock
    r = requests.get(
        ''.join([endpoint_url, 'product/', str(product['id']) ]),
    )
    last_stock = json.loads(r.content)['Data']['stock']

    # get ordered quantity
    r = requests.get(
        ''.join([endpoint_url, 'order/product/', str(product['id']) ]),
    )
    ordered_qty = json.loads(r.content)['Data']

    print('')
    print('Expectation ==> Last stock = 2, Ordered qty = 297')
    print(''.join([ 'Result      ==> Last stock = ', str(last_stock), ', Ordered qty = ', str(ordered_qty) ]))
