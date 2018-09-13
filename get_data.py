import os
import multiprocessing as mp
import json

import requests
from tqdm import tqdm

# Get latest comic
num_comics = requests.get("https://xkcd.com/info.0.json").json()['num']

if "XDG_CONFIG_HOME" in os.environ:
    xkcd_file = os.path.join(os.environ["XDG_CONFIG_HOME"], "xkcd")
else:
    xkcd_file = os.path.join(os.environ["HOME"], ".config", "xkcd")

if not os.path.exists(xkcd_file):
    open(xkcd_file, 'x').close()

comics = []

def get_comic(i):
    try:
        return requests.get("https://xkcd.com/{}/info.0.json".format(i)).json()
    except:
        print("Can't get comic #{}".format(i))
        return {"num": i, "safe_title": "Unknown"}


with mp.Pool() as pool:
    comics = list(tqdm(pool.imap(get_comic, list(range(1, num_comics + 1))),
                  total=num_comics,
                  unit="comics",
                  desc="downloading data"))

comics.sort(key=lambda x: x['num'] if x else print(x))

with open(xkcd_file, 'w') as f:
    for comic in tqdm(comics, unit="comics", desc="saving data"):
        f.write("{} {}\n".format(comic['num'], comic['safe_title']))
