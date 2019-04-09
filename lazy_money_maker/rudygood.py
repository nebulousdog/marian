'''
Methods grouped becuase they all need a instantiated Fast Arrow client to reference.
'''

from flask import jsonify

from fast_arrow import (
    Client,
    Collection,
    Dividend,
    Stock,
    StockMarketdata,
    StockPosition,
)

from lazy_money_maker.utils.config import read_secrets
from lazy_money_maker.utils.sheets import list_to_row
from lazy_money_maker.utils.robinhood import rh_id_from_instrument_url

class RuddyGood():
    def __init__(self, **kwargs):
        self.options = kwargs
        self.client = None

    def rh_client(self):
        """start and memoize a RH connection via fast_arrow."""

        if self.client is None:
            print(f'authenticating....')

            secrets = read_secrets('rh_account')
            self.client = Client(username=secrets['username'], password=secrets['password'])
            self.client.authenticate()

            print('done.')

        return self.client

    def raw_dividends(self):
        """raw dividends via fast_arrow."""

        return Dividend.all(self.rh_client())

    def rh_dividends(self):
        """rh dividend infos formatted for personal use."""

        dividends = self.raw_dividends()

        return jsonify(dividends)

    def raw_positions(self):
        """raw robinhood positions."""

        return StockPosition.all(self.rh_client())

    def raw_stock(self, symbol, attributes=None):
        """raw robinhood stock infos. not personal position on the stock.

        if attributes is passed along, only return those attributes.
        """

        stock = Stock.fetch(self.rh_client(), symbol)

        if attributes is not None:
            return {k: stock[k] for k in attributes}

        return stock

    def raw_stocks(self, symbols):
        """raw robinhood stock infos."""

        stocks = Stock.all(self.rh_client(), symbols)

        return stocks

    def rh_positions(self, csv):
        """my portfolio positions. formatted for personal use in Google Sheets."""

        positions = self.raw_positions()
        instrument_urls = list(map(lambda p: p['instrument'], positions))

        instrument_data = {}
        for url in instrument_urls:
            data = self.rh_client().get(url)
            instrument_data[data['id']] = data

        formatted_positions = {}
        for position in positions:
            if float(position['quantity']) == 0.0:
                continue

            item = {}

            for k in ['average_buy_price', 'created_at', 'quantity']:
                item[k] = position[k]

            rh_id = rh_id_from_instrument_url(position['instrument'])

            data = instrument_data[rh_id]
            for k in ['simple_name', 'symbol', 'type']:
                item[k] = data[k]

            quote = self.raw_quote(item['symbol'])

            for k in [
                    'adjusted_previous_close',
                    'ask_price',
                    'bid_price',
                    'last_trade_price',
                    'last_extended_hours_trade_price',
                    'last_trade_price',
                    'previous_close',
                ]:
                item[k] = quote[k]

            formatted_positions[item['symbol']] = item

        if csv is not False:
            row = ''
            i = 0
            for item in list(formatted_positions.values()):
                if i == 0:
                    row += list_to_row(item.keys())

                row += list_to_row(item.values())
                i += 1

            return row

        return jsonify(formatted_positions)

    def raw_collection(self, tag):
        """raw robinhood collection info via fast_arrow."""

        return Collection.fetch_instruments_by_tag(self.rh_client(), tag)

    def rh_collection(self, tag):
        """rh collection. formatted for personal use"""

        return jsonify(self.raw_collection(tag))

    def raw_quote(self, symbol, attributes=None):
        """raw market price quote info via fast_arrow."""

        quote = StockMarketdata.quote_by_symbol(self.rh_client(), symbol)

        if attributes is not None:
            return {k: quote[k] for k in attributes}

        return quote

    def rh_quote(self, symbol):
        """formatted price quote infos for personal use."""

        quote = self.raw_quote(symbol, [
            "last_trade_price"
        ])

        return jsonify(quote)

    def raw_watchlist(self):
        """raw watchlist infos."""

    def rh_watchlist(self):
        """my watchlist. formatted position list."""

        return jsonify(self.raw_watchlist())
