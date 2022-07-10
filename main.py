from stations.station_handler import StationHandler


def main():
    station_handler = StationHandler()
    station_handler.get_transformed_stations()
    station_handler.sort_transformed_stations()
    station_handler.add_addresses_to_transformed_stations()
    print("sorted transformed stations with addresses", station_handler.sorted_transformed_stations_list_with_addresses)


if __name__ == "__main__":
    main()
