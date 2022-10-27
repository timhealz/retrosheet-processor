
import csv
import logging

import pyarrow as pa
import pyarrow.parquet as pq
from pyarrow.compute import cast

from argparse import ArgumentParser
from collections import defaultdict

from extractor import get_retrosheet_events
from schemas.tools import get_schema, get_event_type_dict


logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO,
)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="""
        CLI interface for processing retrosheet.org data
        """
    )
    parser.add_argument(
        "-d",
        "--data_dir",
        type=str,
        help="Where to save the raw data"
    )
    parser.add_argument(
        "-s",
        "--start-year",
        type=int,
        help="Starting year to process data for"
    )
    parser.add_argument(
        "-e",
        "--end-year",
        type=int,
        help="Ending year to process data for"
    )
    args = parser.parse_args()


    logger.info(f"processing data for {args.start_year} - {args.end_year}")

    retrosheet_events = get_retrosheet_events(
        range(args.start_year, args.end_year + 1),
        args.data_dir
    )

    processed_data = defaultdict(list)
    for i, event in enumerate(retrosheet_events):

        if i % 1e5 == 0:
            logger.info(f"{i} events processed")

        event_type, row = event.split(",", maxsplit=1)

        if event_type == "id":
            game_id = row
            continue

        if event_type == "version":
            continue

        if event_type not in processed_data:
            try:
                processed_data[event_type] = get_event_type_dict(
                    event_type
                )
            except:
                logger.error(row)

        schema = get_schema(event_type)


        parsed_row = list(csv.reader(
            [row],
            delimiter=',',
            quotechar='"'
        ))[0]

        row = dict(zip(
            schema.names,
            [game_id] + parsed_row,
        ))

        for field_name, val in row.items():
            processed_data[event_type][field_name].append(val)

    for event_type in processed_data.keys():

        schema = get_schema(event_type)

        for field_name, data_type in zip(schema.names, schema.types):
            processed_data[event_type][field_name] = cast(
                processed_data[event_type][field_name],
                target_type=data_type
            )
        
        pq.write_table(
            pa.Table.from_pydict(
                processed_data[event_type],
                schema,
            ),
            f"/Users/timhealz/code/data/parquet/{event_type}s.parquet",
            compression="snappy"
        )
