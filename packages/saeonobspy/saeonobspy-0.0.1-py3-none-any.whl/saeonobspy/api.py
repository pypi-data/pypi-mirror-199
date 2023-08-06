import os
import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from typing import Union


class SAEONObsAPI:
    def __init__(self):
        """
        Initialize the SAEONObsAPI class to access the South African Environmental Observation Network (SAEON) Observation Database API.

        Example:
        -------
        saeon_api = SAEONObsAPI()
        """

        self.BASE_URL = "https://observationsapi.saeon.ac.za/Api/Datasets"
        self.API_KEY = os.getenv("OBSDB_KEY")

        if not self.API_KEY:
            raise ValueError(
                "Failed to find API key. Please set API key using os.environ."
            )

        self.HEADERS = {"Authorization": f"Bearer {self.API_KEY}"}

    def view_datasets(
        self, extent: gpd.GeoDataFrame = None, spatial: bool = False
    ) -> pd.DataFrame:
        """
        Retrieve available datasets from the SAEON Observation Database API.

        Parameters:
        -----------
        extent : geopandas.GeoDataFrame, optional
            A GeoDataFrame containing a single polygon representing an area of interest. If provided, the resulting DataFrame will only include datasets within the specified area.
        spatial : bool, optional
            If True, return a GeoDataFrame with a 'geometry' column containing point geometries for each dataset. Default is False.

        Returns:
        --------
            pd.DataFrame
        A DataFrame containing information on the available datasets, filtered by the provided extent if applicable. If 'spatial' is set to True, a GeoDataFrame with point geometries is returned instead.

        Example:
        -------
        saeon_api = SAEONObsAPI()

        # Without extent and spatial set to False (default)
        datasets_df = saeon_api.view_datasets()

        # With extent and spatial set to True
        extent_gdf = geopandas.read_file('path/to/extent/shapefile.shp')
        spatial_datasets_gdf = saeon_api.view_datasets(extent=extent_gdf, spatial=True)
        """
        response = requests.get(self.BASE_URL, headers=self.HEADERS)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)

        # Extract relevant columns and clean up the DataFrame
        df = df[
            [
                "id",
                "siteName",
                "stationName",
                "phenomenonName",
                "phenomenonCode",
                "offeringName",
                "offeringCode",
                "unitName",
                "unitCode",
                "latitudeNorth",
                "longitudeEast",
                "startDate",
                "endDate",
                "valueCount",
            ]
        ]
        df["obs_type_code"] = (
            df["phenomenonCode"] + "_" + df["offeringCode"] + "_" + df["unitCode"]
        )
        df["description"] = (
            df["phenomenonName"] + " - " + df["offeringName"] + " - " + df["unitName"]
        )
        if extent is not None:
            gdf = gpd.GeoDataFrame(
                df,
                geometry=gpd.points_from_xy(df.longitudeEast, df.latitudeNorth),
                crs="EPSG:4326",
            )
            gdf = gpd.overlay(gdf, extent, how="intersection")

            if not spatial:
                gdf.drop(columns="geometry", inplace=True)
            return gdf
        else:
            if spatial:
                df["geometry"] = list(zip(df.longitudeEast, df.latitudeNorth))
                df["geometry"] = df["geometry"].apply(Point)
                gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
                return gdf
            else:
                return df

    def get_datasets(
        self,
        df: Union[pd.DataFrame, gpd.GeoDataFrame],
        start_date: str = None,
        end_date: str = None,
    ) -> pd.DataFrame:
        """
        Retrieve the observation data for the selected datasets.
        Parameters:
        -----------
        df : pandas.DataFrame
            A DataFrame containing an 'id' column with dataset IDs to retrieve.
        start_date : str, optional
            The start date for the observations in the format 'YYYY-MM-DD'. Default is None, which retrieves data from the earliest available date.
        end_date : str, optional
            The end date for the observations in the format 'YYYY-MM-DD'. Default is None, which retrieves data up to the most recent available date.

        Returns:
        --------
        pd.DataFrame
            A DataFrame containing the observation data for the selected datasets.

        Example:
        -------
        saeon_api = SAEONObsAPI()
        datasets_df = saeon_api.view_datasets()

        # Filter the datasets DataFrame based on your criteria
        filtered_datasets_df = datasets_df[datasets_df['siteName'] == 'Constantiaberg']
        filtered_datasets_df = filtered_datasets_df[filtered_datasets_df['description'] == 'Air Temperature - Daily Minimum - Degrees Celsius']

        #download data
        obs_data = saeon_api.get_datasets(filtered_datasets_df, start_date='2020-01-01', end_date='2020-12-31')
        """

        if (
            not (isinstance(df, pd.DataFrame) or isinstance(df, gpd.GeoDataFrame))
            or "id" not in df.columns
        ):
            raise ValueError("Input must be a DataFrame containing an 'id' column.")

        if start_date:
            start_date = pd.to_datetime(start_date).strftime("%Y-%m-%dT%H:%M:%S")
        if end_date:
            end_date = pd.to_datetime(end_date).strftime("%Y-%m-%dT%H:%M:%S")

        datasets = []

        for dataset_id in df["id"]:
            url_obs = f"{self.BASE_URL}/{dataset_id}/Observations"
            payload = {}
            if start_date and end_date:
                payload = {"startDate": start_date, "endDate": end_date}

            response = requests.post(url_obs, headers=self.HEADERS, json=payload)
            response.raise_for_status()

            data = response.json()
            temp_df = pd.DataFrame(data)
            datasets.append(temp_df)

        result = pd.concat(datasets, ignore_index=True)
        return result
