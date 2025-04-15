import json
from agents import Agent, function_tool
import pandas as pd
import typing as t

POSSIBLE_AGGREGATES = ["sum", "max","min", "median","mean"]
STR_POS_AGG = {",".join([f"`{n}`" for n in POSSIBLE_AGGREGATES])}
def agg(grouped_df, agg_func):
    if agg_func == 'sum':
        return grouped_df.sum().reset_index()
    elif agg_func == 'mean':
        return grouped_df.mean().reset_index()
    elif agg_func == 'median':
        return grouped_df.median().reset_index()
    elif agg_func == 'max':
        return grouped_df.max().reset_index()
    elif agg_func == 'min':
        return grouped_df.min().reset_index()
    else:
        raise ValueError(f"Неизвестная агрегирующая функция: {agg_func}")

@function_tool(strict_mode=False)
async def summary_up_csv(content: str, group_aggregates: t.Dict[str, t.List[str]]) -> str:
    f"""
    Reads the csv file with `pandas.read_csv(content)` and then 
    for each group in `group_aggregates` try to group the data in 
    the csv by given column name (the dict key) 
    and calculate each aggregate function from `group_aggregates` value.
    Aggregate function may be one of: {STR_POS_AGG}.
    Unknown aggregate functions will be ignored and not calculated.

    Returns the dict where key is the key from `group_aggregates` joined 
    by undescore the name of aggregation funcion.
    The value is the appropriate calculated value for that key.

    E.g. if we have a csv like:
    customer,country,income
    Freddy,USA,5000
    Dima,RUS,1000
    Maria,USA,1000
    
    and we call this funtion with `group_aggregates` 
    `dict(country=["sum","mean"])` that the output will be:
    ```
    {
        "USA_sum": 6000,
        "RUS_sum": 1000,
        "USA_mean": 3000,
        "RUS_mean": 1000
    }

    Args:
        content (str): The CSV file content as a string.
        group_aggregates (Dict[str, List[str]]): A dictionary where the keys 
        are column names to group by and the values are lists of aggregate 
        functions to calculate on each group.

    Returns:
        str: A JSON string containing the results of the aggregation.
    ```
    
    """
    df = pd.read_csv(content)
    output = {}
    for column, aggregates in group_aggregates.items():
        group = df.groupby(column)
        for aggregate in aggregates:
            value = agg(group, aggregate)
            output[column + "_" + aggregate] = value
    return json.dumps(output)

csv_agent = Agent(
    name="CSV Summarizer",
    instructions=f"You will summarize CSV to aggregate values. \
    You will get only csv file data as string and you need to \
    imagine which aggregates can be calculated on which fields \
    and then, using the tool summary_up_csv calculate those aggregates. \
    List of possible aggregates: {STR_POS_AGG}. Separate output json \
    from your thought by delimeter `------`.",
    model="o3-mini",
    tools=[summary_up_csv],
)
