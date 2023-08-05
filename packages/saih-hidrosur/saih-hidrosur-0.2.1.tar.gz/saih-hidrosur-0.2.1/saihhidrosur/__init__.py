import csv
import datetime
import io
import os

import requests

class APIClient:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://www.redhidrosurmedioambiente.es',
        'Connection': 'keep-alive',
        'Referer': 'http://www.redhidrosurmedioambiente.es/saih/datos/a/la/carta',
    }

    root_url = 'http://www.redhidrosurmedioambiente.es/'

    def __init__(self):
        if 'SAIH_CACHE' in os.environ:
            # Warning, do not cache in prod, as you may not get the latest values
            import requests_cache
            self.session = requests_cache.CachedSession('cache')
        else:
            self.session = requests.Session()

    def post(self, url: str, data: dict = {}):
        return self.session.post(self.root_url + url, headers=self.headers, data=data)
    def get(self, url: str, data: dict = {}, params: dict = {}):
        return self.session.get(self.root_url + url, headers=self.headers, data=data, params=params)


class Station:
    RESAMPLINGS = {
        # WUUT ‽
        'hourly': 60,
        'daily': 1,
        'weekly': 7,
        'monthly': 31,
        '5-mins': 5,
    }
    TIME_FMT = "%d/%m/%Y %H:%M"
    TIME_FMT_FALLBACK = "%d/%m/%y %H:%M"

    def __init__(self, id: int, api_client: APIClient = None):
        self.id = id
        if not api_client:
            api_client = APIClient()
        self.api_client = api_client

        self._get_infos()

    def __repr__(self):
        return f'<{self.name} with sensors {list(self.sensors.keys())}>'

    def _get_infos(self):
        data = {
            'subsistema': '',
            'provincia': '',
            'tipoestacion': '',
            'estacion': str(self.id),
            'tipo': '',
            'sensor': '',
        }

        r = self.api_client.get('saih/datos/a/la/carta/parametros', data)
        dq = r.json()[str(self.id)]
        self.name = dq['nombre']

        sensor_names = dq['nombres']
        sensor_ids = dq['sensores']

        sensor_dict = dict(zip(sensor_names, sensor_ids))  # {'TEMPERATURA EXTERIOR': '051M02', 'NIVOMETRO': '051N02', 'PLUVIOMETRO': '051P01'}
        self.sensors = sensor_dict


    @staticmethod
    def _parse_csv_output(csvtxt: str, sensor_id: str) -> dict[datetime.datetime, float]:

        sensor_type = sensor_id[-3] # M, N, P
        value_column = {
            'D': 5,  # Water level (mm)
            'E': 5,  # Water capacity (hm³) via Balanza
            'L': 5,  # Water capacity (hm³) via Gauge / Limnímetro
            'M': 4,  # Temp exterior (°C)
            'N': 5,  # Nivometro (l/m²)
            'P': 5,  # Pluviometro (l/m²)
            'R': 4,  # Nivel del rio (m)
        }[sensor_type]



        csvf = io.StringIO(csvtxt.replace('\r', '\r\n'))

        sr = csv.reader(csvf, delimiter=';')
        head = next(sr)
        sensor_column = head.index('Sensor')
        date_column = head.index('Fecha')

        results = {}
        for row in sr:
            sensor = row[sensor_column]
            if sensor != sensor_id:
                continue

            sdate = row[date_column]
            try:
                date = datetime.datetime.strptime(sdate, Station.TIME_FMT)
            except ValueError:
                # What a consistent API…
                date = datetime.datetime.strptime(sdate, Station.TIME_FMT_FALLBACK)

            svalue = row[value_column]
            if svalue == 'n/d':
                value = float('NaN')
            else:
                value = float(svalue.replace(',', '.'))

            results[date] = value

        return results


    def sensor_values(self, sensor_name: str, date_from: datetime.datetime, date_to: datetime.datetime) -> dict[datetime.datetime, float]:
        """
        Returns a {datetime: float} dict for each value between date_from and date_to
        """

        sensor_id = self.sensors[sensor_name]
        date_start = date_from.strftime(self.TIME_FMT)
        date_end = date_to.strftime(self.TIME_FMT)

        params = {
            'datepickerini': date_start,
            'datepickerfin': date_end,
            'agrupacion': self.RESAMPLINGS['hourly'],
            'subsistema': '',
            'provincia': '',
            'tipoestacion': '',
            'estacion': self.id,
            'sensor': sensor_id,
        }

        print(params)


        r = self.api_client.get('saih/datos/a/la/carta/csv', params=params)
        csvtxt = r.content.decode('utf-8')

        if 'Error_404' in csvtxt:
            # why you no return 404 instead ‽
            return {}

        if r.content == b'':
            return {}

        return Station._parse_csv_output(csvtxt, sensor_id)



def get_stations() -> list[Station]:
    """ Returns the list of stations"""
    a = APIClient()
    sts = a.get('saih/datos/a/la/carta/parametros').json()
    return {int(key): val['nombre'] for key, val in sts.items()}
