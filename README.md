# Reactive Markets Platform SDK Python

The Reactive Platform SDK for Python.

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

The REST API has endpoints for various kinds of data from platform, e.g. orders, analytics and
references. This package now only supports querying reference data. To access the platform, a API
token must be granted from platform UI.

### Create a REST client

Create a client first:

```python
from reactive.platform.rest.client import Client

api_key = 'xxx'
url = "https://api.platform.reactivemarkets.com"
rc = Client(url=url, api_key=api_key)
```

### Reference Data

Reference data includes asset, instrument, venue and markets. Get those data:

```python
asset_ref = rc.fetch_asset_ref()
# json format assets reference data
assets = asset_ref.to_json()
print("asset reference:\n", assets)
# dict format assets
assets_dict = asset_ref.to_dict()
print("assets dict:\n", assets)

# instr reference
instr_ref = rc.fetch_instr_ref()
instrs = instr_ref.to_json()
print("instrument reference:\n", instrs)

# venue reference
venue_ref = rc.fetch_venue_ref()
venues = venue_ref.to_json()
print("venue reference:\n", venues)

# market reference
market_ref = rc.fetch_market_ref()
markets = market_ref.to_json()
print("market reference:\n", venues)
```

If client uses pandas, the reference data can be viewed in a Dataframe table in jupyter-notebook:

```python
import pandas as pd

df = pd.read_json(market_ref.to_json())
df
```

## Platform WebSocket API

The websocket feed provides real-time level 2 market data snapshots, public trades and liquidation
via

```
wss://api.platform.reactivemarkets.com/feed
```

## WebSocket Client

To access the platform via web socket, create a Client which manages the web socket connection
and provides methods to access the platform. See the example in `example/wsclient.py`.

The message protocol is Flatbuffers, which provides an efficient
serialization/deserializaton mechanism in terms of both processing and space requirements.
The flatbuffer message python API for the platform is in the `reactive-papi` package.

Client decodes receiving messages into `reactive.papi.Message.Message` and allow user to apply
user defined `data_handler` call back to handle the flatbuffer message.

### Create a FeedClient

The platform-py also provides another option, `FeedClient`. 

```python
from reactive.platform.feed.client import FeedClient

api_key = 'xxx'
addr = "wss://api.platform.reactivemarkets.com/feed"
feed_client = FeedClient(addr=addr, api_key=api_key)
```

FeedClient provides methods `subscribe` and `unsubscribe` to control sending request to platform,
and implement python classes in `reactive.platform.feed` subpackage for corresponding flatbuffer
message types. see a full example in `example/marketdata.py` or `example/trade`. The client can
specify book view parameters in the request. Currently, the feed gateway supports, book
depths (1, 5, 10, 20), tick grouping (1, 50), and frequency integer (1 or a larger number).
