import io
import pandas as pd
from .. import models

# TODO написать логику сохранения df в базу
def save_data(df, meter_pk):
    """
    Iterates over the dataframe and generates models for writing to the database
    """
    meter_instance = models.Meter.objects.get(id=meter_pk)
    # TODO доработать логику для удаления старых показаний или для наложения новых показаний на старые
    readings = []
    for row in df.T.to_dict().values():
        row['meter'] = meter_instance
        readings.append(models.Readings(**row))

    models.Readings.objects.bulk_create(readings)


def parse_data(**kwargs):
    """
    Accepts an input file with readings and prepares it for writing to the database
    """
    file = io.TextIOWrapper(kwargs['csv_file'].file)
    df = pd.read_csv(file, sep=',', parse_dates=['DATE'])

    new_df = pd.DataFrame()
    new_df['absolute_value'] = df['VALUE'].astype(int)
    new_df['date'] = df['DATE']
    new_df = new_df.sort_values(by='date')
    new_df['relative_value'] = new_df['absolute_value'].diff().fillna(0)
    new_df['relative_value'] = new_df['relative_value'].astype(int)

    return new_df