import io
import pandas as pd
from .. import models


class ReadingsProcessor:
    def __init__(self, csv_file, meter_pk):
        self.csv_file = csv_file
        self.meter_pk = meter_pk
        self.last_readings = models.Readings.objects.filter(
            meter=self.meter_pk
        ).last()
        self.df = None

    # TODO написать логику сохранения df в базу
    def save_data(self) -> None:
        """
        Iterates over the dataframe and generates models for writing to the database
        """
        # Preparing CSV for recording in the database
        self.parse_data(csv_file=self.csv_file)
        meter_instance = models.Meter.objects.get(id=self.meter_pk)

        # Formation of objects for writing to the database
        readings = []
        for row in self.df.T.to_dict().values():
            row['meter'] = meter_instance
            readings.append(models.Readings(**row))

        models.Readings.objects.bulk_create(readings)
        # TODO обработать исключение при невозможности записи из-за дублирования

    def parse_data(self, **kwargs) -> None:
        """
        Accepts an input file with readings and prepares it for writing to the database
        """
        file = io.TextIOWrapper(kwargs['csv_file'].file)
        df = pd.read_csv(file, sep=',', parse_dates=['DATE'])
        new_df = pd.DataFrame()
        new_df['absolute_value'] = df['VALUE'].astype(int)
        new_df['date'] = df['DATE']
        new_df = new_df.sort_values(by='date')

        # Adding a column of relative resource consumption values
        new_df['relative_value'] = new_df['absolute_value'].diff()

        # Logic for linking previous and next readings
        if self.last_readings:
            last_next_diff = new_df.iloc[0]['absolute_value'] - self.last_readings.absolute_value
            new_df.loc[new_df.index[0], 'relative_value'] = last_next_diff

        new_df['relative_value'] = new_df['relative_value'].fillna(0)
        new_df['relative_value'] = new_df['relative_value'].astype(int)

        self.df = new_df
