.. _marketdata:

==========
MarketData
==========

To receive market data from reactive-platform, use `reactive.platform.marketdata.MDClient`
class to set up a websocket connection and consume market data. A `MDClient` object requires
a API token and address. The token is issued from the trading platform under account settings:

.. code:: python

    from reactive.platform.marketdata.mdclient import MDClient

    key = 'xxx'
    addr = "wss://api.platform.reactivemarkets.com/stream"
    md_client = Client(addr=addr, key=key)


Before consuming data, create your own callback function to handle market data, and create an
application coroutine to send market data subscription.

.. code:: python

    from reactive.platform.marketdata.marketdata import MarketData


    def md_print_handler(md: MarketData):
    """
    implement a market data callback handler to print best bid and offer.
    """

    best_bid = md.bid_price[0] if len(md.bid_price) > 0 else None
    best_offer = md.offer_price[0] if len(md.offer_price) > 0 else None
    print(md.market, best_bid, best_offer)

    async def app_run(c: MDClient):
    """
    implement an application run coroutine to and subscribe or
    unsubscribe markets.
    """

    await c.subscribe(["BTCUSD-CNB"])

Then run the application as following:

.. code:: python

    run = asyncio.ensure_future(md_client.run(app_run, md_print_handler))
    asyncio.get_event_loop().run_until_complete(run)
