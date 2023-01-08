from kedro.pipeline import Pipeline, node, pipeline
from .nodes import merge_data, update_column_names_from_mapping, merge_who_ears_owid_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=merge_data,
            inputs="raw_daily_who_ears",
            outputs="merged_daily_who_ears",
            name="merge_who_ears_partitions",
        ),
        node(
            func=update_column_names_from_mapping,
            inputs=["who_ears_doc_mapping", "merged_daily_who_ears"],
            outputs="processed_daily_who_ears",
            name="update_column_names_from_mapping",
        ),
        node(
            func=merge_who_ears_owid_data,
            inputs=["processed_daily_who_ears", "raw_daily_owid"],
            outputs="merge_who_ears_owid_data",
            name="merge_who_ears_owid_data",
        ),
    ])
