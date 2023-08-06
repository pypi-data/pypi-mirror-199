import pandas as pd

from concurrent.futures import ThreadPoolExecutor
from gandai.datastore import Cloudstore

ds = Cloudstore()


def companies_query(search_key: str) -> pd.DataFrame:
    keys = ds.keys(f"searches/{search_key}/companies")
    if len(keys) == 0:
        return pd.DataFrame(dict(domain=[]))
    table_uris = [f"gs://{ds.BUCKET_NAME}/{k}" for k in keys]
    with ThreadPoolExecutor(max_workers=10) as exec:
        futures = exec.map(pd.read_feather, table_uris)
    df = pd.concat(list(futures))
    df = df.dropna(subset=["domain"])  #
    df = df.drop_duplicates(subset=["domain"])
    return df.reset_index(drop=True)


def events_query(search_key: str) -> pd.DataFrame:
    keys = ds.keys(f"searches/{search_key}/events")
    return pd.DataFrame(ds.load_async(keys))


def comments_query(search_key: str) -> pd.DataFrame:
    keys = ds.keys(f"searches/{search_key}/comments")
    return pd.DataFrame(ds.load_async(keys))


def searches_query() -> pd.DataFrame:
    keys = ds.keys(f"searches/")
    keys = [k for k in keys if k.endswith("search")]
    df = pd.DataFrame(ds.load_async(keys))
    df["status"] = df["meta"].apply(lambda x: f"{x.get('status')}")
    df = df[~df["status"].isin(["Completed Engagement", "Dead Post-Mandate"])]
    df["group"] = df["meta"].apply(lambda x: f"{x.get('status')} - {x.get('stage')}")
    df["research"] = df["meta"].apply(lambda x: x.get("research", ""))
    df = df[["key", "label","status", "group", "research"]].fillna("")
    return df.reset_index(drop=True)


def dealcloud_company_query() -> pd.DataFrame:
    table_uri = f"gs://{ds.BUCKET_NAME}/sources/dealcloud/company_id_domain.feather"
    df = pd.read_feather(table_uri)
    df = (
        df[["dealcloud_id", "domain", "days_since_contact"]]
        .drop_duplicates(subset=["domain"])
        .reset_index(drop=True)
    )
    assert "domain" in df.columns
    return df
