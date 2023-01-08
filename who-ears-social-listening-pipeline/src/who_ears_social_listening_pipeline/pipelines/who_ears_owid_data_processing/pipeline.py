from kedro.pipeline import Pipeline, node, pipeline
from .nodes import merge_data, update_column_names_from_mapping


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
    ])
