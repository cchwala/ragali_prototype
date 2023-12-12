import numpy as np
import xarray as xr
from shapely import LineString, Point


def _shapely_lines_from_dataset(ds_cmls):
    lines = [
        LineString(
            [
                (ds_cmls.isel(cml_id=i).site_0_lon, ds_cmls.isel(cml_id=i).site_0_lat),
                (ds_cmls.isel(cml_id=i).site_1_lon, ds_cmls.isel(cml_id=i).site_1_lat),
            ]
        )
        for i in range(len(ds_cmls.cml_id.values))
    ]
    return lines


def _shapely_points_from_dataset(ds_gauges):
    points = [
        Point([ds_gauges.isel(station_id=i).lon, ds_gauges.isel(station_id=i).lat])
        for i in range(len(ds_gauges.station_id.values))
    ]
    return points


def get_gauge_distance_per_cml(ds_cmls, ds_gauges):
    lines = _shapely_lines_from_dataset(ds_cmls)
    points = _shapely_points_from_dataset(ds_gauges)
    gauge_distance_per_cml_line = xr.DataArray(
        data=[line.distance(points) for line in lines],
        coords={
            'cml_id': ds_cmls.cml_id,
            'station_id': ds_gauges.station_id,
        },
    )
    return gauge_distance_per_cml_line


def get_n_closest_gauges(ds_cmls, ds_gauges, n_closest=3):
    gauge_distance_per_cml = get_gauge_distance_per_cml(
        ds_cmls=ds_cmls,
        ds_gauges=ds_gauges,
    )

    closest_gauges = xr.Dataset(
        data_vars={
            'distance': (('cml_id', 'n_closest'), np.sort(gauge_distance_per_cml, axis=1)),
            'station_id': (
                ('cml_id', 'n_closest'),
                gauge_distance_per_cml.station_id.values[np.argsort(gauge_distance_per_cml)],
            ),
        },
        coords={
            'cml_id': ds_cmls.cml_id.values,
        },
    )
    return closest_gauges.isel(n_closest=slice(0, n_closest))
