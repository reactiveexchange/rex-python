.. _platform websocket:

==========
MarketData
==========

To subscribe market data from reactive-platform, use `reactive.platform.feed.FeedClient`
class to set up a websocket connection and consume data. A `FeedClient` object requires
a API token and URL. The token is issued from the trading platform UI under account settings:

.. code:: python

    from reactive.platform.feed.client import FeedClient

    TOKEN = 'xxx'
    addr = "wss://api.platform.reactivemarkets.com/feed"
    feed_client = FeedClient(addr=addr, key=TOKEN)


Before start to subscribe data from feed server, two callback functions should be implemented:
`data_handler` to process reading data from feed server, and `client_handler` function to control
`FeedClient` (send request to platform) and execute user's codes.

.. code:: python

    from reactive.platform.feed.mdsnapshotl2 import MDSnapshotL2


    def data_handler(data):
    """
    implement a data callback handler to print market data.
    """
    if isinstance(obj, MDSnapshotL2):
        md = obj
        best_bid = md.bid_price[0] if md.bid_price.size > 0 else None
        best_offer = md.offer_price[0] if md.offer_price.size > 0 else None
        print(md.market, best_bid, best_offer)
        print(md.depth)
    else:
        print(" not market data message")

    async def client_handler(c: FeedClient):
    """
    implement client_handler
    """

    await c.subscribe(["BTCUSD-CNB"], depth=10, grouping=1)


User can specify book depth and tick grouping values for subscribing markets, to determine different
view on the market data. Successful subscription will be notified via a feed ack message,
including a feed_id which is an integer number to represents a book view (depth and grouping),
and requested id corresponding to the client request. On the other hand, a feed reject message is
received for a bad subscription. Currently only support depths: [1, 5, 10, 20] and grouping ticks
with [1, 10, 50, 100]. (Currently, only grouping value `1` for all the instruments are supported)

Run the application as following:

.. code:: python

    run = asyncio.ensure_future(feed_client.run(client_handler, data_handler))
    asyncio.get_event_loop().run_until_complete(run)


===========
PublicTrade
===========

Public trade channel publishes real-time trade message from platform, clients must set
`FeedType` to `FeedTypeTrade` in the requests.


.. code:: python

    async def client_handler(c: FeedClient):
    """
    implement client_handler
    """

    await c.subscribe(["BTCUSD-CNB"], feed_type=FeedType.Trade)

