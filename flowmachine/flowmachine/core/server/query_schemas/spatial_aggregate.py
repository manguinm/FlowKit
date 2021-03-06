# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marshmallow import Schema, fields, post_load
from marshmallow_oneofschema import OneOfSchema


from flowmachine.features.utilities.spatial_aggregates import SpatialAggregate
from .base_exposed_query import BaseExposedQuery
from .daily_location import DailyLocationSchema
from .modal_location import ModalLocationSchema

__all__ = [
    "SpatialAggregateSchema",
    "SpatialAggregateExposed",
    "InputToSpatialAggregate",
]


class InputToSpatialAggregate(OneOfSchema):
    type_field = "query_kind"
    type_schemas = {
        "daily_location": DailyLocationSchema,
        "modal_location": ModalLocationSchema,
    }


class SpatialAggregateSchema(Schema):
    locations = fields.Nested(InputToSpatialAggregate, required=True)

    @post_load
    def make_query_object(self, params):
        return SpatialAggregateExposed(**params)


class SpatialAggregateExposed(BaseExposedQuery):
    def __init__(self, *, locations):
        # Note: all input parameters need to be defined as attributes on `self`
        # so that marshmallow can serialise the object correctly.
        self.locations = locations

    @property
    def _flowmachine_query_obj(self):
        """
        Return the underlying flowmachine object.

        Returns
        -------
        Query
        """
        locations = self.locations._flowmachine_query_obj
        return SpatialAggregate(locations=locations)
