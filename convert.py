import xml.etree.ElementTree as ET
from datetime import datetime

kml_file = 'US_HistCounties_ExAKHI_Gen05.kml'
namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}
county_date = datetime(1926, 1, 1)

root = ET.parse(kml_file, parser=ET.XMLParser(encoding='ISO-8859-1')).getroot()
for folder in root.findall('./kml:Document/kml:Folder', namespaces):
    folder_name = folder.find('./kml:name', namespaces).text
    if 'Counties' == folder_name:
        for county_folder in folder.findall('./kml:Folder', namespaces):
            state_terr_name = county_folder.find('./kml:name', namespaces).text
            print('Parsing {}'.format(state_terr_name))
            for placemark in county_folder.findall('./kml:Placemark', namespaces):
                county_name = placemark.find('./kml:name', namespaces).text
                county_time_span_begin = placemark.find('./kml:TimeSpan/kml:begin', namespaces).text
                county_time_span_end = placemark.find('./kml:TimeSpan/kml:end', namespaces).text
                # Get counties that existed at a certain date.
                if datetime.strptime(county_time_span_begin, '%Y-%m-%d') <= county_date <= datetime.strptime(county_time_span_end, '%Y-%m-%d'):
                    schema_data = placemark.find('./kml:ExtendedData/kml:SchemaData', namespaces)
                    county_ahcb_id = schema_data.find('./kml:SimpleData[@name="ID"]', namespaces).text;
                    print('\tParsing {}\t{}\t{}\t{}'.format(county_name, county_ahcb_id, county_time_span_begin, county_time_span_end))
                    for polygon in placemark.findall('./kml:MultiGeometry/kml:Polygon', namespaces):
                        print(polygon.find('./kml:outerBoundaryIs/kml:LinearRing/kml:coordinates', namespaces).text)
