import argparse
from datetime import datetime
import uuid

import elasticsearch
import pandas as pd


def read_csv(csv_delimiter: str, csv_path: str) -> 'pd.DataFrame':
    """
    Reads CSV file in `csv_path` with specified `csv_delimiter`.

    Args:
        csv_delimiter: CSV delimiter.
        csv_path: path to CSV file.

    Returns:
        CSV dataframe.
    """

    csv_df = pd.read_csv(csv_path, delimiter=csv_delimiter)
    return csv_df


def create_index(csv_df: 'pd.DataFrame', es_host: str, es_index: str) -> None:
    """
    Update specified `es_index` with `csv_df` data.

    Args:
        csv_df: CSV dataframe.
        es_host: Elasticsearch server address.
        es_index: name of Elasticsearch index.
    """

    es = elasticsearch.Elasticsearch(es_host)
    for idx in range(csv_df.shape[0]):
        es_doc = {
            'timestamp': datetime.now(),
        }
        row = csv_df.iloc[idx]
        es_doc.update(**{
            column_name.strip().lower(): row[column_name]
            for column_name in csv_df.columns
        })
        doc_id = uuid.uuid4().hex
        res = es.index(index=es_index, id=doc_id, document=es_doc)
        print(f'Indexing doc with id {doc_id}: {res["result"]}')


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
