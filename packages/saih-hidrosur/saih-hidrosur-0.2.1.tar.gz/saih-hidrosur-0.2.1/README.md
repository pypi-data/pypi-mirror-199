python-saih-hidrosur
==========================


## What is this lib ?
Python library around [S.A.I.H Hidrosur](http://www.redhidrosurmedioambiente.es/saih/) data

## How to install the lib ?
You can get it from [pypi](https://pypi.org/project/saih-hidrosur/) like so:
```
pip3 install saih-hidrosur
```

## How to use the lib
```python3
>>> import datetime
>>> from pprint import pprint as pprint
>>> from saihhidrosur import get_stations, Station

>>> pprint(get_stations())
{1: 'SIERRA MIJAS  (MA)',
 2: 'SIERRA DE LUNA (CA)',
 3: 'EMBALSE DE CHARCO REDONDO (CA)',
 4: 'DEPÓSITO REGULADOR CHARCO RDO (CA)',
 5: 'TORRE TOMA DE CHARCO REDONDO (CA)',
 6: 'LOS REALES (MA)',
 7: 'DEPÓSITO DI-1 (CA)',
 8: 'EMBALSE DE GUADARRANQUE (CA)',
 ...}


>>> murtas = Station(59)
>>> murtas
<MURTAS (GR) with sensors ['TEMPERATURA EXTERIOR', 'NIVOMETRO', 'PLUVIOMETRO']>

>>> murtas.sensors
{'NIVOMETRO': '059N02',
 'PLUVIOMETRO': '059P01',
 'TEMPERATURA EXTERIOR': '059M02'}

>>> date_from = datetime.datetime(2022, 1, 1)
>>> date_to = datetime.datetime(2022, 1, 2)
>>> murtas.sensor_values('TEMPERATURA EXTERIOR', date_from, date_to)
{datetime.datetime(2022, 10, 1, 0, 0): 15.2,
 datetime.datetime(2022, 10, 1, 1, 0): 14.7,
 …
 datetime.datetime(2022, 10, 1, 23, 0): 17.0,
 datetime.datetime(2022, 10, 2, 0, 0): 16.6}


```
