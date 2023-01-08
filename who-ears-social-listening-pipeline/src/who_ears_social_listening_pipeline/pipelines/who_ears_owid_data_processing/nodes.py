from typing import Any, Callable, Dict
import pandas as pd
from datetime import timedelta, datetime as dt


def merge_data(partitioned_input: Dict[str, Callable[[], Any]]) -> pd.DataFrame:
    merged_df = pd.DataFrame()
    for partition_id, partition_load_func in sorted(partitioned_input.items()):
        partition_data = partition_load_func()  # Load partition data
        merged_df = pd.concat([merged_df, partition_data], ignore_index=True, sort=True)
    return merged_df


def update_column_names_from_mapping(who_ears_doc_mapping, merged_daily_who_ears):
    from re import sub

    def to_snake_case(s):
        return '_'.join(sub('([A-Z][a-z]+)', r' \1',
                            sub('([A-Z]+)', r' \1',
                                s.replace('-', ' '))).split()).lower()

    who_ears_doc_mapping['document_name'] = who_ears_doc_mapping['document_name'].apply(to_snake_case)

    for col_name in merged_daily_who_ears.columns:
        # Extract the index from the column name
        if len(col_name.split('-')) == 4:
            index = int(col_name.split('-')[3])
            suffix = '_' + col_name.split('-')[1]
            new_name = who_ears_doc_mapping.loc[who_ears_doc_mapping['doc_index'] == index, 'document_name'][index - 1]
            merged_daily_who_ears.rename(columns={col_name: new_name + suffix}, inplace=True)
        elif len(col_name.split('-')) > 2:
            index = int(col_name.split('-')[2])
            suffix = '_' + col_name.split('-')[1]
            new_name = who_ears_doc_mapping.loc[who_ears_doc_mapping['doc_index'] == index, 'document_name'][index - 1]
            merged_daily_who_ears.rename(columns={col_name: new_name + suffix}, inplace=True)
        elif len(col_name.split('-')) > 1:
            index = int(col_name.split('-')[1])
            suffix = ""
            new_name = who_ears_doc_mapping.loc[who_ears_doc_mapping['doc_index'] == index, 'document_name'][index - 1]
            merged_daily_who_ears.rename(columns={col_name: new_name + suffix}, inplace=True)
        else:
            continue

    return merged_daily_who_ears


def merge_who_ears_owid_data(processed_daily_who_ears, raw_daily_owid):
    # Left join on the two sets
    merged_owid_who_ears = pd.merge(processed_daily_who_ears, raw_daily_owid,
                                    how='left',
                                    left_on=['id', 'date'],
                                    right_on=['iso_code', 'date'])
    return merged_owid_who_ears
