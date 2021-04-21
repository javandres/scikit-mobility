import re
import geopandas as gpd
from skmob.tessellation import tilers
import shapely
import pytest

poly = [[[116.1440758191, 39.8846396072],
         [116.3449987678, 39.8846396072],
         [116.3449987678, 40.0430521004],
         [116.1440758191, 40.0430521004],
         [116.1440758191, 39.8846396072]]]
geom = [shapely.geometry.Polygon(p) for p in poly]
bbox = gpd.GeoDataFrame(geometry=geom, crs="EPSG:4326")


@pytest.mark.parametrize('tiler_type', ["squared", "h3_tessellation"])
@pytest.mark.parametrize('base_shape', ['Beijing, China', bbox])
@pytest.mark.parametrize('meters', [15000])
def test_tiler_get(tiler_type, base_shape, meters):
    tessellation = tilers.tiler.get(tiler_type, base_shape=base_shape, meters=meters)
    assert isinstance(tessellation, gpd.GeoDataFrame)

# Arrange
@pytest.fixture()
def h3_tess():
    return tilers.H3TessellationTiler()

@pytest.mark.parametrize("input_meters, expected_res", [(500, 8), (1500, 7), (5000, 6)])
def test__meters_to_res(h3_tess, input_meters, expected_res):
    assert h3_tess._meters_to_res(input_meters) == expected_res

def test__meters_to_h3_resolution(h3_tess):
    assert h3_tess._meters_to_h3_resolution(bbox, 5000) == 6

# test UserWarning is triggered for input hexs
# that are larger than the base_shape
def test_warning(h3_tess):
    with pytest.warns(UserWarning) as user_warnings:
        pattern=r".*Try something smaller.*"
        a = h3_tess._meters_to_h3_resolution(bbox, 5000000000000000000000000000000000)

        print("---------------------------------------------")
        print(a)
        print(user_warnings)
        print("---------------------------------------------")
        # # check that 2 warnings were raised
        # assert len(user_warnings) == 1
        # # check that the message matches
        # assert re.match(pattern, user_warnings[1].message.args[0])