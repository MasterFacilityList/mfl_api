import json

regions_path = '/home/titan/Downloads/kenya_gis.json'

regions_file = open(regions_path, 'r')

all_data = regions_file.read()

all_data = json.loads(all_data)

wards = all_data.get('wards')
constituencies = all_data.get('constituencies')
counties = all_data.get('counties')


# wards not in data 50, 209, 641, 734, 735


def get_wards():
    formatted_wards = []
    index = 0
    for ward in wards:
        index += 1
        try:
            ward = json.loads(ward)
            props = ward.get('features')[0].get('properties')
            ward_dict = {
                'name': props.get('COUNTY_A_1'),
                'code': props.get('COUNTY_ASS'),
                'constituency': {
                    'code': props.get('CONST_CODE')
                }
            }
            if not ward_dict.get('name'):
                import pdb
                pdb.set_trace()

            else:
                formatted_wards.append(ward_dict)
        except:

            print "Ward with code {} not parsable".format(index)

            if ward == 'Not found Here':
                pass

    return formatted_wards


def write_the_wards_file():
    wards_file = open('wards_file.txt', 'w+')
    wards_data = json.dumps(get_wards())
    wards_file.write(wards_data)


def get_constituencies():
    formatted_consts = []
    index = 0
    for constituency in constituencies:
        index += 1
        try:
            ward = json.loads(constituency)
            props = ward.get('features')[0].get('properties')
            const_dict = {
                'name': props.get('CONSTITUEN'),
                'code': props.get('CONST_CODE'),
                'county': {
                    'code': props.get('COUNTY_COD')}}
            formatted_consts.append(const_dict)
        except:

            print "constituency with code {} not parsable".format(index)

    return formatted_consts


def write_the_consts_file():
    consts_file = open('consts_file.txt', 'w')
    consts_data = json.dumps(get_constituencies())
    consts_file.write(consts_data)


def get_counties():
    formatted_counties = []
    index = 0
    for county in counties:
        index += 1
        try:
            ward = json.loads(county)
            props = ward.get('features')[0].get('properties')
            county_dict = {
                'name': props.get('COUNTY_NAM'),
                'code': props.get('COUNTY_COD')
            }
            formatted_counties.append(county_dict)
        except:

            print "constituency with code {} not parsable".format(index)

            if ward == 'Not found Here':
                pass

    return formatted_counties


def write_the_counties_file():
    counties_file = open('counties_file.txt', 'w')
    counties_data = json.dumps(get_counties())
    counties_file.write(counties_data)
