.. _quickstart:

==========
Quickstart
==========

The Reactive Platform API for python.

----------------
Rest API Client
----------------

A API token for a client must be granted from the platform under account settings.

Create a Rest API `Client` with the token and platform address.

.. code:: python

    from reactive.platform.rest.client import Client
    api_key = 'xxx'
    url = "https://api.platform.reactivemarkets.com"
    rc = Client(url=url, api_key=api_key)

Use methods of `rc` client to access data.

---------------
Reference Data
---------------

Reference data includes asset, instrument, venue and markets on Reactive Platform.

.. code:: python

    asset_ref = rc.fetch_asset_ref_data()
    assets = asset_ref.to_json(indent=None)
    asset_dict = asset_ref.to_dict()

    instr_ref = rc.fetch_instr_ref_data()
    instrs = instr_ref.to_json()

    venue_ref = rc.fetch_venue_ref_data()
    venues = venue_ref.to_json()

    market_ref = rc.fetch_market_ref_data()
    markets = market_ref.to_json()

The refData objects have methods: `to_json` and `to_dict` to get a json string or python dict.

If client uses pandas locally, the reference data can be viewed in a Dataframe table in jupyter-note
book:

.. code:: python

    import pandas as pd
    df = pd.read_json(market_ref.to_json())
    df
