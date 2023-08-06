"""Play with the contents of `videos.db` programmatically and store results in data frames."""

import pandas as pd
import sqlite3
import fmdt.args
import fmdt.truth
import fmdt.config
import fmdt.db


# Add a videos.db file to our config
fmdt.download_csvs()

# config = fmdt.config.load_config()
# files_in_config = fmdt.config.listdir()

# print(files_in_config)
print(f"config directory: {fmdt.config.dir()}")

fmdt.download_dbs()
vids = fmdt.load_draco6() # list[Video]
for i in range(20):
    v = vids[i]
    print(f"{v.id()}: {v} has {len(v.meteors())} meteor(s) in our database")

print(".")
print(".")
print(".")

print(f"{vids[-1].id()}: {vids[-1]} has {len(vids[-1].meteors())} meteor(s) in our database")

id = 17
print(f"vids[{id}].meteors() -> {vids[id].meteors()[0]}")