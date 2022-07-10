import responses

from stations import settings
from stations.station_handler import StationHandler

stations_json = [
    {
        "id": 108,
        "name": "Friedrich Schmidtplatz",
        "status": "aktiv",
        "description": "Ecke Lichtenfelsgasse U2 Station Rathaus",
        "boxes": 24,
        "free_boxes": 24,
        "free_bikes": 0,
        "longitude": 16.356581,
        "latitude": 48.211433,
        "internal_id": 1026
    },
    {
        "id": 109,
        "name": "Johannesgasse",
        "status": "aktiv",
        "description": "Parkring / Stadtpark beim Haupteingang des Kursalons",
        "boxes": 20,
        "free_boxes": 13,
        "free_bikes": 6,
        "longitude": 16.376719,
        "latitude": 48.203366,
        "internal_id": 1029
    },
    {
        "id": 112,
        "name": "Kärntner Ring",
        "status": "aktiv",
        "description": "Ecke Akademiestraße in der Mitte der beiden Einkaufszentren der Ringstraßengalerien",
        "boxes": 16,
        "free_boxes": 11,
        "free_bikes": 5,
        "longitude": 16.371317,
        "latitude": 48.202157,
        "internal_id": 1028
    },
    {
        "id": 110,
        "name": "Rathausplatz",
        "status": "aktiv",
        "description": "Universitätsring gegenüber des Burgtheaters",
        "boxes": 20,
        "free_boxes": 20,
        "free_bikes": 0,
        "longitude": 16.36025,
        "latitude": 48.209921,
        "internal_id": 1027
    },
    {
        "id": 103,
        "name": "Schottenring U4",
        "status": "aktiv",
        "description": "Franz-Josefs-Kai / Ringturm / Höhe Werdertorgasse U4 Station Schottenring beim Ausgang Salztorbrücke",
        "boxes": 21,
        "free_boxes": 16,
        "free_bikes": 5,
        "longitude": 16.372222,
        "latitude": 48.215964,
        "internal_id": 1020
    },
    {
        "id": 104,
        "name": "Schwedenplatz",
        "status": "aktiv",
        "description": "Franz-Josefs-Kai / Rotenturmstraße bei der U-Bahnstation Schwedenplatz - Ausgang Rotenturmstraße",
        "boxes": 30,
        "free_boxes": 29,
        "free_bikes": 1,
        "longitude": 16.376655,
        "latitude": 48.211699,
        "internal_id": 1023
    },
    {
        "id": 101,
        "name": "Singerstraße",
        "status": "aktiv",
        "description": "Singerstraße vor Hausnummer 2",
        "boxes": 22,
        "free_boxes": 9,
        "free_bikes": 12,
        "longitude": 16.372136949390438,
        "latitude": 48.20782938971974,
        "internal_id": 1030
    },
    {
        "id": 106,
        "name": "Stadtpark Stubenring",
        "status": "inaktiv",
        "description": "Parkring / Weiskirchner Str. / Stadtpark gegenüber dem Museum für Angewandte Kunst",
        "boxes": 20,
        "free_boxes": 17,
        "free_bikes": 1,
        "longitude": 16.380446122684475,
        "latitude": 48.20682045864029,
        "internal_id": 1024
    },
    {
        "id": 113,
        "name": "Universitätsring",
        "status": "aktiv",
        "description": "gegenüber ONr. 6",
        "boxes": 38,
        "free_boxes": 19,
        "free_bikes": 19,
        "longitude": 16.360787,
        "latitude": 48.21192,
        "internal_id": 1134
    },
    {
        "id": 102,
        "name": "Wallnerstraße",
        "status": "aktiv",
        "description": "Ecke Fahnengasse U3 Station Herrengasse vor dem Ausgang Fahnengasse",
        "boxes": 27,
        "free_boxes": 1,
        "free_bikes": 25,
        "longitude": 16.36668681481933,
        "latitude": 48.2097240924198,
        "internal_id": 1021
    },
    {
        "id": 201,
        "name": "Heinestraße",
        "status": "aktiv",
        "description": "U-Bahn Aufgang Heinestraße",
        "boxes": 38,
        "free_boxes": 20,
        "free_bikes": 18,
        "longitude": 16.390280334987665,
        "latitude": 48.21845439674175,
        "internal_id": 1069
    }
]

address_json_0 = {
   "data":{
      "id":"bev:V2llbnx8MTAyMHx8T2x5bXBpYXBsYXR6fHwy",
      "name":"Olympiaplatz 2, 1020 Wien",
      "type":"address",
      "coordinate":{
         "longitude":16.421348,
         "latitude":48.210316
      },
      "parts":{
         "postcode":"1020",
         "city":"Wien",
         "street":"Olympiaplatz",
         "country":"AT",
         "streetnumber":"2"
      }
   }
}


class TestStationHandler:

    @responses.activate
    def test_get_sorted_transformed_stations_and_get_address_for_first_one(self):
        station_handler = StationHandler()
        responses.add(
            responses.GET,
            settings.STATION_URL,
            status=200,
            json=stations_json
        )
        assert station_handler.stations_list == []
        assert station_handler.transformed_stations_list == []
        station_handler.get_transformed_stations()
        assert len(station_handler.stations_list) == 11
        assert len(station_handler.transformed_stations_list) == 9

        station_handler.sort_transformed_stations()

        station_0 = station_handler.sorted_transformed_stations_list[0]
        assert station_0.id == 102
        assert station_0.name == 'Wallnerstraße'
        assert station_0.active is True
        assert station_0.boxes == 27
        assert station_0.description == 'Ecke Fahnengasse U3 Station Herrengasse vor dem Ausgang Fahnengasse'
        assert station_0.free_boxes == 1
        assert station_0.free_bikes == 25
        assert station_0.free_ratio == 0.037037037037037035
        assert station_0.coordinates == [16.36668681481933, 48.2097240924198]

        station_1 = station_handler.sorted_transformed_stations_list[1]
        assert station_1.id == 113
        assert station_1.name == 'Universitätsring'
        assert station_1.active is True
        assert station_1.boxes == 38
        assert station_1.description == 'gegenüber ONr. 6'
        assert station_1.free_boxes == 19
        assert station_1.free_bikes == 19
        assert station_1.free_ratio == 0.5
        assert station_1.coordinates == [16.360787, 48.21192]

        station_2 = station_handler.sorted_transformed_stations_list[2]
        assert station_2.id == 201
        assert station_2.name == 'Heinestraße'
        assert station_2.active is True
        assert station_2.boxes == 38
        assert station_2.description == 'U-Bahn Aufgang Heinestraße'
        assert station_2.free_boxes == 20
        assert station_2.free_bikes == 18
        assert station_2.free_ratio == 0.5263157894736842
        assert station_2.coordinates == [16.390280334987665, 48.21845439674175]

        station_7 = station_handler.sorted_transformed_stations_list[7]
        assert station_7.id == 104
        assert station_7.name == 'Schwedenplatz'
        assert station_7.active is True
        assert station_7.boxes == 30
        assert station_7.description == (
            'Franz-Josefs-Kai / Rotenturmstraße bei der U-Bahnstation Schwedenplatz - Ausgang Rotenturmstraße'
        )
        assert station_7.free_boxes == 29
        assert station_7.free_bikes == 1
        assert station_7.free_ratio == 0.9666666666666667
        assert station_7.coordinates == [16.376655, 48.211699]

        station_8 = station_handler.sorted_transformed_stations_list[8]
        assert station_8.id == 106
        assert station_8.name == 'Stadtpark Stubenring'
        assert station_8.active is False
        assert station_8.boxes == 20
        assert station_8.description == 'Parkring / Weiskirchner Str. / Stadtpark gegenüber dem Museum für Angewandte Kunst'
        assert station_8.free_boxes == 17
        assert station_8.free_bikes == 1
        assert station_8.free_ratio == 0.85
        assert station_8.coordinates == [16.380446122684475, 48.20682045864029]

        params = {"longitude": station_0.coordinates[0], "latitude": station_0.coordinates[1]}
        responses.add(
            responses.GET,
            settings.ADDRESS_URL,
            status=200,
            json=address_json_0,
            match=[responses.matchers.query_param_matcher(params)],
        )

        station_handler.add_addresses_to_transformed_stations()

        station_0 = station_handler.sorted_transformed_stations_list_with_addresses[0]
        assert station_0.address == "Olympiaplatz 2, 1020 Wien"