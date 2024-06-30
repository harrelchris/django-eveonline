from django.db.transaction import atomic
import numpy as np
import pandas as pd


class Pipeline:
    file_name: str = None
    model = None
    in_cols: list = None
    out_cols: list = None
    null_cols: list = None

    def run(self):
        df = self.extract()
        df = self.transform(df=df)
        self.load(df=df)

    def extract(self) -> pd.DataFrame:
        # TODO: support file caching
        url = f"https://www.fuzzwork.co.uk/dump/latest/{self.file_name}.csv.bz2"
        df = pd.read_csv(url)
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.in_cols:
            df.columns = self.in_cols
        df.replace({
            np.nan: None,
            "\\N": None,
        })
        df.dropna(subset=self.null_cols, inplace=True)
        if "published" in df.columns:
            df = df[df["published"] == True]  # noqa
        if self.out_cols:
            df = df[self.out_cols]
        return df

    @atomic
    def load(self, df: pd.DataFrame):
        self.model.objects.all().delete()
        records = []
        for _, row in df.iterrows():
            record = self.model(**row.to_dict())
            records.append(record)
        self.model.objects.bulk_create(records)
