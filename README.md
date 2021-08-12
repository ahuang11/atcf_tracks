# Automated Tropical Cyclone Forecast (ATCF) Tracks

### Overview

Make ATCF Tracks accessible with a `wget` and `pandas.read_parquet`.

### Motivation

Trying to set up a machine learning model, but the data is so inconsistent and dirty from all sources... so I tidied up the data and shared it, hoping that it can help you too.

### Usage

In the command line:
`wget https://raw.githubusercontent.com/ahuang11/atcf_tracks/master/data/2020_fcst_track.parquet.gzip`

In Python:
```
import pandas as pd
df = pd.read_parquet("2020_fcst_track.parquet.gzip")
print(df.head())

# output
                                       init technum   lat   lon  vmax    mslp
basin number tau   tech
AL    1.0    -24.0 CARQ 2020-05-14 18:00:00      01  23.4 -83.6  20.0     0.0
             -18.0 CARQ 2020-05-14 18:00:00      01  23.4 -83.0  25.0     0.0
             -12.0 CARQ 2020-05-14 18:00:00      01  23.4 -82.4  25.0     0.0
             -6.0  CARQ 2020-05-14 18:00:00      01  23.5 -81.8  25.0     0.0
              0.0  CARQ 2020-05-14 18:00:00      01  23.7 -81.2  30.0  1013.0
```

### Notes

See download.py and process.py for source code
Data from https://ftp.nhc.noaa.gov/atcf/archive/
Docs at https://www.nrlmry.navy.mil/atcf_web/docs/database/new/database.html
