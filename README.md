# AHCB KML to GeoJSON

This utility will convert [KML](https://www.opengeospatial.org/standards/kml/) files
published by the [Atlas of Historical County Boundaries (AHCB)](https://publications.newberry.org/ahcbp/)
to [GeoJSON](https://tools.ietf.org/html/rfc7946) files.

After downloading a KMZ file from [AHCB's download page](https://publications.newberry.org/ahcbp/downloads/united_states.html)
you must convert it to an uncompressed KML file.

```
$ unzip US_HistCounties_ExAKHI_Gen01_KMZ.zip
$ mv US_HistCounties_ExAKHI_Gen01.kmz US_HistCounties_ExAKHI_Gen01.zip
$ unzip US_HistCounties_ExAKHI_Gen01.kmz
```
