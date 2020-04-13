.. _marketdata:

==========
MarketData
==========

To receive market data from reactive-platform, use `reactive.platform.feed.FeedClient`
class to set up a websocket connection and consume market data. A `FeedClient` object requires
a API token and address. The token is issued from the trading platform under account settings:

.. code:: python

    from reactive.platform.feed.feedclient import FeedClient

    TOKEN = 'xxx'
    addr = "wss://api.platform.reactivemarkets.com/feed"
    feed_client = FeedClient(addr=addr, key=TOKEN)


Before consuming data, create your own callback function to handle market data, and create an
application coroutine to send market data subscription.

.. code:: python

    from reactive.platform.feed.level2book import Level2Book


    def md_print_handler(md: Level2Book):
    """
    implement a market data callback handler to print best bid and offer.
    """

    best_bid = md.bid_side[0] if len(md.bid_side) > 0 else None
    best_offer = md.offer_side[0] if len(md.offer_side) > 0 else None
    print(md.market, best_bid.price, best_offer.price)

    async def app_run(c: FeedClient):
    """
    implement an application run coroutine to and subscribe or
    unsubscribe markets.
    """

    await c.subscribe(["BTCUSD-CNB"])

Then run the application as following:

.. code:: python

    run = asyncio.ensure_future(feed_client.run(app_run, md_print_handler))
    asyncio.get_event_loop().run_until_complete(run)
