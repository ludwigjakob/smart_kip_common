from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from common.data_connector.base_connector import BaseConnector
import os
from dotenv import load_dotenv
import pandas as pd

# .env-Datei laden, damit os.getenv() funktioniert
load_dotenv()

class TemperatureConnector(BaseConnector):
    def __init__(self, name="debo_temp_1", bucket="None"):
        # Bucket aus ENV übernehmen, falls nicht explizit gesetzt
        bucket = bucket or os.getenv("INFLUX_BUCKET")
        super().__init__(name, bucket)
        
        # Umgebungsvariablen laden
        influx_url = os.getenv("INFLUX_URL")
        influx_token = os.getenv("INFLUX_TOKEN")
        influx_org = os.getenv("INFLUX_ORG")
        self.org = influx_org

        # Optional: Debug-Ausgabe zur Kontrolle
        if not all([influx_url, influx_token, influx_org]):
            raise ValueError("Fehlende InfluxDB-Konfiguration in .env")

        self.client = InfluxDBClient(
            url=influx_url,
            token=influx_token,
            org=influx_org
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)


    def read(self):
        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: -1h)
          |> filter(fn: (r) => r._measurement == "temperature")
          |> filter(fn: (r) => r.sensor == "{self.name}")
          |> last()
        '''
        result = self.client.query_api().query(query)
        for table in result:
            for record in table.records:
                return round(record.get_value(), 2)
        return None

    def write(self, data: dict):
        point = (
            Point(data["type"])
            .tag("sensor", data["sensor"])
            .field("value", data["value"])
        )
        self.write_api.write(bucket=self.bucket, org=self.org, record=point)

    def read_trainingdata_7_days_df(self):
        query = f'''
        from(bucket: "training_data")
        |> range(start: -7d)
        |> filter(fn: (r) => r._measurement == "temperature" or r._measurement == "fan_status")
        |> filter(fn: (r) => r.sensor == "{self.name}")
        |> filter(fn: (r) => r._field == "value")
        |> keep(columns: ["_time", "_value", "_measurement"])
        '''
        result = self.client.query_api().query(query)

        records = []
        for table in result:
            for record in table.records:
                records.append({
                    "time": record.get_time(),
                    "measurement": record.get_measurement(),
                    "value": round(record.get_value(), 2)
                })

        df = pd.DataFrame(records)
        df.set_index("time", inplace=True)

        # Pivotieren: Spalten für temperature und fan_status
        df = df.pivot(columns="measurement", values="value")

        return df
