.. _marketdata:

==========
MarketData
==========

To subscribe market data from reactive-platform, use `reactive.platform.feed.FeedClient`
class to set up a websocket connection and consume data. A `FeedClient` object requires
a API token and URL. The token is issued from the trading platform UI under account settings:

.. code:: python

    from reactive.platform.feed.feedclient import FeedClient

    TOKEN = 'xxx'
    addr = "wss://api.platform.reactivemarkets.com/feed"
    feed_client = FeedClient(addr=addr, key=TOKEN)


Before starting subscriptions, creates a callback function to handle market data, and create an
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

    await c.subscribe(["BTCUSD-CNB"], depth=10, grouping=1)


User can specify book depth and tick grouping values for subscribing markets, to determine different
view on the market data. Successful subscription will be notified via a feed ack message,
including a feed_id which is an integer number to represents a book view (depth and grouping),
and requested id corresponding to the client request. On the other hand, a feed reject message is
received for a bad subscription. Currently only support depths: [1, 5, 10, 20] and grouping ticks
with [1, 10, 50, 100]. (Not all the instruments are supported for different grouping yet. Use 1 as
grouping value at this moment.)

Run the application as following:

.. code:: python

    run = asyncio.ensure_future(feed_client.run(app_run, md_print_handler))
    asyncio.get_event_loop().run_until_complete(run)
