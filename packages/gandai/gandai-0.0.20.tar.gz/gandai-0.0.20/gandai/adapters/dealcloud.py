import json
from gandai.datastore import Cloudstore
import pandas as pd

ds = Cloudstore()
keys = ds.keys()

DEFAULT_FILTERS = {
        "employee_count": {"max": 2500, "min": 25},
        "country": ["USA", "CAN", "MEX"],
        "state": [],
    }


def seed_search(engagement: pd.Series, force=False) -> None:
    data = json.loads(engagement.dropna().to_json())  # ugly
    search = {
        "key": data["dealcloud_id"],
        "label": data["engagement_name"],
        "meta": data,
        "keywords": [],
        "sort": {"employee_count": "desc"},
        "do_not_contact": [],
        "filters": DEFAULT_FILTERS,
    }
    search_key = f'searches/{search["key"]}/search'

    if search_key in keys:
        print(f"already exists: {search_key}")
        if force:
            print("force update")
            ds[search_key] = search
    else:
        ds[search_key] = search
        print(f"seeded: {search_key}")
