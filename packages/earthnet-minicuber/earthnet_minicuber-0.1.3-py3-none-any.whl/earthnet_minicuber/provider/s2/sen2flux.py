"""
This code is originally Core code for the sen2flux dataset from https://github.com/davemlz/sen2flux. It is licensed under:

The MIT License (MIT)

Copyright (c) 2022 David Montero Loaiza

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import planetary_computer as pc

import xarray as xr
from .nbar import nbar
from pyproj import Transformer

from .utils import *



def sunAndViewAngles(items, ref, aws_bucket = "dea"):
    """Creates the Sun and Sensor View angles in degrees from the metadata.

    Parameters
    ----------
    items : dict
        Items from the STAC.
    ref : xarray.DataArray
        Stacked array to merge the angles.

    Returns
    -------
    xarray.DataArray, xarray.DataArray
        Stacked array with angles and the previous array.
    """
    items = items[::-1]
    metadata_items = []
    idx = []
    iC = 0
    for item in items:
        if ((aws_bucket != "planetary_computer") and (item.properties['sentinel:product_id'] in ref.id)) or (item.id in ref.id):
            item.clear_links()
            try:
                if aws_bucket == "planetary_computer":
                    metadata_items.append(
                        Metadata(pc.sign(item.assets["granule-metadata"].href))
                    )
                else:
                    metadata_items.append(
                        Metadata(item.assets["metadata"].href)
                    )
                idx.append(iC)
            except:
                if aws_bucket == "planetary_computer":
                    print(f"No BRDF metadata found for {item.id}. Thus skipping.")
                else:
                    print(f"No BRDF metadata found for {item.properties['sentinel:product_id']}. Thus skipping.")

            iC = iC + 1
    ref = ref[idx]

    angles_array = []
    for metadata in metadata_items:

        curr_metadata = metadata.xr
        
        if ref.epsg.values != metadata.epsg:

            transformer = Transformer.from_crs(int(metadata.epsg), int(ref.epsg.values), always_xy = True)

            x_grid, y_grid = metadata.xr.x.values, metadata.xr.y.values

            new_x, new_y = transformer.transform(x_grid, y_grid)

            curr_metadata["x"] = new_x
            curr_metadata["y"] = new_y

        
        angles_array.append(
            curr_metadata.interp(
                x=ref.x.data,
                y=ref.y.data,
                method="linear",
                kwargs={"fill_value": "extrapolate"},
            )
        )
    
    if len(angles_array) == 0:
        return None, None
    md = xr.concat(angles_array, dim="time")
    md = md.assign_coords(time=("time", ref.time.data))


    complete = xr.concat([ref, md], dim="band")

    return complete, ref



def computeNBAR(arr, ref):
    """Computes the NBAR.

    Parameters
    ----------
    arr : xarray.DataArray
        Stacked array with angles.
    ref : xarray.DataArray
        Previous stacked array.

    Returns
    -------
    xarray.DataArray
        Stacked array with NBAR.
    """
    complete_nbar = xr.concat([nbar(i) for i in arr], dim="time")
    complete_nbar = (complete_nbar * 10000).round()

    nbar_bands = [b.split("_")[0] for b in complete_nbar.band.values]

    S2_NBAR_DAY = xr.concat([ref.where(~ref.band.isin(nbar_bands), drop = True), complete_nbar.assign_coords({"band": nbar_bands})], dim="band")

    return S2_NBAR_DAY
