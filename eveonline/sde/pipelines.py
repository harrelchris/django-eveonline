import pathlib
import urllib.request

from django.conf import settings
from django.db.models import Model
from django.db.transaction import atomic
import numpy as np
import pandas as pd

from eveonline.sde import models

SDE_CACHE_DIR: pathlib.Path = getattr(settings, "SDE_CACHE_DIR", settings.BASE_DIR / ".sde")
SDE_CACHE_DIR.mkdir(parents=True, exist_ok=True)


class Pipeline:
    file_name: str = None
    model: Model = None
    in_cols: list = None
    out_cols: list = None
    null_cols: list = None

    def run(self, cache: bool):
        df = self.extract(cache)
        df = self.transform(df=df)
        self.load(df=df)

    def extract(self, cache: bool) -> pd.DataFrame:
        url = f"https://www.fuzzwork.co.uk/dump/latest/{self.file_name}.csv.bz2"
        if cache:
            cache_path = SDE_CACHE_DIR / f"{self.file_name}.csv.bz2"
            if not cache_path.exists():
                self.download_file(url=url, path=cache_path)
            return pd.read_csv(cache_path)
        else:
            return pd.read_csv(url)

    def download_file(self, url: str, path: pathlib.Path):
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        content = response.read()
        with path.open("wb") as file:
            file.write(content)

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


class Categories(Pipeline):
    file_name = "invCategories"
    model = models.Categories
    in_cols = [
        "id",
        "name",
        "icon_id",
        "published",
    ]
    out_cols = [
        "id",
        "name",
    ]


class ContrabandTypes(Pipeline):
    file_name = "invContrabandTypes"
    model = models.ContrabandTypes
    in_cols = [
        "faction_id",
        "type_id",
        "standing_loss",
        "confiscate_min_sec",
        "fine_by_value",
        "attack_min_sec",
    ]
    out_cols = [
        "faction_id",
        "type_id",
        "standing_loss",
        "confiscate_min_sec",
        "fine_by_value",
        "attack_min_sec",
    ]


class ControlTowerResources(Pipeline):
    file_name = "invControlTowerResources"
    model = models.ControlTowerResources


class Flags(Pipeline):
    file_name = "invFlags"
    model = models.Flags
    in_cols = ["id", "name", "text", "order_id"]
    out_cols = ["id", "name", "text", "order_id"]


class Groups(Pipeline):
    file_name = "invGroups"
    model = models.Groups


class Items(Pipeline):
    file_name = "invItems"
    model = models.Items


class MarketGroups(Pipeline):
    file_name = "invMarketGroups"
    model = models.MarketGroups


class MetaGroups(Pipeline):
    file_name = "invMetaGroups"
    model = models.MetaGroups


class MetaTypes(Pipeline):
    file_name = "invMetaTypes"
    model = models.MetaTypes


class Names(Pipeline):
    file_name = "invNames"
    model = models.Names


class Positions(Pipeline):
    file_name = "invPositions"
    model = models.Positions


class Traits(Pipeline):
    file_name = "invTraits"
    model = models.Traits


class TypeMaterials(Pipeline):
    file_name = "invTypeMaterials"
    model = models.TypeMaterials


class Types(Pipeline):
    file_name = "invTypes"
    model = models.Types


class UniqueNames(Pipeline):
    file_name = "invUniqueNames"
    model = models.UniqueNames


class Volumes(Pipeline):
    file_name = "invVolumes"
    model = models.Volumes
