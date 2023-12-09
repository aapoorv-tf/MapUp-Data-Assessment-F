import pandas as pd
import numpy as np

def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    df = df.pivot(index = "id_1", columns = "id_2", values = "car")
    np.fill_diagonal(df.values, 0)

    return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here

    df['car_type'] = pd.cut(df['car'], bins=[0, 15, 25, np.inf], labels=['low', 'medium', 'high'])
    result = df['car_type'].value_counts().to_dict()
    result = dict(sorted(result.items()))
    return result
    


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    mean = df['bus'].mean()
    result = df[df['bus'] > 2 * mean].index.tolist()
    return result
    


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    result = df.groupby('route')['truck'].mean().reset_index()
    result = sorted(result[result['truck'] > 7]['route'].tolist())
    
    return result



def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    matrix[matrix > 20] *= 0.75
    matrix[matrix <= 20] *= 1.25
    return matrix
    


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['start'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime']) #throws error, outofbounds for pd.to_datetime
    df['end'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    df['duration'] = df['end'] - df['start']
    grouped = df.groupby(['id', 'id_2'])

    result = grouped.apply(lambda x: (x['duration'].min() <= pd.Timedelta(days=6, hours=23, minutes=59, seconds=59)) & (x['duration'].max() >= pd.Timedelta(days=7)))
    result.index.names = ['id', 'id_2']
    return result
