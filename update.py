#!/usr/bin/env python3

import csv
import io
import json
import logging
from pathlib import Path
import zipfile

logging.basicConfig(format="%(asctime)s %(message)s")
logging.getLogger().setLevel(logging.DEBUG)


def geojson(long, lat, properties):
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [long, lat]},
        "properties": properties,
    }


config_toml_template = Path("config.toml.template")
config_toml = Path("config.toml")


def open_csv():
    zip_path = Path("NationalFile.zip")
    logging.debug("%s", zip_path)
    z = zipfile.ZipFile("NationalFile.zip")
    entry = z.filelist[0]
    logging.debug("%s", entry.filename)
    run_id = Path(entry.filename).stem

    config_toml.write_text(config_toml_template.read_text().format(attribution=run_id))

    b = z.open(entry)
    f = io.TextIOWrapper(b, encoding="utf-8-sig")
    return f


properties_to_keep = {
    "FEATURE_ID": "gnis:feature_id",
    "FEATURE_NAME": "name",
    "FEATURE_CLASS": "gnis:Class",
    "MAP_NAME": "MAP_NAME",
    "STATE_ALPHA": "STATE_ALPHA",
    "COUNTY_NAME": "COUNTY_NAME",
    "ELEV_IN_M": "ELEV_IN_M",
    "ELEV_IN_FT": "ELEV_IN_FT",
}


def load_data():
    r = csv.DictReader(open_csv(), delimiter="|")
    row_count = 0
    with_source = 0
    with_prim = 0
    null_source = 0
    null_prim = 0
    for row in r:
        FEATURE_ID = row["FEATURE_ID"]
        row_count += 1
        properties = {
            (properties_to_keep[k]): v
            for (k, v) in row.items()
            if k in properties_to_keep
        }
        if row["SOURCE_LONG_DEC"] and row["SOURCE_LAT_DEC"]:
            long = float(row["SOURCE_LONG_DEC"])
            lat = float(row["SOURCE_LAT_DEC"])
            if (long, lat) == (0, 0):
                null_source += 1
            else:
                with_source += 1
                yield geojson(long, lat, properties)
        if row["PRIM_LONG_DEC"] and row["PRIM_LONG_DEC"]:
            long = float(row["PRIM_LONG_DEC"])
            lat = float(row["PRIM_LAT_DEC"])
            if (long, lat) == (0, 0):
                null_prim += 1
            else:
                with_prim += 1
                yield geojson(long, lat, properties)
    logging.debug(
        "row count %s, with source %s, with prim %s, null source %s, null prim %s",
        row_count,
        with_source,
        with_prim,
        null_source,
        null_prim,
    )


for row in load_data():
    print("\x1e", json.dumps(row))
