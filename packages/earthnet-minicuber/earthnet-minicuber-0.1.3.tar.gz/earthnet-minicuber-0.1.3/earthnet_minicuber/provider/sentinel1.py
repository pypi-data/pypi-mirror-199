

import os
import pystac_client
import stackstac
import rasterio
import numpy as np
import xarray as xr
from rasterio import RasterioIOError
from contextlib import nullcontext
import time
import random
import planetary_computer as pc


from scipy.ndimage.filters import uniform_filter
from scipy.ndimage.measurements import variance

from . import provider_base


def lee_filter(da, size):
    """
    Apply lee filter of specified window size.
    Adapted from https://stackoverflow.com/questions/39785970/speckle-lee-filter-in-python
    and from https://docs.digitalearthafrica.org/fr/latest/sandbox/notebooks/Real_world_examples/Radar_water_detection.html

    """
    img = da.values
    img_mean = uniform_filter(img, (size, size))
    img_sqr_mean = uniform_filter(img**2, (size, size))
    img_variance = img_sqr_mean - img_mean**2

    overall_variance = variance(img)

    img_weights = img_variance / (img_variance + overall_variance)
    img_output = img_mean + img_weights * (img - img_mean)

    return img_output

FILTERS = {"lee": lee_filter}

def get_valid_trafo_s1(item):
    a,b,c,d,e,f,g,h,j = item.properties["proj:transform"]
    if c == 0 and e == 0:
        return [b,c,a,e,f,d,g,h,j]
    else:
        return item.properties["proj:transform"]
        
    

class Sentinel1(provider_base.Provider):

    def __init__(self, bands = ["vv", "vh","mask"], speckle_filter = True, speckle_filter_kwargs = {"type": "lee", "size": 9}, s1_avail_var = True, aws_bucket = "dea"):

        self.is_temporal = True

        self.bands = bands
        self.speckle_filter = speckle_filter
        self.speckle_filter_kwargs = speckle_filter_kwargs
        self.s1_avail_var = s1_avail_var
        self.aws_bucket = aws_bucket

        if self.aws_bucket == "dea":
            URL = "https://explorer.digitalearth.africa/stac/"
        elif self.aws_bucket == "planetary_computer":
            URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
        self.catalog = pystac_client.Client.open(URL)

        if self.aws_bucket == "dea":
            os.environ['AWS_NO_SIGN_REQUEST'] = "TRUE"
            os.environ['AWS_S3_ENDPOINT'] = 's3.af-south-1.amazonaws.com'


    def load_data(self, bbox, time_interval, **kwargs):

        gdal_session = stackstac.DEFAULT_GDAL_ENV.updated(always=dict(session=rasterio.session.AWSSession(aws_unsigned = True, endpoint_url = 's3.af-south-1.amazonaws.com' if self.aws_bucket == "dea" else None)))

        if self.aws_bucket == "dea":
            cm = rasterio.Env(aws_unsigned = True, AWS_S3_ENDPOINT= 's3.af-south-1.amazonaws.com')
            
        else:
            cm = nullcontext()
        
        with cm as gs:

            search = self.catalog.search(
                    bbox = bbox,
                    collections=["s1_rtc" if self.aws_bucket == "dea" else "sentinel-1-rtc"],
                    datetime=time_interval
                )
                
            if self.aws_bucket == "planetary_computer":
                for attempt in range(10):
                    try:
                        items_s1 = pc.sign(search)
                    except pystac_client.exceptions.APIError:
                        print(f"Sen2: Planetary computer time out, attempt {attempt}, retrying in 60 seconds...")
                        time.sleep(random.uniform(30,90))
                    else:
                        break
                else:
                    print("Loading Sen2 failed after 10 attempts...")
                    return None
            else:
                items_s1 = search.get_all_items()

                for item in items_s1:
                    trafo = get_valid_trafo_s1(item)
                    item.properties["proj:transform"] = trafo
                    for asset in item.assets:
                        item.assets[asset].extra_fields['proj:transform'] = trafo
                
            if len(items_s1.to_dict()['features']) == 0:
                return None
            
            metadata = items_s1.to_dict()['features'][0]["properties"]
            epsg = metadata["proj:epsg"]
            # geotransform = metadata["proj:transform"]

            stack = stackstac.stack(items_s1, epsg = epsg, assets = self.bands, dtype = "float32", properties = False, band_coords = False, bounds_latlon = bbox, xy_coords = 'center', chunksize = 2048,errors_as_nodata=(RasterioIOError('.*'), ), gdal_env=gdal_session)

            # stack = stack.isel(time = [v[0] for v in stack.groupby("time.date").groups.values()])

            stack["band"] = [f"s1_{b}" for b in stack.band.values]

            stack = stack.to_dataset("band")

            if self.speckle_filter:
                valid = np.isfinite(stack)
                #stack = stack.where(valid, 0)

                if "s1_vv" in stack.variables:
                    stack["s1_vv"] = stack.where(valid, 0).s1_vv.groupby("time").apply(FILTERS[self.speckle_filter_kwargs["type"]], size=self.speckle_filter_kwargs["size"])
                    stack['s1_vv'] = stack.s1_vv.where(valid.s1_vv)

                if "s1_vh" in stack.variables:
                    stack["s1_vh"] = stack.where(valid, 0).s1_vh.groupby("time").apply(FILTERS[self.speckle_filter_kwargs["type"]], size=self.speckle_filter_kwargs["size"])
                    stack['s1_vh'] = stack.s1_vh.where(valid.s1_vh)
            
            
            
            stack = stack.drop_vars(["epsg", "id"])

            if self.aws_bucket == "dea":
                stack = stack.rename({"x": "lon", "y": "lat"})
            
            if len(stack.time) > 0:
                stack = stack.groupby("time.date").last(skipna = False).rename({"date": "time"})
            else:
                return None

            stack["time"] = np.array([str(d) for d in stack.time.values], dtype="datetime64[D]")

            if "s1_vv" in stack.variables:
                stack["s1_vv"].attrs = {"provider": "Sentinel 1", "interpolation_type": "linear", "description": "Linear backscatter intensity in VV polarization"}
            if "s1_vh" in stack.variables:
                stack["s1_vh"].attrs = {"provider": "Sentinel 1", "interpolation_type": "linear", "description": "Linear backscatter intensity in VH polarization"}
            if "s1_mask" in stack.variables:
                stack["s1_mask"].attrs = {"provider": "Sentinel 1", "interpolation_type": "nearest", "description": "Data mask", "classes": """
                0 - Nodata
                1 - Valid
                2 - Invalid (in/near radar shadow)
                """}

            if self.s1_avail_var:
                stack["s1_avail"] = xr.DataArray(np.ones_like(stack.time.values, dtype = "uint8"), coords = {"time": stack.time.values}, dims = ("time",))

            stack.attrs["epsg"] = epsg

            return stack
