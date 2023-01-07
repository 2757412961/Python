import os
import config
import datetime
import cdsapi

c = cdsapi.Client(url="https://cds.climate.copernicus.eu/api/v2", key="169125:7b21c9c3-8506-4293-b04d-66d069ed143f")

if __name__ == '__main__':
    begin = datetime.date(2003, 1, 1)
    end = datetime.date(2022, 1, 1)
    base_dir = config.DATA_ROOT + "/ERA5"

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for i in range((end - begin).days + 1):
        time = begin + datetime.timedelta(days=i)
        year = time.strftime("%Y")  # 2003
        month = time.strftime("%m")  # 01
        day = time.strftime("%d")  # 01
        print(time)
        if os.path.exists(f'{base_dir}/ERA5_hourly_{year}{month}{day}.nc'):
            continue
        c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'variable': [
                    '10m_u_component_of_wind', '10m_v_component_of_wind', 'mean_sea_level_pressure',
                    'sea_surface_temperature', 'total_precipitation',
                ],
                'year': [year],
                'month': [month],
                'day': [day],
                'time': '12:00',
                'format': 'netcdf',
            },
            f'{base_dir}/ERA5_hourly_{year}{month}{day}.nc')

'''
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'variable': [
            '10m_u_component_of_wind', '10m_v_component_of_wind', 'mean_sea_level_pressure',
            'sea_surface_temperature', 'total_precipitation',
        ],
        'year': [
            '2019', '2020',
        ],
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
        'time': '12:00',
        'format': 'netcdf',
    },
    'download.nc')
'''
