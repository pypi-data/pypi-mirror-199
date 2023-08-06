import os
import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from saeonobspy import SAEONObsAPI

@pytest.fixture
def saeon_api():
    os.environ["OBSDB_KEY"] = "test_key"
    return SAEONObsAPI()


@pytest.fixture
def api_response():
    response = {
            "id": 1,
            "siteName": "Test Site",
            "stationName": "Test Station",
            "phenomenonName": "Temperature",
            "phenomenonCode": "T",
            "offeringName": "Air",
            "offeringCode": "A",
            "unitName": "Celsius",
            "unitCode": "C",
            "latitudeNorth": 0.0,
            "longitudeEast": 0.0,
            "startDate": "2022-01-01",
            "endDate": "2022-12-31",
            "valueCount": 1,
        }
    return response


def test_init(saeon_api):
    assert saeon_api.BASE_URL == "https://observationsapi.saeon.ac.za/Api/Datasets"
    assert saeon_api.API_KEY == "test_key"
    assert saeon_api.HEADERS == {"Authorization": "Bearer test_key"}


@pytest.mark.parametrize("spatial", [True, False])
def test_view_datasets(saeon_api,  api_response, spatial, mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = [api_response]

    mocker.patch("requests.get", return_value=mock_response)

    df = saeon_api.view_datasets(spatial=spatial)

    assert isinstance(df, gpd.GeoDataFrame) if spatial else isinstance(df, pd.DataFrame)
    assert "geometry" in df.columns if spatial else "geometry" not in df.columns


def test_get_datasets(saeon_api, mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = \
        [{"id": 1, "date": "2022-01-01", "value": 25.0}]

    mocker.patch("requests.post", return_value=mock_response)

    df = pd.DataFrame({"id": [1]})
    start_date = "2022-01-01"
    end_date = "2022-12-31"
    data = saeon_api.get_datasets(df, start_date=start_date, end_date=end_date)

    assert isinstance(data, pd.DataFrame)
    assert len(data) == 1
    assert data.loc[0, "id"] == 1
    assert data.loc[0, "date"] == "2022-01-01"
    assert data.loc[0, "value"] == 25.0


def test_view_datasets_with_extent(saeon_api, api_response, mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = [api_response]

    mocker.patch("requests.get", return_value=mock_response)

    extent_gdf = gpd.GeoDataFrame(
        # Create a circular polygon around the point (0, 0) with radius 1
        {
            "geometry": [
                Point(0, 0).buffer(
                    1
                )
            ]
        },
        crs="EPSG:4326",
    )

    df = saeon_api.view_datasets(extent=extent_gdf)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.loc[0, "id"] == 1
    assert df.loc[0, "siteName"] == "Test Site"
