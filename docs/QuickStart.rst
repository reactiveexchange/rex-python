.. _quickstart:

==========
Quickstart
==========

To use rex-py package to access reactive exchange platform, a API token must be used, and it can be
created from the trading platform under account settings.

----------------
Create RexClient
----------------

RexClient represents rex client class, and a user must to create a rex client first with
API key and platform API url

.. code:: python

    from rex.client import RexClient
    key = 'xxx'
    url = "https://api.crossfire-dev.reactivemarkets.net"
    rc = RexClient(key=key, url=url)

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
