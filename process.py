import glob
import dask
import pandas as pd

col_widths = [3, 4, 12, 4, 6, 6, 5, 7, 6, 5]
cols = [
    "basin",
    "number",
    "init",
    "technum",
    "tech",
    "tau",
    "lat",
    "lon",
    "vmax",
    "mslp",
]
index = ["basin", "number", "tau", "tech"]


def lat_lon_to_num(string):
    value = pd.to_numeric(string[:-1], errors="coerce") / 10
    if string.endswith(("N", "E")):
        return value
    else:
        return -value


@dask.delayed()
def process_df(file):
    df = pd.read_fwf(file, widths=col_widths, names=cols, header=None, na_value="nan")
    df = df.astype(str).applymap(lambda string: string.strip(","))
    df["lat"] = df["lat"].apply(lat_lon_to_num)
    df["lon"] = df["lon"].apply(lat_lon_to_num)
    df["init"] = pd.to_datetime(df["init"], format="%Y%m%d%H", errors="coerce")
    df[["number", "vmax", "mslp"]] = df[["number", "vmax", "mslp"]].apply(
        pd.to_numeric, errors="coerce"
    )
    return df


for prefix in ["b", "a"]:
    df_list = dask.compute(
        [process_df(file) for file in sorted(glob.glob(f"{prefix}*.dat"))],
        scheduler="processes", num_workers=4
    )[0]
    df = pd.concat(df_list)
    label = "fcst" if prefix == "a" else "best"
    for year in df["init"].dt.year.unique():
        df.loc[df["init"].dt.year == year].set_index(index).to_parquet(
            f"{year:.0f}_{label}_track.parquet.gzip", compression="gzip")

