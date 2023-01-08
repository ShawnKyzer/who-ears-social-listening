from re import sub

import pandas as pd
import pytest
import who_ears_social_listening_pipeline.pipelines.who_ears_owid_data_processing.nodes as nodes


def test_update_column_names_from_mapping():
    def to_snake_case(s):
        return '_'.join(sub('([A-Z][a-z]+)', r' \1',
                            sub('([A-Z]+)', r' \1',
                                s.replace('-', ' '))).split()).lower()

    # Set up test data
    who_ears_doc_mapping = pd.DataFrame({'doc_index': [1, 2, 3],
                                         'document_name': ['Test Doc 1', 'Test Doc 2', 'Test Doc 3']})
    who_ears_doc_mapping['document_name'] = who_ears_doc_mapping['document_name'].apply(to_snake_case)
    merged_daily_who_ears = pd.DataFrame({'col1-1': [1, 2, 3],
                                          'col2-2': [4, 5, 6],
                                          'col3-3': [7, 8, 9]})

    # Ensure original column names are correct
    expected_col_names = ['col1-1', 'col2-2', 'col3-3']
    assert list(merged_daily_who_ears.columns) == expected_col_names

    # Ensure returned DataFrame has the expected column names after running the function
    updated_df = nodes.update_column_names_from_mapping(who_ears_doc_mapping, merged_daily_who_ears)
    expected_col_names = ['test_doc_1', 'test_doc_2', 'test_doc_3']
    assert list(updated_df.columns) == expected_col_names
