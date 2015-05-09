GIS Support
==============
This chapter assumes that the reader is familiar with the general
principles explained in the :doc:`06_api` chapter.

The MFL 2 API server uses the excellent `GeoDjango`_ and `PostGIS`_ to provide
09_services that can be used to generate facility maps, perform geographic
queries and validate facility coordinate data. You can read more about this at
the :doc:`13_gis` page.

.. _`GeoDjango`: https://docs.djangoproject.com/en/dev/ref/contrib/gis/
.. _`PostGIS`: http://postgis.net/

What is GIS?
-------------
A geographic information system (GIS) lets us visualize, question, analyze, and interpret data to understand relationships, patterns, and trends.

Master Facility List data is inherently geographical - the Master Facility
List should have coordinates for all facilities in Kenya. The GIS APIs provided
by this server support the visualization, interogation and analysis of this
data.

.. note::

    The official front-ends barely scratch the surface when it comes to the
    use of GIS data. These APIs are open to third party applications too.

GIS data formats
-------------------
There are many `GIS file formats`_ to choose from. We chose to go with
`GeoJSON`_ because it fits in with our general preference for JSON. It is easy
to convert from GeoJSON to `ESRI Shapefile`_ and `KML`_ formats.

.. _`GIS file formats`: http://en.wikipedia.org/wiki/GIS_file_formats
.. _`GeoJSON`: http://geojson.org/geojson-spec.html
.. _`ESRI Shapefile`: http://en.wikipedia.org/wiki/Shapefile
.. _`KML`: http://en.wikipedia.org/wiki/Keyhole_Markup_Language

A brief note about points
----------------------------
In "day to day language", we might be accustomed to expressing points as
`(latitude, longitude)` pairs e.g `(-1.300462, 36.791533)` for the location of
this writer's office at the time of writing. When expressing that location as
a GeoJSON "point", we'll need to "flip" the coordinates, so that the GeoJSON
for this author's office would be:

.. code-block:: javascript

    {
        type: "Point",
        coordinates: [
            36.791533,
            -1.300462
        ]
    }

How do I move from GeoJSON to a map?
-------------------------------------
If you are building a web application, take a look at `Leaflet`_ and
`OpenLayers`_.

If you are working on a mobile application, you could take a look at the
`Google Maps API`_ or its competitors e.g Bing Maps.

If you are working on on a desktop application, we assume that you know what
you are doing and do not need any helpful pointers.

.. _`Leaflet`: http://leafletjs.com/
.. _`OpenLayers`: http://openlayers.org/
.. _`Google Maps API`: https://developers.google.com/maps/

Administrative units
----------------------
Kenya has a three tier administrative structure: the country has 47
**counties**. Each county has a number of **constituencies**, with the total
for the country being 290 constituencies. Each constituency has a number of
wards, with the total for the country being 1450 wards. The GIS enabled APIs
follow this administrative structure.

.. note::

    This server also has resources that contain country boundaries. The
    default distribution has data from the `World Borders Dataset` ( from
    http://thematicmapping.org/ ).

    We have not documented the country boundary APIs for the following reasons:

     * The county, constituency and ward boundary APIs meet all of the Kenyan MFL needs.
     * The borders in the World Borders Dataset are inaccurate - sometimes lopping off several square kilometers around the borders.

.. note::

    The default distribution has map ( boundary ) data for 1482 out of 1450
    wards.

The administrative unit data is considered "setup data" - loaded at
server install time, rarely changed afterward. For that reason, the
documentation will focus on retrieval and interpretation. If you need to change
or add, the basic principles explained in the :doc:`06_api` chapter still
apply.

Counties
++++++++++++
Counties can be listed by sending a ``GET`` to ``/api/common/counties/``.
Every county is identified by a ``name`` and ``code``.

An individual county's detail record is available at
``/api/common/counties/<pk>/`` e.g
``/api/common/counties/dd999449-d36b-47f2-a958-1f5bb52951d4/`` for the county
whose ``id`` is ``dd999449-d36b-47f2-a958-1f5bb52951d4``.

.. note::

    The county detail view is "rich". It embeds a ``facility_coordinates`` key
    that shows the location of every facility in that county.

    The facility co-ordinates are a map, with the facility names as keys.
    For example:

    .. code-block:: javascript

        facility_coordinates: {
            AAR Gwh Health Care Ltd: {
                type: "Point",
                coordinates: [
                    36.80897,
                    -1.29467
                ]
            },
            Dr Musili Clinic (Afya Centre-Nairobi): {
                type: "Point",
                    coordinates: [
                        36.82763,
                        -1.28799
                ]
            },
            // truncated for brevity

    The county detail view also embeds within itself the appropriate
    ``county_boundary``. The contents of this will be discussed in the next
    section.

County Boundaries
+++++++++++++++++++
County boundaries can be listed at ``/api/gis/county_boundaries/``. The list
view is a GeoJSON "FeatureCollection", while the detail view is a GeoJSON
"Feature".

.. note::
    The border ( polygon ) is under the ``geometry`` key for every feature.

    Every boundary ( feature ) serialization has the following fields:

     * ``center`` - a ``Point`` that represents the **geometric centre** of the area
     * ``facility_count`` - the number of facilities in that geographic area
     * ``density`` - a **synthetic value** ( roughly comparable to facilities per square kilometer, although it is not actually facilities / sq.km ). This is used by front-end clients to color-code maps.
     * ``constituency_ids`` - a list of the ``id`` s ( primary keys ) of the constituencies under that county. These can be appended to the ``/api/common/constituencies/`` endpoint i.e ``/api/constituencies/<id>/`` in order to retrieve the details of each constituency in the county.
     * ``constituency_boundary_ids`` - a list of the ``id`` s of the constituency boundary objects for the constituencies under the county in question. These can be used to retrieve the constituency boundaries at ``/api/gis/constituency_boundaries/<pk>/``.

Constituencies
+++++++++++++++++
Constituencies can be listed by sending a ``GET`` to
``/api/common/constituencies/``. Every constituency is identified by a
``name`` and a ``code``.

.. note::

    The constituency detail view is, like the county detail view, "rich".
    It embeds ``facility_coordinates`` and the relevant
    ``constituency_boundary``.


Constituency Boundaries
+++++++++++++++++++++++++
Constituency boundaries can be listed at ``/api/gis/constituency_boundaries/``.
The output is similar to that of the county boundary endpoints, with the
following differences: it embeds ``ward_ids`` instead of ``constituency_ids``
and ``ward_boundary_ids`` instead of ``constituency_boundary_ids``.

Wards
++++++++
Wards can be listed by sending a ``GET`` to ``/api/common/wards/``. Every ward
is identified by a ``name`` and a ``code``.

.. note::

    The ward detail view is, like the county and constituency detail views,
    "rich". It embeds ``facility_coordinates`` and the relevant
    ``ward_boundary``.

Ward Boundaries
++++++++++++++++++
Ward boundaries can be listed at ``/api/gis/ward_boundaries/``.
The output is similar to that of the county boundary endpoints, with the
following differences: as the smallest administrative unit, a ward does not
embed the coordinates of any other administrative unit.

Facility Coordinates
-----------------------
The facility coordinates resources can be found at ``/api/gis/coordinates/``.
The example below will be used to explain the format:

.. code-block:: javascript

    {
        id: "1051cac1-b6e1-46c6-8782-a182dd1a9c50",
        type: "Feature",
        geometry: {
            type: "Point",
            coordinates: [
                34.92687,
                0.88226
            ]
        },
        properties: {
            created: "2015-05-06T17:29:47.710254Z",
            updated: "2015-05-06T17:29:47.710266Z",
            deleted: false,
            active: true,
            search: null,
            collection_date: "2015-05-06T17:29:48.624415Z",
            created_by: 1,
            updated_by: 1,
            facility: "7f91fb27-8fa5-4160-b572-2dc0ad7a554e",
            source: "c027c6fa-19b2-4fcd-83fa-f84705be84ea",
            method: "1a3f3df8-8c18-4cac-89cc-93dc59a0e057"
        }
    }

The facility's location is the ``geometry`` ``Point``. The facility in
question is identified by the ``facility`` property, which contains a
facility primary key that can be used to retrieve the facilities from
``/api/facilities/facilities/<pk>/`` e.g.
``/api/facilities/facilities/7f91fb27-8fa5-4160-b572-2dc0ad7a554e/`` for
the example above.

To set up new facility coordinates, ``POST`` to ``/api/gis/coordinates/``
a payload similar to the example below:

.. code-block:: javascript

    {
        "coordinates": {
            "type": "Point",
            "coordinates": [
                34.96962,
                0.45577
            ]
        },
        "facility": "be6ca131-5767-45b2-8213-104214becdd3",
        "source": "c027c6fa-19b2-4fcd-83fa-f84705be84ea",
        "method": "cd0bbbcf-60fa-4b76-b48c-5dcda414b43d"
    }

Every geocode is associated with a geocode source and a geocode method.
The ``source`` key in the payload above is for the geocode source while
the ``method`` key is for the geocode method.

Geocode sources are viewed/created at ``/api/gis/geo_code_sources/``
while geocode methods are viewed/created at ``/api/gis/geo_code_methods/``.
Both take a ``name`` and a ``description``.
