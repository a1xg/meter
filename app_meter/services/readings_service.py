import io
import pandas as pd
from .. import models


class ReadingsProcessor:
    def __init__(self, csv_file, meter_pk):
        self.csv_file = csv_file
        self.meter_pk = meter_pk
        self.exist_readings = models.Readings.objects.filter(meter=self.meter_pk)

        self.df = None

    def save_data(self) -> None:
        """
        Iterates over the dataframe and generates models for writing to the database
        """
        # Preparing CSV for recording in the database
        self._parse_data(csv_file=self.csv_file)
        self._old_new_readings_diff()
        self._create_or_update()

    def _old_new_readings_diff(self):
        """Extract the interval of existing records from the earliest to the record
        on the date of the first element of new indications, in order to
        correlate old and new indications"""
        if self.exist_readings:
            interval_exist_readings = self.exist_readings.filter(
                date__range=[self.exist_readings.first().date, self.df.iloc[0]['date']]
            )
            readings_list = list(interval_exist_readings)
            if len(readings_list) >= 2:
                prev_readings = readings_list[-2].absolute_value
                last_next_diff = self.df.iloc[0]['absolute_value'] - prev_readings
                self.df.loc[self.df.index[0], 'relative_value'] = last_next_diff

    def _create_or_update(self) -> None:
        """Creates new or updates old records based on the date of reporting"""
        meter_instance = models.Meter.objects.get(id=self.meter_pk)
        readings_to_update = []
        readings_to_create = []

        for row in self.df.T.to_dict().values():
            row['meter'] = meter_instance
            exist_row = self.exist_readings.filter(date=row['date']).first()
            if exist_row:
                exist_row.absolute_value = row['absolute_value']
                exist_row.relative_value = row['relative_value']
                readings_to_update.append(exist_row)

            if not exist_row:
                readings_to_create.append(models.Readings(**row))

        if readings_to_create:
            models.Readings.objects.bulk_create(readings_to_create)
        if readings_to_update:
            models.Readings.objects.bulk_update(readings_to_update, ['relative_value', 'absolute_value'])

    def _parse_data(self, **kwargs) -> None:
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

        new_df['relative_value'] = new_df['relative_value'].fillna(0)
        new_df['relative_value'] = new_df['relative_value'].astype(int)

        self.df = new_df
