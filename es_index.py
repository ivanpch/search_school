import argparse
from datetime import datetime
import uuid

import elasticsearch
from elasticsearch import helpers
import pandas as pd


def read_csv(csv_delimiter: str, csv_path: str) -> 'pd.DataFrame':
    """
    Reads CSV file in `csv_path` with specified `csv_delimiter`.
    Rename columns: lowercase, replace spaces with underscores.

    Args:
        csv_delimiter: CSV delimiter.
        csv_path: path to CSV file.

    Returns:
        CSV dataframe.
    """

    csv_df = pd.read_csv(csv_path, delimiter=csv_delimiter)
    csv_df.rename(
        columns={
            column: column.strip().replace(' ', '_').lower()
            for column in csv_df.columns
        },
        inplace=True
    )
    return csv_df


def generate_docs(csv_df: 'pd.DataFrame', es_index: str) -> dict:
    """
    Docs generator for ES bulk helper.

    Args:
        csv_df: CSV dataframe.
        es_index: name of Elasticsearch index.

    Returns:
        single ES document at a time.
    """

    for _, row in csv_df.iterrows():
        doc = {
            '_id': uuid.uuid4().hex,
            '_index': es_index,
            '_source': {
                'timestamp': datetime.now(),
                **row.to_dict(),
            },
        }
        yield doc


def create_index(csv_df: 'pd.DataFrame', es_host: str, es_index: str) -> None:
    """
    Update specified `es_index` with `csv_df` data.

    Args:
        csv_df: CSV dataframe.
        es_host: Elasticsearch server address.
        es_index: name of Elasticsearch index.
    """

    es = elasticsearch.Elasticsearch(es_host)
    res = helpers.bulk(es, generate_docs(csv_df, es_index))
    print(f'Documents ingested: {res[0]}')


def main():
    parser = argparse.ArgumentParser(description='ES indexer for simple CSV files.')
    parser.add_argument('--es-index', type=str, required=True, help='ES index name.')
    parser.add_argument('--es-host', type=str, default='http://localhost:9200', help='ES host.')
    parser.add_argument('--csv-delimiter', type=str, default=';',
                        help='Delimiter to parse CSV correctly.')
    parser.add_argument('--csv-path', type=str, required=True, help='Path to CSV file.')
    cmd_args = parser.parse_args()
    csv_df = read_csv(cmd_args.csv_delimiter, cmd_args.csv_path)
    create_index(csv_df, cmd_args.es_host, cmd_args.es_index)


if __name__ == '__main__':
    main()
