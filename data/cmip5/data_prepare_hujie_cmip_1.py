"""
@Description:
input:  [1861-2001(141year),36month] = [1861-2003(143year),12month]
output: [1863-2003(141year),12month]
change input range to output range, thus
new input = output = [1863,2003(12month)] = 141*12 = 1692 month
"""

from netCDF4 import Dataset, num2date, date2num
import numpy as np
import datetime as dt

"""
Create new_cmip_input_nc_path netCDF file. 
"""
cmip_input_nc_path = 'I:/hujie/CMIP5.input.36mon.1861_2001.nc'
cmip_input_nc = Dataset(cmip_input_nc_path)

SST = cmip_input_nc.variables['sst1'][:]
T300 = cmip_input_nc.variables['t300'][:]
lat = cmip_input_nc.variables['lat'][:]
lon = cmip_input_nc.variables['lon'][:]

new_cmip_input_nc_path = 'I:/hujie/data/CMIP5_train_1.nc'
new_cmip_input_nc = Dataset(new_cmip_input_nc_path, 'w')

new_cmip_input_nc.createDimension('time', 1692)
new_cmip_input_nc.createDimension('lat', 24)
new_cmip_input_nc.createDimension('lon', 72)
new_cmip_input_nc.createVariable('time', 'd', ('time'))
new_cmip_input_nc.createVariable('lat', 'd', ('lat'))
new_cmip_input_nc.createVariable('lon', 'd', ('lon'))
new_cmip_input_nc.createVariable('sst', 'd', ('time', 'lat', 'lon'), fill_value=np.nan)
new_cmip_input_nc.createVariable('t300', 'd', ('time', 'lat', 'lon'), fill_value=np.nan)

time_list = []
for year in range(1863, 2003 + 1):
    for month in range(12):
        out_dt = dt.datetime(year=year, month=1 + month, day=1, hour=0, minute=0, second=0)
        out_time = date2num(out_dt, units="hours since 1850-01-01 00:00:00", calendar="standard")
        time_list.append(out_time)
time_list = np.array(time_list)
print(time_list)
print('time_list.shape', time_list.shape)

new_cmip_input_nc.variables['time'][:] = time_list
new_cmip_input_nc.variables['lat'][:] = lat
new_cmip_input_nc.variables['lon'][:] = lon
new_cmip_input_nc.variables['time'].units = "hours since 1850-01-01 00:00:00"
new_cmip_input_nc.variables['lat'].units = "degrees_north"
new_cmip_input_nc.variables['lon'].units = "degrees_east"

# start_index = 2
# end_index = 141

SST = SST[:141, :]
T300 = T300[:141, :]
print('SST.shape', SST.shape)
print('T300.shape', T300.shape)
for year_index in range(2, 143):
    for month_index in range(12):
        year = year_index + 1861
        month = month_index + 1
        time_dt = dt.datetime(year=year, month=month, day=1, hour=0, minute=0, second=0)
        time_dt_value = date2num(time_dt, units="hours since 1850-01-01 00:00:00", calendar="standard")
        time_index = np.where(time_list == time_dt_value)[0]
        if year_index == 141:
            new_cmip_input_nc.variables['sst'][time_index, :] = SST[140, 12 + month_index, :]
            new_cmip_input_nc.variables['t300'][time_index, :] = T300[140, 12 + month_index, :]
        elif year_index == 142:
            new_cmip_input_nc.variables['sst'][time_index, :] = SST[140, 24 + month_index, :]
            new_cmip_input_nc.variables['t300'][time_index, :] = T300[140, 24 + month_index, :]
        else:
            new_cmip_input_nc.variables['sst'][time_index, :] = SST[year_index, month_index, :]
            new_cmip_input_nc.variables['t300'][time_index, :] = T300[year_index, month_index, :]

"""
Create new_cmip_output_nc_path netCDF file. 
"""
cmip_output_nc_path = 'I:/hujie/CMIP5.label.12mon.1863_2003.nc'
cmip_output_nc = Dataset(cmip_output_nc_path)
nino = cmip_output_nc.variables['pr'][:]
lat = cmip_output_nc.variables['lat'][:]
lon = cmip_output_nc.variables['lon'][:]

new_cmip_output_nc_path = 'I:/hujie/data/CMIP5_label_1.nc'
new_cmip_output_nc = Dataset(new_cmip_output_nc_path, 'w')
new_cmip_output_nc.createDimension('time', 1692)
new_cmip_output_nc.createDimension('lat', 1)
new_cmip_output_nc.createDimension('lon', 1)
new_cmip_output_nc.createVariable('time', 'd', ('time'))
new_cmip_output_nc.createVariable('lat', 'd', ('lat'))
new_cmip_output_nc.createVariable('lon', 'd', ('lon'))
new_cmip_output_nc.createVariable('nino', 'd', ('time', 'lat', 'lon'), fill_value=np.nan)

new_cmip_output_nc.variables['time'][:] = time_list
new_cmip_output_nc.variables['lat'][:] = lat
new_cmip_output_nc.variables['lon'][:] = lon
new_cmip_output_nc.variables['time'].units = "hours since 1850-01-01 00:00:00"
new_cmip_output_nc.variables['lat'].units = "degrees_north"
new_cmip_output_nc.variables['lon'].units = "degrees_east"

nino = nino[:141, :]
print('nino.shape', nino.shape)
for year_index in range(0, 141):
    for month_index in range(12):
        year = year_index + 1863
        month = month_index + 1
        time_dt = dt.datetime(year=year, month=month, day=1, hour=0, minute=0, second=0)
        time_dt_value = date2num(time_dt, units="hours since 1850-01-01 00:00:00", calendar="standard")
        time_index = np.where(time_list == time_dt_value)[0]

        new_cmip_output_nc.variables['nino'][time_index, :] = nino[year_index, month_index, :]
