import copy
import json
from time import sleep

import requests

from stations import settings
from stations.dataclass import RawStation, TransformedStation, Address
from stations.settings import ADDRESS_URL


class StationHandler:
    def __init__(self) -> None:
        self.stations_list = []
        self.transformed_stations_list = []
        self.sorted_transformed_stations_list = []
        self.sorted_transformed_stations_list_with_addresses = []
        super().__init__()

    def fetch_stations(self):
        print("starting fetching stations list")
        response = requests.get(settings.STATION_URL)
        stations_list = json.loads(response.text)
        self.stations_list = stations_list
        print("done fetching stations list")

    def get_transformed_stations(self):
        print("getting transformed stations")
        self.fetch_stations()
        print("count of stations before filtering out the ones without free bikes", len(self.stations_list))
        for station_dict in self.stations_list:
            raw_station = RawStation(**station_dict)
            if raw_station.free_bikes == 0:
                continue
            transformed_station = TransformedStation(
                id=raw_station.id,
                name=raw_station.name,
                active=True if raw_station.status == "aktiv" else False,
                description=raw_station.description,
                boxes=raw_station.boxes,
                free_boxes=raw_station.free_boxes,
                free_bikes=raw_station.free_bikes,
                coordinates=[raw_station.longitude, raw_station.latitude]
            )
            self.transformed_stations_list.append(transformed_station)
        print(f"done getting transformed stations, count: {len(self.transformed_stations_list)}")

    def sort_transformed_stations(self):
        print("sorting transformed stations")
        self.sorted_transformed_stations_list = sorted(self.transformed_stations_list, key=lambda transformed_station: (
            -transformed_station.free_bikes, transformed_station.name)
        )
        print("done sorting transformed stations")

    def fetch_address(self, latitude, longitude, index, total):
        print(f"starting fetching address {index+1}/{total}")

        if index != 0:
            # because we dont want response code 429 - too many requests
            sleep(0.1)
        response = requests.get(ADDRESS_URL, {"latitude": latitude, "longitude": longitude})
        response_json = json.loads(response.text)
        print(f"done fetching address {index+1}/{total}")
        return response_json

    def add_addresses_to_transformed_stations(self):
        total = len(self.sorted_transformed_stations_list)
        for index, transformed_station in enumerate(self.sorted_transformed_stations_list):
            try:
                address_json = self.fetch_address(
                    transformed_station.coordinates[1],
                    transformed_station.coordinates[0],
                    index,
                    total
                )
            except Exception as e:
                print(f"error fetching address for sorted transformed station {index+1}", e)
                continue
            address_data = Address(**address_json)
            transformed_station_with_address = copy.deepcopy(transformed_station)
            transformed_station_with_address.address = address_data.data["name"]
            self.sorted_transformed_stations_list_with_addresses.append(transformed_station_with_address)
        print("done adding addresses to transformed stations")
