
import logging

from typing import Any, Dict, List

import pyarrow as pa
import schemas.events as event_schemas


logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO,
)


def get_schema(event_type: str) -> pa.Schema:

    if event_type == "info":
        return event_schemas.INFO
    
    elif event_type == "start":
        return event_schemas.START_SUB
    
    elif event_type == "sub":
        return event_schemas.START_SUB
    
    elif event_type == "play":
        return event_schemas.PLAY
    
    elif event_type == "badj":
        return event_schemas.BADJ
    
    elif event_type == "padj":
        return event_schemas.PADJ

    elif event_type == "ladj":
        return event_schemas.LADJ

    elif event_type == "radj":
        return event_schemas.RADJ

    elif event_type == "data":
        return event_schemas.DATA

    elif event_type == "com":
        return event_schemas.COMMENT
    
    else:
        logger.error(event_type)
        raise NotImplementedError(
            "No schema for this event type is implemented!"
        )


def get_event_type_dict(event_type: str) -> Dict[str, List[Any]]:
    return {
        field_name: []
        for field_name in get_schema(event_type).names
    }