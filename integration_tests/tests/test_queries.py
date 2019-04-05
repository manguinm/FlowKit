# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from flowclient.client import get_result

import flowclient

from .utils import permissions_types, aggregation_types


@pytest.mark.parametrize(
    "query_kind, params",
    [
        (
            "daily_location",
            {"date": "2016-01-01", "aggregation_unit": "admin3", "method": "last"},
        ),
        (
            "daily_location",
            {
                "date": "2016-01-01",
                "aggregation_unit": "admin3",
                "method": "most-common",
                "subscriber_subset": None,
            },
        ),
        (
            "total_network_objects",
            {
                "start_date": "2016-01-01",
                "end_date": "2016-01-02",
                "aggregation_unit": "admin3",
            },
        ),
        # (
        #     # TODO: currently flowclient.modal_location() doesn't accept a 'locations'
        #     # argument but rather expects a list of location objects. We can't test this
        #     # using the parametrized paradigm in this test...
        #     "modal_location",
        #     {
        #         "aggregation_unit": "admin3",
        #         "locations": [
        #             {
        #                 "query_kind": "daily_location",
        #                 "date": "2016-01-01",
        #                 "aggregation_unit": "admin3",
        #                 "method": "last",
        #             },
        #             {
        #                 "query_kind": "daily_location",
        #                 "date": "2016-01-02",
        #                 "aggregation_unit": "admin3",
        #                 "method": "last",
        #             },
        #         ],
        #     },
        # ),
        (
            "modal_location_from_dates",
            {
                "start_date": "2016-01-01",
                "stop_date": "2016-01-03",
                "aggregation_unit": "admin3",
                "method": "most-common",
            },
        ),
        (
            "flows",
            {
                "from_location": {
                    "query_kind": "daily_location",
                    "date": "2016-01-01",
                    "aggregation_unit": "admin3",
                    "method": "last",
                },
                "to_location": {
                    "query_kind": "daily_location",
                    "date": "2016-01-04",
                    "aggregation_unit": "admin3",
                    "method": "last",
                },
                "aggregation_unit": "admin3",
            },
        ),
        # (
        #     # TODO: currently flowclient.modal_location() doesn't accept a 'locations'
        #     # argument but rather expects a list of location objects. We can't test this
        #     # using the parametrized paradigm in this test...
        #     "flows",
        #     {
        #         "from_location": {
        #             "query_kind": "modal_location",
        #             "aggregation_unit": "admin3",
        #             "locations": [
        #                 {
        #                     "query_kind": "daily_location",
        #                     "date": "2016-01-01",
        #                     "aggregation_unit": "admin3",
        #                     "method": "last",
        #                 },
        #                 {
        #                     "query_kind": "daily_location",
        #                     "date": "2016-01-02",
        #                     "aggregation_unit": "admin3",
        #                     "method": "last",
        #                 }
        #             ],
        #         },
        #         "to_location": {
        #             "query_kind": "daily_location",
        #             "date": "2016-01-04",
        #             "aggregation_unit": "admin3",
        #             "method": "last",
        #         },
        #         "aggregation_unit": "admin3",
        #     },
        # ),
        (
            "meaningful_locations_aggregate",
            {
                "start_date": "2016-01-01",
                "stop_date": "2016-01-02",
                "aggregation_unit": "admin1",
                "label": "unknown",
                "tower_hour_of_day_scores": [
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    0,
                    0,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    0,
                    0,
                    0,
                    0,
                    -1,
                    -1,
                    -1,
                ],
                "tower_day_of_week_scores": {
                    "monday": 1,
                    "tuesday": 1,
                    "wednesday": 1,
                    "thursday": 0,
                    "friday": -1,
                    "saturday": -1,
                    "sunday": -1,
                },
                "labels": {
                    "evening": {
                        "type": "Polygon",
                        "coordinates": [
                            [[1e-06, -0.5], [1e-06, -1.1], [1.1, -1.1], [1.1, -0.5]]
                        ],
                    },
                    "day": {
                        "type": "Polygon",
                        "coordinates": [
                            [[-1.1, -0.5], [-1.1, 0.5], [-1e-06, 0.5], [0, -0.5]]
                        ],
                    },
                },
            },
        ),
        (
            "meaningful_locations_between_label_od_matrix",
            {
                "start_date": "2016-01-01",
                "stop_date": "2016-01-02",
                "aggregation_unit": "admin1",
                "label_a": "unknown",
                "label_b": "evening",
                "tower_hour_of_day_scores": [
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    0,
                    0,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    0,
                    0,
                    0,
                    0,
                    -1,
                    -1,
                    -1,
                ],
                "tower_day_of_week_scores": {
                    "monday": 1,
                    "tuesday": 1,
                    "wednesday": 1,
                    "thursday": 0,
                    "friday": -1,
                    "saturday": -1,
                    "sunday": -1,
                },
                "labels": {
                    "evening": {
                        "type": "Polygon",
                        "coordinates": [
                            [[1e-06, -0.5], [1e-06, -1.1], [1.1, -1.1], [1.1, -0.5]]
                        ],
                    },
                    "day": {
                        "type": "Polygon",
                        "coordinates": [
                            [[-1.1, -0.5], [-1.1, 0.5], [-1e-06, 0.5], [0, -0.5]]
                        ],
                    },
                },
            },
        ),
        (
            "meaningful_locations_between_dates_od_matrix",
            {
                "start_date_a": "2016-01-01",
                "stop_date_a": "2016-01-02",
                "start_date_b": "2016-01-01",
                "stop_date_b": "2016-01-05",
                "aggregation_unit": "admin1",
                "tower_hour_of_day_scores": [
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    0,
                    0,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    0,
                    0,
                    0,
                    0,
                    -1,
                    -1,
                    -1,
                ],
                "tower_day_of_week_scores": {
                    "monday": 1,
                    "tuesday": 1,
                    "wednesday": 1,
                    "thursday": 0,
                    "friday": -1,
                    "saturday": -1,
                    "sunday": -1,
                },
                "label": "unknown",
                "labels": {
                    "evening": {
                        "type": "Polygon",
                        "coordinates": [
                            [[1e-06, -0.5], [1e-06, -1.1], [1.1, -1.1], [1.1, -0.5]]
                        ],
                    },
                    "day": {
                        "type": "Polygon",
                        "coordinates": [
                            [[-1.1, -0.5], [-1.1, 0.5], [-1e-06, 0.5], [0, -0.5]]
                        ],
                    },
                },
            },
        ),
    ],
)
def test_run_query(query_kind, params, access_token_builder, flowapi_url):
    """
    Test that queries can be run, and return a QueryResult object.
    """
    query_spec = getattr(flowclient, query_kind)(**params)
    con = flowclient.Connection(
        flowapi_url,
        access_token_builder(
            {
                query_spec["query_kind"]: {
                    "permissions": permissions_types,
                    "spatial_aggregation": aggregation_types,
                }
            }
        ),
    )

    result_dataframe = get_result(con, query_spec)
    assert 0 < len(result_dataframe)


def test_get_geography(access_token_builder, flowapi_url):
    """
    Test that queries can be run, and return a GeoJSON dict.
    """
    con = flowclient.Connection(
        flowapi_url,
        access_token_builder(
            {
                "geography": {
                    "permissions": permissions_types,
                    "spatial_aggregation": aggregation_types,
                }
            }
        ),
    )
    result_geojson = flowclient.get_geography(con, "admin3")
    assert "FeatureCollection" == result_geojson["type"]
    assert 0 < len(result_geojson["features"])
    feature0 = result_geojson["features"][0]
    assert "Feature" == feature0["type"]
    assert "admin3name" in feature0["properties"]
    assert "admin3pcod" in feature0["properties"]
    assert "MultiPolygon" == feature0["geometry"]["type"]
    assert list == type(feature0["geometry"]["coordinates"])
    assert 0 < len(feature0["geometry"]["coordinates"])


@pytest.mark.parametrize(
    "event_types, expected_result",
    [
        (
            ["sms", "forwards"],
            {
                "sms": [
                    "2016-01-01",
                    "2016-01-02",
                    "2016-01-03",
                    "2016-01-04",
                    "2016-01-05",
                    "2016-01-06",
                    "2016-01-07",
                ],
                "forwards": [],
            },
        ),
        (
            None,
            {
                "calls": [
                    "2016-01-01",
                    "2016-01-02",
                    "2016-01-03",
                    "2016-01-04",
                    "2016-01-05",
                    "2016-01-06",
                    "2016-01-07",
                ],
                "forwards": [],
                "mds": [
                    "2016-01-01",
                    "2016-01-02",
                    "2016-01-03",
                    "2016-01-04",
                    "2016-01-05",
                    "2016-01-06",
                    "2016-01-07",
                ],
                "sms": [
                    "2016-01-01",
                    "2016-01-02",
                    "2016-01-03",
                    "2016-01-04",
                    "2016-01-05",
                    "2016-01-06",
                    "2016-01-07",
                ],
                "topups": [
                    "2016-01-01",
                    "2016-01-02",
                    "2016-01-03",
                    "2016-01-04",
                    "2016-01-05",
                    "2016-01-06",
                    "2016-01-07",
                ],
            },
        ),
    ],
)
def test_get_available_dates(
    event_types, expected_result, access_token_builder, flowapi_url
):
    """
    Test that queries can be run, and return the expected JSON result.
    """
    con = flowclient.Connection(
        flowapi_url,
        access_token_builder(
            {"available_dates": {"permissions": {"get_result": True}}}
        ),
    )
    result = flowclient.get_available_dates(con, event_types=event_types)
    assert expected_result == result
