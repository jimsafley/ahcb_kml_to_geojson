# AHCB KML to GeoJSON

This utility will convert [KML](https://www.opengeospatial.org/standards/kml/) published
by the [Atlas of Historical County Boundaries (AHCB)](https://publications.newberry.org/ahcbp/)
to [GeoJSON](https://tools.ietf.org/html/rfc7946).

After downloading a KMZ file from [AHCB's download page](https://publications.newberry.org/ahcbp/downloads/united_states.html)
you must convert it to an uncompressed KML file:

```
$ unzip US_HistCounties_ExAKHI_Gen01_KMZ.zip
$ mv US_HistCounties_ExAKHI_Gen01.kmz US_HistCounties_ExAKHI_Gen01.zip
$ unzip US_HistCounties_ExAKHI_Gen01.kmz
```

To convert the KML to GeoJSON, run the following command:

```
$ python3 convert.py <kml_file> <county_date>
```

The command takes two positional arguments:

1. kml_file: The AHCB KML file (e.g. `US_HistCounties_ExAKHI_Gen01.kml`)
1. county_date: Get counties that existed at this date (YYYY-MM-DD) (e.g. `1926-01-01`)

This will create the GeoJSON file in the same directory.
