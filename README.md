# Reactive-Platform Python

The Reactive Platform API for Python.

## Getting Started

### Install

The package only support python3.7 and python3.8, not for lower versions.

Install the package in a python environment:

```bash
$ pip install reactive-platform
```

Uninstall the package:

```bash
$ pip uninstall reactive-platform
```

### Using REST API

The REST API has endpoints for different type data, e.g. orders, analytics and references.
At this moment, this packages only supports reference data. To access the platform, a API
token must be granted from platform UI.

### Create a REST client

Create a client first:

```python
from reactive.platform.client import Client

key = 'xxx'
url = "https://api.platform.reactivemarkets.com"
rc = Client(url=url, key=key)

```

### Reference Data

Reference data includes asset, instrument, venue and markets. Get those data:

```python

asset_ref = rc.fetch_asset_ref_data()
assets = asset_ref.to_json(indent=None)
asset_dict = asset_ref.to_dict()

instr_ref = rc.fetch_instr_ref_data()
instrs = instr_ref.to_json()

venue_ref = rc.fetch_venue_ref_data()
venues = venue_ref.to_json()

market_ref = rc.fetch_market_ref_data()
markets = market_ref.to_json()

```

If client uses pandas locally, the reference data can be viewed in a Dataframe table in jupyter-note
book:

```python
import pandas as pd

df = pd.read_json(market_ref.to_json())
df
```

## Feed Gateway WekSocket API

The websocket feed provides real-time level 2 market data snapshots and public trades via

```angular2
wss://api.platform.reactivemarkets.com/feed
```

### Create an FeedClient

To access feed gateway via web socket, create an FeedClient which manages the web socket connection
and provides methods to access the gateway.

```python
from reactive.platform.feed.feedclient import FeedClient

TOKEN = 'xxx'
addr = "wss://api.platform.reactivemarkets.com/feed"
feed_client = FeedClient(addr=addr, key=TOKEN)
```

Use `feed_client` to subscribe market data, see a full example in
`example/marketdata.py`. The client can specify book view parameters in the request. Currently,
the feed gateway supports, book depths (1, 5, 10, 20), tick grouping (1, 50) and frequency
(100ms).

The message protocol via feed gateway is Flatbuffers, which provides an efficient
serialization/deserializaton mechanism in terms of both processing and space requirements.
The reactive-platform generated python classes Flatbuffer schema are located under
`reactive.platform.fbs`.
