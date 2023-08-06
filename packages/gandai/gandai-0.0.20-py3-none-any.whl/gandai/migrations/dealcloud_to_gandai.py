import re
import pandas as pd
from time import time

from gandai.adapters.dealcloud import seed_search
from gandai.services import Query
from gandai.datastore import Cloudstore

ds = Cloudstore()


def engagement_export_query(fp) -> pd.DataFrame:
    # DRAFT
    """
    Read in the DealCloud engagements file and return a dataframe
    """
    df = pd.read_excel(fp)
    df.columns = [col.lower().replace(" ", "_").replace(".", "") for col in df.columns]
    today = pd.to_datetime("today")
    df["modified_days_ago"] = (today - pd.to_datetime(df["modified_date"])).dt.days
    date_cols = [col for col in df.columns if col.endswith("_date")]
    # date_cols = [
    #     "added_date",
    #     "created_date",
    #     "modified_date",
    #     "completed_engagement_date",
    #     "project_end_date",
    #     "pitch_delivered_date",
    #     "engagement_signed_date"
    # ]
    for col in date_cols:
        df[col] = df[col].apply(lambda x: str(x)[0:10])
    df = df.dropna(subset="engagement_name")  # never hit this condition
    df = df.sort_values("modified_date", ascending=False)
    return df


def company_export_query(fp) -> pd.DataFrame:
    def _get_domain(url) -> str:
        url = url.replace("http://", "").replace("https://", "").replace("www.", "")
        return url.split("/")[0]

    df = pd.read_excel(fp)  # hmm why so slow
    df.columns = [col.replace(" ", "_").replace(".", "").lower() for col in df.columns]
    df["domain"] = df["website"].dropna().apply(_get_domain)
    df["days_since_contact"] = (
        df["days_since_contact"].dropna().apply(lambda x: int(re.findall(r"\d+", x)[0]))
    )
    df = (
        df[["dealcloud_id", "domain", "days_since_contact"]]
        .drop_duplicates(subset=["domain"])
        .reset_index(drop=True)
    )
    return df


def run_dealcloud_engagement_to_gandai_search():
    """
    Transfer DealCloud engagements to Gandai
    """
    df = engagement_export_query(
        "/Users/parker/Development/gandai-workspace/notebooks/2023-03-26/data/engagement.xlsx"
    )
    df = df[df["modified_days_ago"] < 365].reset_index(drop=True)
    df = df[
        ~df["status"].isin(
            ["Lost Pre-Mandate", "Completed Engagement", "Dead Post-Mandate"]
        )
    ].reset_index(drop=True)
    # for i, row in list(df.iterrows())[0:10]:
    #     seed_search(row)
    for i, row in df.iterrows():
        seed_search(row, True)


def run_dealcloud_company_to_gandai_company():
    """
    Transfer DealCloud companies to Gandai
    """
    df = company_export_query(
        "/Users/parker/Development/gandai-workspace/notebooks/2023-03-26/data/company.xlsx"
    )
    table_uri = f"gs://{ds.BUCKET_NAME}/sources/dealcloud/company_id_domain.feather"
    df.to_feather(table_uri)


def main():
    """
    1. Transfers from DealCloud Engagement to Gandai Search
    2. Transfers from DealCloud Companies to Gandai dealcloud_company_domain.feather
    """
    run_dealcloud_engagement_to_gandai_search()
    run_dealcloud_company_to_gandai_company()


if __name__ == "__main__":
    start = time()
    main()
    print(f"Total time: {time() - start}")
