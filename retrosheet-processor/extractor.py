import io
import logging
import requests
import zipfile

from glob import glob
from typing import List


logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO,
)


def get_retrosheet_events(
        years: List[int], data_dir: str
    ) -> List[str]:
    
    for year in years:
        url = f"https://www.retrosheet.org/events/{year}eve.zip"
        logger.info(f"fetching data from {url}, saving to {data_dir}")
        
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(f"{data_dir}/retrosheet")

    data_paths = f"{data_dir}/retrosheet/*.EV*"

    retrosheet_events = []
    for data_path in glob(data_paths):
        retrosheet_events += open(data_path, "r").read().splitlines()

    return retrosheet_events


if __name__ == "__main__":
    get_retrosheet_events([2020], "/Users/timhealz/code/data")