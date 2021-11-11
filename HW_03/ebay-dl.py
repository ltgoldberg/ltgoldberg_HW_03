import argparse
import requests
from bs4 import BeautifulSoup
import json

def parse_itemssold(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string.

    >>> parse_itemssold('38 sold')
    38
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0

def parse_price(text):
    '''
    >>> parse_price('+$10.52 shipping')
    1052
    >>> parse_price('Free 3 day shipping')
    0
    '''
    numbers = ''
    if text.find("$")==-1:
        return 0
    if text.find("to")!=-1:
        text = text[:text.find("to")]
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'Free' in text:
        return 0
    else:
        return (int(numbers))

def parse_shippingcost(text):
    '''
    >>> parse_shippingcost('+$3.37 shipping')
    337
    >>> parse_shippingcost('Free 2 day shipping')
    0
    '''
    shipping_cost = ''
    if 'Free' in text and 'shipping' in text:
        return 0
    else:
        for char in text:
            if char in '1234567890':
                shipping_cost += char
        return int(shipping_cost)

# this if statement says only run the code below when the python file is run "normally"
# where normally means not in the doctests
if __name__ == '__main__':

    # get command line arguments
    parser = argparse.ArgumentParser(description='Download information from ebay and convert it to JSON.')
    parser.add_argument('search_term')
    args = parser.parse_args()
    print('args.search_term=', args.search_term)

    # list of all items found in all ebay webpages
    items = []

    # loop over the ebay webpages
    for page_number in range(1,11):
        # build the url
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' 
        url += args.search_term
        url += '&_sacat=0&_pgn='
        url += str(page_number) 
        url += '&rt=nc'
        print('url=', url)

        # download the html
        r = requests.get(url)
        status = r.status_code
        print('status=', status)
        html = r.text

        # process the html
        soup = BeautifulSoup(html, 'html.parser')

        # loop over the items on the page
        tags_items = soup.select('.s-item')
        for tag_item in tags_items:

            name = None
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name:
                name = tag.text

            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = parse_price(tag.text)

            status = None
            tags_status = tag_item.select('.SECONDARY_INFO')
            for tag in tags_status:
                status = tag.text

            shipping_cost = None
            tags_shippingcost = tag_item.select('.s-item__shipping')
            for tag in tags_shippingcost:
                shipping_cost = parse_price(tag.text)

            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns = True

            items_sold = None
            tags_itemssold = tag_item.select('.s-item__hotness')
            for tag in tags_itemssold:
                items_sold = parse_itemssold(tag.text)

            item = {
                'name': name,
                'price': price,
                'status': status,
                'shipping_cost': shipping_cost,
                'free_returns': freereturns,
                'items_sold': items_sold,
            }
            items.append(item)

            print('len(tags_items)=',len(tags_items))
            print('len(items)=',len(items))

    # write the json to a file
    filename = args.search_term + '.json'
    with open(filename, 'w', encoding='ascii') as f:
        f.write(json.dumps(items))