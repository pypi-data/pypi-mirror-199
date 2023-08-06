

import xarray as xr
import numpy as np
import s3fs

from . import provider_base

SHORT_TO_LONG_NAMES = {
    't2m': '2m_temperature_mean', 
    't2mmax': '2m_temperature_max',
    't2mmin': '2m_temperature_min',  
    'pev': 'potential_evaporation', 
    'pet': 'potential_evapotranspiration',
    'ssrd': 'surface_net_solar_radiation', 
    'e': 'total_evaporation', 
    'tp': 'total_precipitation'
}

class ERA5_ESDL(provider_base.Provider):

    def __init__(self, bands = ['e', 'pet', 'pev', 'ssrd', 't2m', 't2mmax', 't2mmin','tp'], zarrpath = None, proxy = None):
        self.is_temporal = True
        
        self.bands = bands
        self.zarrpath = zarrpath

        if zarrpath is None:
            self.s3 = s3fs.S3FileSystem(anon=True,
            client_kwargs={
            'endpoint_url': 'https://s3.bgc-jena.mpg.de:9000',
            'region_name': 'thuringia',
            },
            config_kwargs = {
            "proxies": {'http': proxy}
            } if proxy else {}
            )

    def load_data(self, bbox, time_interval, **kwargs):
        
        # If an URL is given, loads the cloud zarr, otherwise loads from local zarrpath
        if self.zarrpath:
            era5 = xr.open_zarr(self.zarrpath)
        else:
            era5 = xr.open_zarr(s3fs.S3Map(root ="s3:///xaida/ERA5Data.zarr", s3=self.s3, check = False), consolidated=True)

        era5 = era5[self.bands]

        era5 = era5.rename({'latitude': 'lat', 'longitude': 'lon'})

        center_lon = (bbox[0] + bbox[2])/2
        center_lat = (bbox[1] + bbox[3])/2

        era5 = era5.sel(lat = center_lat, lon = center_lon, method = "nearest").drop_vars(["lat", "lon"])

        era5 = era5.sel(time = slice(time_interval[:10], time_interval[-10:]))

        era5 = era5.rename({b: f"era5_{b}" for b in self.bands})

        for b in self.bands:

            era5[f"era5_{b}"].attrs = {
                "provider": "ERA5",
                "interpolation_type": "linear",
                "description": f"{SHORT_TO_LONG_NAMES[b]} daily data processed by Fabian Gans for XAIDA project."
            }
        

        return era5