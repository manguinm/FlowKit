# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from marshmallow import ValidationError

from flowmachine.core.server.query_schemas import FlowmachineQuerySchema


@pytest.mark.parametrize(
    "expected_md5, query_spec",
    [
        (
            "ac3368744bd6f07cd55645adc3245cd6",
            {
                "query_kind": "daily_location",
                "date": "2016-01-01",
                "aggregation_unit": "admin3",
                "method": "last",
                "subscriber_subset": None,
            },
        ),
        (
            "a427b3d8499296e739e1e7dec20884cd",
            {
                "query_kind": "location_event_counts",
                "start_date": "2016-01-01",
                "end_date": "2016-01-02",
                "interval": "day",
                "aggregation_unit": "admin3",
                "direction": "both",
                "event_types": None,
                "subscriber_subset": None,
            },
        ),
        (
            "7bab205a3cbc6992f935bf429bcc3b36",
            {
                "query_kind": "modal_location",
                "aggregation_unit": "admin3",
                "locations": (
                    {
                        "query_kind": "daily_location",
                        "date": "2016-01-01",
                        "aggregation_unit": "admin3",
                        "method": "last",
                        "subscriber_subset": None,
                    },
                    {
                        "query_kind": "daily_location",
                        "date": "2016-01-02",
                        "aggregation_unit": "admin3",
                        "method": "last",
                        "subscriber_subset": None,
                    },
                ),
            },
        ),
        (
            "5b2b2484e941da429b52dda7e81fb917",
            {"query_kind": "geography", "aggregation_unit": "admin3"},
        ),
        (
            "ad1d6b73767507f85d5c55f139cb32dc",
            {
                "query_kind": "meaningful_locations_aggregate",
                "aggregation_unit": "admin1",
                "start_date": "2016-01-01",
                "stop_date": "2016-01-02",
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
                "tower_cluster_radius": 1.0,
                "tower_cluster_call_threshold": 0,
                "subscriber_subset": None,
            },
        ),
        (
            "5a2bb25072e08c232241eb4f9075b3f6",
            {
                "query_kind": "meaningful_locations_between_label_od_matrix",
                "aggregation_unit": "admin1",
                "start_date": "2016-01-01",
                "stop_date": "2016-01-02",
                "label_a": "day",
                "label_b": "evening",
                "labels": {
                    "day": {
                        "type": "Polygon",
                        "coordinates": [
                            [[-1.1, -0.5], [-1.1, 0.5], [-1e-06, 0.5], [0, -0.5]]
                        ],
                    },
                    "evening": {
                        "type": "Polygon",
                        "coordinates": [
                            [[1e-06, -0.5], [1e-06, -1.1], [1.1, -1.1], [1.1, -0.5]]
                        ],
                    },
                },
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
                "tower_cluster_radius": 1.0,
                "tower_cluster_call_threshold": 0,
                "subscriber_subset": None,
            },
        ),
        (
            "27a8d1cfa44ff875335bbc4d4aedccf9",
            {
                "query_kind": "meaningful_locations_between_dates_od_matrix",
                "aggregation_unit": "admin1",
                "start_date_a": "2016-01-01",
                "stop_date_a": "2016-01-02",
                "start_date_b": "2016-01-01",
                "stop_date_b": "2016-01-05",
                "label": "unknown",
                "labels": {
                    "day": {
                        "type": "Polygon",
                        "coordinates": [
                            [[-1.1, -0.5], [-1.1, 0.5], [-1e-06, 0.5], [0, -0.5]]
                        ],
                    },
                    "evening": {
                        "type": "Polygon",
                        "coordinates": [
                            [[1e-06, -0.5], [1e-06, -1.1], [1.1, -1.1], [1.1, -0.5]]
                        ],
                    },
                },
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
                "tower_cluster_radius": 1.0,
                "tower_cluster_call_threshold": 2,
                "subscriber_subset": None,
            },
        ),
    ],
)
def test_construct_query(expected_md5, query_spec):
    """
    Test that expected query objects are constructed by construct_query_object
    """
    obj = FlowmachineQuerySchema().load(query_spec)
    assert expected_md5 == obj.query_id


# TODO: we should re-think how we want to test invalid values, now that these are validated using marshmallow
def test_wrong_geography_aggregation_unit_raises_error():
    """
    Test that an invalid aggregation unit in a geography query raises an InvalidGeographyError
    """
    with pytest.raises(
        ValidationError,
        match="aggregation_unit.*Must be one of: admin0, admin1, admin2, admin3.",
    ):
        _ = FlowmachineQuerySchema().load(
            {"query_kind": "geography", "aggregation_unit": "DUMMY_AGGREGATION_UNIT"}
        )
