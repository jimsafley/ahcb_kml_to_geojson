import xml.etree.ElementTree as ET
from datetime import datetime
import argparse
import json

parser = argparse.ArgumentParser(description='Convert KML published by the Atlas of Historical County Boundaries (AHCB) to GeoJSON')
parser.add_argument('kml_file', help='The AHCB KML file')
parser.add_argument('county_date', help='Get counties that existed at this date (YYYY-MM-DD)')
args = parser.parse_args()

county_date = datetime.strptime(args.county_date, '%Y-%m-%d')
namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}
parser = ET.XMLParser(encoding='ISO-8859-1')
root = ET.parse(args.kml_file, parser=parser).getroot()
geojson_features = []

for folder in root.findall('./kml:Document/kml:Folder', namespaces):
    folder_name = folder.find('./kml:name', namespaces).text
    if 'Counties' == folder_name:
        for state_terr_folder in folder.findall('./kml:Folder', namespaces):
            state_terr_folder_name = state_terr_folder.find('./kml:name', namespaces).text
            for county_placemark in state_terr_folder.findall('./kml:Placemark', namespaces):
                county_placemark_name = county_placemark.find('./kml:name', namespaces).text
                county_time_span_begin = county_placemark.find('./kml:TimeSpan/kml:begin', namespaces).text
                county_time_span_end = county_placemark.find('./kml:TimeSpan/kml:end', namespaces).text
                # Only convert counties that existed at the specified date.
                if datetime.strptime(county_time_span_begin, '%Y-%m-%d') <= county_date <= datetime.strptime(county_time_span_end, '%Y-%m-%d'):
                    polygons = county_placemark.findall('./kml:MultiGeometry/kml:Polygon', namespaces)
                    print('{}\t{}'.format(state_terr_folder_name, county_placemark_name))
                    geojson_coordinates = []
                    for polygon in polygons:
                        kml_coordinates = polygon.find('./kml:outerBoundaryIs/kml:LinearRing/kml:coordinates', namespaces).text.splitlines()
                        kml_coordinates = [coord.strip() for coord in kml_coordinates] # Trim whitespace
                        kml_coordinates = [coord for coord in kml_coordinates if coord] # Remove empty strings
                        kml_coordinates = [[float(latlng) for latlng in coord.split(',')[:2]] for coord in kml_coordinates] # Split and cast to float
                        geojson_coordinates.append(kml_coordinates if (1 == len(polygons)) else [kml_coordinates])
                    county_schema_data = county_placemark.find('./kml:ExtendedData/kml:SchemaData', namespaces)
                    geojson_features.append({
                        'type': 'Feature',
                        'properties': {
                            'id': county_schema_data.find('./kml:SimpleData[@name="ID"]', namespaces).text,
                            'id_num': county_schema_data.find('./kml:SimpleData[@name="ID_NUM"]', namespaces).text,
                            'fips': county_schema_data.find('./kml:SimpleData[@name="FIPS"]', namespaces).text,
                            'name': county_schema_data.find('./kml:SimpleData[@name="NAME"]', namespaces).text,
                            'full_name': county_schema_data.find('./kml:SimpleData[@name="FULL_NAME"]', namespaces).text,
                            'cnty_type': county_schema_data.find('./kml:SimpleData[@name="CNTY_TYPE"]', namespaces).text,
                            'area_sqmi': county_schema_data.find('./kml:SimpleData[@name="AREA_SQMI"]', namespaces).text,
                            'state_terr': county_schema_data.find('./kml:SimpleData[@name="STATE_TERR"]', namespaces).text,
                            'start_date': county_time_span_begin,
                            'end_date': county_time_span_end,
                        },
                        'geometry': {
                            'type': 'Polygon' if (1 == len(geojson_coordinates)) else 'MultiPolygon',
                            'coordinates': geojson_coordinates
                        },
                    })
geojson = {
    'type': 'FeatureCollection',
    'features': geojson_features,
}
with open('feature-collection-{}.json'.format(args.county_date), 'w') as outfile:
    outfile.write(json.dumps(geojson))
