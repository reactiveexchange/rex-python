.. _quickstart:

==========
Quickstart
==========

To use reactive-platform package to access reactive platform, a API token must be used,
and it can be created from the trading platform under account settings.

----------------
Create Client
----------------

`Client` represents a client class, and a user must to create a client first with
API key and platform address.

.. code:: python

    from reactive.platform.client import Client
    key = 'xxx'
    url = "https://api.platform.reactivemarkets.com"
    rc = Client(url=url, key=key)

Use methods of `rc` client to access data.

---------------
Reference Data
---------------

Reference data includes asset, instrument, venue and markets.

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

If client use pandas locally, the reference data can be viewed as a Dataframe table in jupyter-note
book:

.. code:: python

    import pandas as pd
    df = pd.read_json(market_ref.to_json())
    df
