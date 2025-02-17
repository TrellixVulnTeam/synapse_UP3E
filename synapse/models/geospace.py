import synapse.exc as s_exc

import synapse.lib.gis as s_gis
import synapse.lib.layer as s_layer
import synapse.lib.types as s_types
import synapse.lib.module as s_module
import synapse.lib.grammar as s_grammar

units = {
    'mm': 1,
    'millimeter': 1,
    'millimeters': 1,

    'cm': 10,
    'centimeter': 10,
    'centimeters': 10,

    # international foot
    'foot': 304.8,
    'feet': 304.8,

    'm': 1000,
    'meter': 1000,
    'meters': 1000,

    # international mile
    'mile': 1609344,
    'miles': 1609344,

    'km': 1000000,
    'kilometer': 1000000,
    'kilometers': 1000000,

    # international yard
    'yard': 914.4,
    'yards': 914.4,
}

distrepr = (
    (1000000.0, 'km'),
    (1000.0, 'm'),
    (10.0, 'cm'),
)

arearepr = (
    (1000000.0, 'sq.km'),
    (1000.0, 'sq.m'),
    (10.0, 'sq.cm'),
)

areaunits = {
    'mm²': 1,
    'sq.mm': 1,

    'cm²': 10,
    'sq.cm': 10,

    # international foot
    'foot²': 304.8,
    'feet²': 304.8,
    'sq.feet': 304.8,

    'm²': 1000,
    'sq.m': 1000,
    'sq.meters': 1000,

    # international mile
    'mile²': 1609344,
    'miles²': 1609344,
    'sq.miles': 1609344,

    'km²': 1000000,
    'sq.km': 1000000,

    # international yard
    'yard²': 914.4,
    'sq.yards': 914.4,
}

geojsonschema = {

    'definitions': {

        'BoundingBox': {'type': 'array', 'minItems': 4, 'items': {'type': 'number'}},
        'PointCoordinates': {'type': 'array', 'minItems': 2, 'items': {'type': 'number'}},
        'LineStringCoordinates': {'type': 'array', 'minItems': 2, 'items': {'$ref': '#/definitions/PointCoordinates'}},
        'LinearRingCoordinates': {'type': 'array', 'minItems': 4, 'items': {'$ref': '#/definitions/PointCoordinates'}},
        'PolygonCoordinates': {'type': 'array', 'items': {'$ref': '#/definitions/LinearRingCoordinates'}},

        'Point': {
            'title': 'GeoJSON Point',
            'type': 'object',
            'required': ['type', 'coordinates'],
            'properties': {
                'type': {'type': 'string', 'enum': ['Point']},
                'coordinates': {'$ref': '#/definitions/PointCoordinates'},
                'bbox': {'$ref': '#/definitions/BoundingBox'},
            },
         },

        'LineString': {
            'title': 'GeoJSON LineString',
            'type': 'object',
            'required': ['type', 'coordinates'],
            'properties': {
                'type': {'type': 'string', 'enum': ['LineString']},
                'coordinates': {'$ref': '#/definitions/LineStringCoordinates'},
                'bbox': {'$ref': '#/definitions/BoundingBox'},
            },
         },

        'Polygon': {
            'title': 'GeoJSON Polygon',
            'type': 'object',
            'required': ['type', 'coordinates'],
            'properties': {
                'type': {'type': 'string', 'enum': ['Polygon']},
                'coordinates': {'$ref': '#/definitions/PolygonCoordinates'},
                'bbox': {'$ref': '#/definitions/BoundingBox'},
            },
        },

        'MultiPoint': {
            'title': 'GeoJSON MultiPoint',
            'type': 'object',
            'required': ['type', 'coordinates'],
            'properties': {
                'type': {'type': 'string', 'enum': ['MultiPoint']},
                'coordinates': {'type': 'array', 'items': {'$ref': '#/definitions/PointCoordinates'}},
                'bbox': {'$ref': '#/definitions/BoundingBox'},
            },
        },

        'MultiLineString': {
            'title': 'GeoJSON MultiLineString',
            'type': 'object',
            'required': ['type', 'coordinates'],
            'properties': {
                'type': {'type': 'string', 'enum': ['MultiLineString']},
                'coordinates': {'type': 'array', 'items': {'$ref': '#/definitions/LineStringCoordinates'}},
                'bbox': {'$ref': '#/definitions/BoundingBox'},
            },
         },

        'MultiPolygon': {
            'title': 'GeoJSON MultiPolygon',
            'type': 'object',
            'required': ['type', 'coordinates'],
            'properties': {
                'type': {'type': 'string', 'enum': ['MultiPolygon']},
                'coordinates': {'type': 'array', 'items': {'$ref': '#/definitions/PolygonCoordinates'}},
                'bbox': {'$ref': '#/definitions/BoundingBox'},
            },
        },

        'GeometryCollection': {
            'title': 'GeoJSON GeometryCollection',
            'type': 'object',
            'required': ['type', 'geometries'],
            'properties': {
                'type': {'type': 'string', 'enum': ['GeometryCollection']},
                'geometries': {'type': 'array', 'items': {'oneOf': [
                    {'$ref': '#/definitions/Point'},
                    {'$ref': '#/definitions/LineString'},
                    {'$ref': '#/definitions/Polygon'},
                    {'$ref': '#/definitions/MultiPoint'},
                    {'$ref': '#/definitions/MultiLineString'},
                    {'$ref': '#/definitions/MultiPolygon'},
                ]}},
                'bbox': {'$ref': '#/definitions/BoundingBox'},
            },
        },

        'Feature': {
            'title': 'GeoJSON Feature',
            'type': 'object',
            'required': ['type', 'properties', 'geometry'],
            'properties': {
                'type': {'type': 'string', 'enum': ['Feature']},
                'geometry': {'oneOf': [
                    {'type': 'null'},
                    {'$ref': '#/definitions/Point'},
                    {'$ref': '#/definitions/LineString'},
                    {'$ref': '#/definitions/Polygon'},
                    {'$ref': '#/definitions/MultiPoint'},
                    {'$ref': '#/definitions/MultiLineString'},
                    {'$ref': '#/definitions/MultiPolygon'},
                    {'$ref': '#/definitions/GeometryCollection'},
                ]},
                'properties': {'oneOf': [{'type': 'null'}, {'type': 'object'}]},
                'bbox': {'$ref': '#/definitions/BoundingBox'},
            },
        },

        'FeatureCollection': {
            'title': 'GeoJSON FeatureCollection',
            'type': 'object',
            'required': ['type', 'features'],
            'properties': {
                'type': {'type': 'string', 'enum': ['FeatureCollection']},
                'features': {'type': 'array', 'items': {'$ref': '#/definitions/Feature'}},
                'bbox': {'$ref': '#/definitions/BoundingBox'},
            },
        },
    },

    'oneOf': [
        {'$ref': '#/definitions/Point'},
        {'$ref': '#/definitions/LineString'},
        {'$ref': '#/definitions/Polygon'},
        {'$ref': '#/definitions/MultiPoint'},
        {'$ref': '#/definitions/MultiLineString'},
        {'$ref': '#/definitions/MultiPolygon'},
        {'$ref': '#/definitions/GeometryCollection'},
        {'$ref': '#/definitions/Feature'},
        {'$ref': '#/definitions/FeatureCollection'},
    ],
}

class Dist(s_types.Int):

    def postTypeInit(self):
        s_types.Int.postTypeInit(self)
        self.setNormFunc(int, self._normPyInt)
        self.setNormFunc(str, self._normPyStr)
        self.baseoff = self.opts.get('baseoff', 0)

    def _normPyInt(self, valu):
        return valu, {}

    def _normPyStr(self, text):
        try:
            valu, off = s_grammar.parse_float(text, 0)
        except Exception:
            mesg = f'Distance requires a valid number and unit. No valid number found: {text}'
            raise s_exc.BadTypeValu(mesg=mesg, name=self.name, valu=text) from None

        unit, off = s_grammar.nom(text, off, s_grammar.alphaset)

        mult = units.get(unit.lower())
        if mult is None:
            mesg = f'Unknown unit of distance: {text}'
            raise s_exc.BadTypeValu(mesg=mesg, name=self.name, valu=text)

        norm = int(valu * mult) + self.baseoff
        if norm < 0:
            mesg = f'A geo:dist may not be negative: {text}'
            raise s_exc.BadTypeValu(mesg=mesg, name=self.name, valu=text)

        return norm, {}

    def repr(self, norm):

        valu = norm - self.baseoff

        text = None

        absv = abs(valu)
        for base, unit in distrepr:
            if absv >= base:
                size = absv / base
                text = '%s %s' % (size, unit)
                break

        if text is None:
            text = '%d mm' % (absv,)

        if valu < 0:
            text = f'-{text}'

        return text

areachars = {'.'}.union(s_grammar.alphaset)
class Area(s_types.Int):

    def postTypeInit(self):
        s_types.Int.postTypeInit(self)
        self.setNormFunc(int, self._normPyInt)
        self.setNormFunc(str, self._normPyStr)

    def _normPyInt(self, valu):
        return valu, {}

    def _normPyStr(self, text):
        try:
            valu, off = s_grammar.parse_float(text, 0)
        except Exception:
            mesg = f'Area requires a valid number and unit, no valid number found: {text}'
            raise s_exc.BadTypeValu(mesg=mesg, name=self.name, valu=text) from None

        unit, off = s_grammar.nom(text, off, areachars)

        mult = areaunits.get(unit.lower())
        if mult is None:
            mesg = f'Unknown unit of area: {text}'
            raise s_exc.BadTypeValu(mesg=mesg, name=self.name, valu=text)

        norm = int(valu * mult)
        if norm < 0:
            mesg = f'A geo:area may not be negative: {text}'
            raise s_exc.BadTypeValu(mesg=mesg, name=self.name, valu=text)

        return norm, {}

    def repr(self, norm):

        text = None
        for base, unit in arearepr:
            if norm >= base:
                size = norm / base
                text = f'{size} {unit}'
                break

        if text is None:
            text = f'{norm} sq.mm'

        return text

class LatLong(s_types.Type):

    stortype = s_layer.STOR_TYPE_LATLONG

    def postTypeInit(self):
        self.setNormFunc(str, self._normPyStr)
        self.setNormFunc(list, self._normPyTuple)
        self.setNormFunc(tuple, self._normPyTuple)

        self.setCmprCtor('near=', self._cmprNear)
        self.storlifts.update({
            'near=': self._storLiftNear,
        })

    def _normCmprValu(self, valu):
        latlong, dist = valu
        rlatlong = self.modl.type('geo:latlong').norm(latlong)[0]
        rdist = self.modl.type('geo:dist').norm(dist)[0]
        return rlatlong, rdist

    def _cmprNear(self, valu):
        latlong, dist = self._normCmprValu(valu)

        def cmpr(valu):
            if s_gis.haversine(valu, latlong) <= dist:
                return True
            return False
        return cmpr

    def _storLiftNear(self, cmpr, valu):
        latlong = self.norm(valu[0])[0]
        dist = self.modl.type('geo:dist').norm(valu[1])[0]
        return ((cmpr, (latlong, dist), self.stortype),)

    def _normPyStr(self, valu):
        valu = tuple(valu.strip().split(','))
        return self._normPyTuple(valu)

    def _normPyTuple(self, valu):
        if len(valu) != 2:
            raise s_exc.BadTypeValu(valu=valu, name=self.name,
                                    mesg='Valu must contain valid latitude,longitude')

        try:
            latv = self.modl.type('geo:latitude').norm(valu[0])[0]
            lonv = self.modl.type('geo:longitude').norm(valu[1])[0]
        except Exception as e:
            raise s_exc.BadTypeValu(valu=valu, name=self.name,
                                    mesg=str(e)) from None

        return (latv, lonv), {'subs': {'lat': latv, 'lon': lonv}}

    def repr(self, norm):
        return f'{norm[0]},{norm[1]}'

class GeoModule(s_module.CoreModule):

    def getModelDefs(self):
        return (
            ('geo', {

                'ctors': (
                    ('geo:dist', 'synapse.models.geospace.Dist', {}, {
                        'doc': 'A geographic distance (base unit is mm).', 'ex': '10 km'
                    }),
                    ('geo:area', 'synapse.models.geospace.Area', {}, {
                        'doc': 'A geographic area (base unit is square mm).', 'ex': '10 sq.km'
                    }),
                    ('geo:latlong', 'synapse.models.geospace.LatLong', {}, {
                        'doc': 'A Lat/Long string specifying a point on Earth.',
                        'ex': '-12.45,56.78'
                    }),
                ),

                'types': (

                    ('geo:nloc', ('comp', {'fields': (('ndef', 'ndef'), ('latlong', 'geo:latlong'), ('time', 'time'))}), {
                        'deprecated': True,
                        'doc': 'Records a node latitude/longitude in space-time.'
                    }),
                    ('geo:telem', ('guid', {}), {
                        'doc': 'A geospatial position of a node at a given time. The node should be linked via -(seenat)> edges.',
                    }),

                    ('geo:json', ('data', {'schema': geojsonschema}), {
                        'doc': 'GeoJSON structured JSON data.'}),

                    ('geo:name', ('str', {'lower': True, 'onespace': True}), {
                        'doc': 'An unstructured place name or address.'}),

                    ('geo:place', ('guid', {}), {
                        'doc': 'A GUID for a geographic place.'}),

                    ('geo:place:taxonomy', ('taxonomy', {}), {
                        'doc': 'A taxonomy of place types.'}),

                    ('geo:address', ('str', {'lower': True, 'onespace': True}), {
                        'doc': 'A street/mailing address string.'}),

                    ('geo:longitude', ('float', {'min': -180.0, 'max': 180.0,
                                       'minisvalid': False, 'maxisvalid': True}), {
                        'ex': '31.337',
                        'doc': 'A longitude in floating point notation.',
                    }),
                    ('geo:latitude', ('float', {'min': -90.0, 'max': 90.0,
                                      'minisvalid': True, 'maxisvalid': True}), {
                        'ex': '31.337',
                        'doc': 'A latitude in floating point notation.',
                    }),

                    ('geo:bbox', ('comp', {'sepr': ',', 'fields': (
                                                ('xmin', 'geo:longitude'),
                                                ('xmax', 'geo:longitude'),
                                                ('ymin', 'geo:latitude'),
                                                ('ymax', 'geo:latitude'))}), {
                        'doc': 'A geospatial bounding box in (xmin, xmax, ymin, ymax) format.',
                    }),
                    ('geo:altitude', ('geo:dist', {'baseoff': 6371008800}), {
                        'doc': 'A negative or positive offset from Mean Sea Level (6,371.0088km from Earths core).'
                    }),
                ),

                'edges': (
                    ((None, 'seenat', 'geo:telem'), {
                        'doc': 'The source node was seen at the geo:telem node place and time.'}),
                ),

                'forms': (

                    ('geo:name', {}, ()),

                    ('geo:nloc', {}, (

                        ('ndef', ('ndef', {}), {'ro': True,
                            'doc': 'The node with location in geospace and time.'}),

                        ('ndef:form', ('str', {}), {'ro': True,
                            'doc': 'The form of node referenced by the ndef.'}),

                        ('latlong', ('geo:latlong', {}), {'ro': True,
                            'doc': 'The latitude/longitude the node was observed.'}),

                        ('time', ('time', {}), {'ro': True,
                            'doc': 'The time the node was observed at location.'}),

                        ('place', ('geo:place', {}), {
                            'doc': 'The place corresponding to the latlong property.'}),

                        ('loc', ('loc', {}), {
                            'doc': 'The geo-political location string for the node.'}),

                    )),

                    ('geo:telem', {}, (
                        ('time', ('time', {}), {
                            'doc': 'The time that the node was at the position.'}),
                        ('desc', ('str', {}), {
                            'doc': 'A description of the telemetry sample.'}),
                        ('latlong', ('geo:latlong', {}), {
                            'doc': 'The latitude/longitude reading at the time.'}),
                        ('place', ('geo:place', {}), {
                            'doc': 'The place which includes the latlong value.'}),
                        ('place:name', ('geo:name', {}), {
                            'doc': 'The purported place name. Used for entity resolution.'}),
                    )),

                    ('geo:place:taxonomy', {}, ()),
                    ('geo:place', {}, (

                        ('name', ('geo:name', {}), {
                            'doc': 'The name of the place.'}),

                        ('type', ('geo:place:taxonomy', {}), {
                            'doc': 'The type of place.'}),

                        ('names', ('array', {'type': 'geo:name', 'sorted': True, 'uniq': True}), {
                            'doc': 'An array of alternative place names.'}),

                        ('parent', ('geo:place', {}), {
                            'doc': 'A parent place, possibly from reverse geocoding.'}),

                        ('desc', ('str', {}), {
                            'doc': 'A long form description of the place.'}),

                        ('loc', ('loc', {}), {
                            'doc': 'The geo-political location string for the node.'}),

                        ('address', ('geo:address', {}), {
                            'doc': 'The street/mailing address for the place.'}),

                        ('geojson', ('geo:json', {}), {
                            'doc': 'A GeoJSON representation of the place.'}),

                        ('latlong', ('geo:latlong', {}), {
                            'doc': 'The lat/long position for the place.'}),

                        ('bbox', ('geo:bbox', {}), {
                            'doc': 'A bounding box which encompasses the place.'}),

                        ('radius', ('geo:dist', {}), {
                            'doc': 'An approximate radius to use for bounding box calculation.'}),

                        ('photo', ('file:bytes', {}), {
                            'doc': 'The image file to use as the primary image of the place.'}),
                    )),
                )
            }),
        )
