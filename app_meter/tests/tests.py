import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ..services.readings_service import ReadingsProcessor
from ..models import Meter, Resource, Unit


class ReadingsProcessorTest(TestCase):
    def test_create_unit(self):
        unit = Unit.objects.create(name='kWh')
        expected_data = {
            'name': 'kWh'
        }
        self.assertEqual(expected_data['name'], unit.name)

    def test_create_resource(self):
        unit = Resource.objects.create(name='Water')
        expected_data = {
            'name': 'Water'
        }
        self.assertEqual(expected_data['name'], unit.name)

    def test_create_meter(self):
        unit = Unit.objects.create(name='m3')
        resource = Resource.objects.create(name='Gas')
        meter = Meter.objects.create(
            unit=unit,
            resource=resource,
            name='test_meter'
        )

        expected_data = {
            'name': 'test_meter',
            'unit': 'm3',
            'resource': 'Gas'
        }

        self.assertEqual(expected_data['name'], meter.name)
        self.assertEqual(expected_data['unit'], meter.unit.name)
        self.assertEqual(expected_data['resource'], meter.resource.name)

    def test_delete_meter(self):
        unit = Unit.objects.create(name='m3')
        resource = Resource.objects.create(name='Gas')
        meter = Meter.objects.create(
            unit=unit,
            resource=resource,
            name='test_meter'
        )
        meter.delete()
        num_meters = len(Meter.objects.all())
        self.assertEqual(0, num_meters)

    def test_create_readings(self):
        path = os.path.dirname(os.path.realpath(__file__))
        data = open(f'{path}\\readings_1.csv', 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        unit = Unit.objects.create(name='m3')
        resource = Resource.objects.create(name='Gas')
        meter = Meter.objects.create(
            unit=unit,
            resource=resource,
            name='test_meter'
        )

        processor_obj = ReadingsProcessor(
            csv_file=data,
            meter_pk=meter.id
        )
        processor_obj.save_data()
        readings = meter.readings.all()
        expected_data = [
            {
                'absolute_value': 9000,
                'relative_value': 0,
                'date': '2013-12-16'
            },
            {
                'absolute_value': 9100,
                'relative_value': 100,
                'date': '2013-12-24'

            },
            {
                'absolute_value': 9250,
                'relative_value': 150,
                'date': '2013-12-30'
            }
        ]
        self.assertEqual(
            expected_data[0]['absolute_value'],
            readings[0].absolute_value
        )
        self.assertEqual(
            expected_data[0]['relative_value'],
            readings[0].relative_value
        )
        self.assertEqual(
            expected_data[0]['date'],
            readings[0].date.strftime("%Y-%m-%d")
        )
        self.assertEqual(
            expected_data[1]['absolute_value'],
            readings[1].absolute_value
        )
        self.assertEqual(
            expected_data[1]['relative_value'],
            readings[1].relative_value
        )
        self.assertEqual(
            expected_data[1]['date'],
            readings[1].date.strftime("%Y-%m-%d")
        )
        self.assertEqual(
            expected_data[2]['absolute_value'],
            readings[2].absolute_value
        )
        self.assertEqual(
            expected_data[2]['relative_value'],
            readings[2].relative_value
        )
        self.assertEqual(
            expected_data[2]['date'],
            readings[2].date.strftime("%Y-%m-%d")
        )

    def test_delete_readings(self):
        path = os.path.dirname(os.path.realpath(__file__))
        data = open(f'{path}\\readings_1.csv', 'rb')
        data = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        unit = Unit.objects.create(name='m3')
        resource = Resource.objects.create(name='Gas')
        meter = Meter.objects.create(
            unit=unit,
            resource=resource,
            name='test_meter'
        )
        processor_obj = ReadingsProcessor(csv_file=data, meter_pk=meter.id)

        processor_obj.save_data()
        meter.readings.all().delete()

        num_readings = len(meter.readings.all())
        self.assertEqual(0, num_readings)

    def test_update_readings(self):
        path = os.path.dirname(os.path.realpath(__file__))
        data = open(f'{path}\\readings_1.csv', 'rb')
        data_1 = SimpleUploadedFile(
            content=data.read(),
            name=data.name,
            content_type='multipart/form-data'
        )

        unit = Unit.objects.create(name='m3')
        resource = Resource.objects.create(name='Gas')
        meter = Meter.objects.create(
            unit=unit,
            resource=resource,
            name='test_meter'
        )
        # Saving original readings
        processor_obj = ReadingsProcessor(csv_file=data_1, meter_pk=meter.id)
        processor_obj.save_data()

        data_2 = open(f'{path}\\readings_2.csv', 'rb')
        data_2 = SimpleUploadedFile(
            content=data_2.read(),
            name=data_2.name,
            content_type='multipart/form-data'
        )
        # Rewrite exist readings
        processor_obj_2 = ReadingsProcessor(csv_file=data_2, meter_pk=meter.id)
        processor_obj_2.save_data()

        expected_data = [
            {
                'absolute_value': 10000,
                'relative_value': 0,
                'date': '2013-12-16'
            },
            {
                'absolute_value': 10500,
                'relative_value': 500,
                'date': '2013-12-24'

            },
            {
                'absolute_value': 10789,
                'relative_value': 289,
                'date': '2013-12-30'
            }
        ]
        readings = meter.readings.all()

        self.assertEqual(
            expected_data[0]['absolute_value'],
            readings[0].absolute_value
        )
        self.assertEqual(
            expected_data[0]['relative_value'],
            readings[0].relative_value
        )
        self.assertEqual(
            expected_data[0]['date'],
            readings[0].date.strftime("%Y-%m-%d")
        )
        self.assertEqual(
            expected_data[1]['absolute_value'],
            readings[1].absolute_value
        )
        self.assertEqual(
            expected_data[1]['relative_value'],
            readings[1].relative_value
        )
        self.assertEqual(
            expected_data[1]['date'],
            readings[1].date.strftime("%Y-%m-%d")
        )
        self.assertEqual(
            expected_data[2]['absolute_value'],
            readings[2].absolute_value
        )
        self.assertEqual(
            expected_data[2]['relative_value'],
            readings[2].relative_value
        )
        self.assertEqual(
            expected_data[2]['date'],
            readings[2].date.strftime("%Y-%m-%d")
        )

    def test_add_readings_in_batches(self):
        #Loading the first batch of readings
        path = os.path.dirname(os.path.realpath(__file__))
        data_1 = open(f'{path}\\readings_1.csv', 'rb')
        data_1 = SimpleUploadedFile(
            content=data_1.read(),
            name=data_1.name,
            content_type='multipart/form-data'
        )

        unit = Unit.objects.create(name='m3')
        resource = Resource.objects.create(name='Gas')
        meter = Meter.objects.create(
            unit=unit,
            resource=resource,
            name='test_meter'
        )

        processor_obj = ReadingsProcessor(
            csv_file=data_1,
            meter_pk=meter.id
        )
        processor_obj.save_data()

        # Loading the second batch of readings
        data_2 = open(f'{path}\\readings_3.csv', 'rb')
        data_2 = SimpleUploadedFile(
            content=data_2.read(),
            name=data_2.name,
            content_type='multipart/form-data'
        )

        processor_obj_2 = ReadingsProcessor(
            csv_file=data_2,
            meter_pk=meter.id
        )
        processor_obj_2.save_data()

        expected_data = [
            {
                'absolute_value': 9000,
                'relative_value': 0,
                'date': '2013-12-16'
            },
            {
                'absolute_value': 9100,
                'relative_value': 100,
                'date': '2013-12-24'

            },
            {
                'absolute_value': 9250,
                'relative_value': 150,
                'date': '2013-12-30'
            },
            {
                'absolute_value': 9523,
                'relative_value': 273,
                'date': '2014-10-31'
            },
            {
                'absolute_value': 9603,
                'relative_value': 80,
                'date': '2014-12-01'

            },
            {
                'absolute_value': 9703,
                'relative_value': 100,
                'date': '2014-12-31'
            },

        ]
        # Old and new readings
        readings = meter.readings.all()


        self.assertEqual(
            expected_data[0]['absolute_value'],
            readings[0].absolute_value
        )
        self.assertEqual(
            expected_data[0]['relative_value'],
            readings[0].relative_value
        )
        self.assertEqual(
            expected_data[0]['date'],
            readings[0].date.strftime("%Y-%m-%d")
        )
        self.assertEqual(
            expected_data[1]['absolute_value'],
            readings[1].absolute_value
        )
        self.assertEqual(
            expected_data[1]['relative_value'],
            readings[1].relative_value
        )
        self.assertEqual(
            expected_data[1]['date'],
            readings[1].date.strftime("%Y-%m-%d")
        )
        self.assertEqual(
            expected_data[2]['absolute_value'],
            readings[2].absolute_value
        )
        self.assertEqual(
            expected_data[2]['relative_value'],
            readings[2].relative_value
        )
        self.assertEqual(
            expected_data[2]['date'],
            readings[2].date.strftime("%Y-%m-%d")
        )
        self.assertEqual(
            expected_data[3]['absolute_value'],
            readings[3].absolute_value
        )
        self.assertEqual(
            expected_data[3]['relative_value'],
            readings[3].relative_value
        )
        self.assertEqual(
            expected_data[3]['date'],
            readings[3].date.strftime("%Y-%m-%d")
        )
        self.assertEqual(
            expected_data[4]['absolute_value'],
            readings[4].absolute_value
        )
        self.assertEqual(
            expected_data[4]['relative_value'],
            readings[4].relative_value
        )
        self.assertEqual(
            expected_data[4]['date'],
            readings[4].date.strftime("%Y-%m-%d")
        )
        self.assertEqual(
            expected_data[5]['absolute_value'],
            readings[5].absolute_value
        )
        self.assertEqual(
            expected_data[5]['relative_value'],
            readings[5].relative_value
        )
        self.assertEqual(
            expected_data[5]['date'],
            readings[5].date.strftime("%Y-%m-%d")
        )
