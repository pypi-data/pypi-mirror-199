#!/usr/bin/env python3
from typing import Dict, Optional, List, Tuple

import singer
from c8connector import SchemaAttributeType
from pymongo.collection import Collection
from singer import get_logger, metadata, SchemaMessage, write_message

from macrometa_source_mongo.sync_strategies.common import calculate_destination_stream_name
from macrometa_source_mongo.exceptions import InvalidAwaitTimeException


logger = get_logger('macrometa_source_mongo')

def validate_config(config: Dict) -> None:
    """
    Validate configuration parameters.
    Args:
        config: Dictionary of config to validate

    Returns: None
    Raises: InvalidAwaitTimeException
    """
    if 'await_time_ms' in config:
        await_time_ms = config['await_time_ms']

        if not isinstance(await_time_ms, int):
            raise InvalidAwaitTimeException(await_time_ms, 'Not integer')

        if await_time_ms <= 0:
            raise InvalidAwaitTimeException(
                await_time_ms, 'time must be > 0')


def get_replication_method_from_stream(stream: Dict, replication_method: str) -> Optional[str]:
    """
    Search for the stream replication method
    Args:
        stream: stream dictionary
        replication_method: replication method

    Returns: replication method if defined, None otherwise

    """
    md_map = metadata.to_map(stream['metadata'])
    return md_map.get('replication-method', replication_method)


def is_log_based_stream(stream: Dict, replication_method: str) -> bool:
    """
    checks if stream uses log based replication method
    Returns: True if LOG_BASED, False otherwise
    """
    return get_replication_method_from_stream(stream, replication_method) == 'LOG_BASED'


def write_schema_message(stream: Dict):
    """
    Creates and writes a stream schema message to stdout
    Args:
        stream: stream catalog
    """
    write_message(SchemaMessage(
        stream=calculate_destination_stream_name(stream),
        schema=stream['schema'],
        key_properties=['_id']))


def is_stream_selected(stream: Dict) -> bool:
    """
    Checks the stream's metadata to see if stream is selected for sync
    Args:
        stream: stream dictionary

    Returns: True if selected, False otherwise

    """
    mdata = metadata.to_map(stream['metadata'])
    is_selected = metadata.get(mdata, (), 'selected')

    return is_selected is True


def streams_list_to_dict(streams: List[Dict]) -> Dict[str, Dict]:
    """
    converts the streams list to dictionary of streams where the keys are the tap stream ids
    Args:
        streams: stream list

    Returns: dictionary od streams

    """
    return {stream['tap_stream_id']: stream for stream in streams}


def filter_streams_by_replication_method(streams_to_sync: List[Dict], replication_method: str) -> Tuple[List[Dict], List[Dict]]:
    """
    Divides the list of streams into two lists: one of streams that use log based and the other that use
    traditional replication method, i.e Full table
    Args:
        streams_to_sync: List of streams selected to sync
        replication_method: replication method
    Returns: Tuple of two lists, first is log based streams and the second is list of traditional streams

    """
    log_based_streams = []
    non_log_based_streams = []

    for stream in streams_to_sync:
        if replication_method == 'LOG_BASED':
            log_based_streams.append(stream)
            non_log_based_streams.append(stream)
        elif is_log_based_stream(stream, replication_method):
            log_based_streams.append(stream)
        else:
            non_log_based_streams.append(stream)

    return log_based_streams, non_log_based_streams


def get_streams_to_sync(streams: List[Dict], state: Dict) -> List:
    """
    Filter the streams list to return only those selected for sync
    Args:
        streams: list of all discovered streams
        state: streams state

    Returns: list of selected streams, ordered from streams without state to those with state

    """
    # get selected streams
    selected_streams = [stream for stream in streams if is_stream_selected(stream)]

    # prioritize streams that have not been processed
    streams_with_state = []
    streams_without_state = []

    for stream in selected_streams:
        if state.get('bookmarks', {}).get(stream['tap_stream_id']):
            streams_with_state.append(stream)
        else:
            streams_without_state.append(stream)

    ordered_streams = streams_without_state + streams_with_state

    if not (currently_syncing := singer.get_currently_syncing(state)):
        return ordered_streams

    currently_syncing_stream = list(filter(
        lambda s: s['tap_stream_id'] == currently_syncing,
        ordered_streams))
    non_currently_syncing_streams = list(filter(lambda s: s['tap_stream_id'] != currently_syncing, ordered_streams))

    return currently_syncing_stream + non_currently_syncing_streams


def produce_collection_schema(collection: Collection) -> Dict:
    """
    Generate a schema/catalog from the collection details for discovery mode
    Args:
        collection: stream Collection

    Returns: collection catalog

    """
    collection_name = collection.name
    collection_db_name = collection.database.name

    is_view = collection.options().get('viewOn') is not None

    mdata = {}
    mdata = metadata.write(mdata, (), 'table-key-properties', ['_id'])
    mdata = metadata.write(mdata, (), 'database-name', collection_db_name)
    mdata = metadata.write(mdata, (), 'row-count', collection.estimated_document_count())
    mdata = metadata.write(mdata, (), 'is-view', is_view)

    return {
        'table_name': collection_name,
        'stream': collection_name,
        'metadata': metadata.to_list(mdata),
        'tap_stream_id': f"{collection_db_name}-{collection_name}",
        'schema': {
            'type': 'object',
            'properties': {
                "_id": {
                    "type": ["string", "null"]
                },
                "document": {
                    "type": [
                        "object",
                        "array",
                        "string",
                        "null"
                    ]
                },
                "_sdc_deleted_at": {
                    "type": [
                        "string",
                        "null"
                    ]
                },
            },
        }
    }


def get_attribute_type(source_type: str) -> SchemaAttributeType:
    if source_type == 'string':
        return SchemaAttributeType.STRING
    elif source_type == 'integer':
        return SchemaAttributeType.LONG
    elif source_type == 'boolean':
        return SchemaAttributeType.BOOLEAN
    elif source_type == 'number':
        return SchemaAttributeType.DOUBLE
    else:
        return SchemaAttributeType.OBJECT
