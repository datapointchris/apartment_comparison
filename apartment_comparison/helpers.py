FEATURE_TYPE_MAP = {
    'id': 'integer',
    'name': 'text',
    'address': 'text',
    'url': 'text',
    'year': 'integer',
    'rent': 'integer',
    'sqft': 'integer',
    'price_per': 'integer',
    'pet_rent': 'integer',
    'pet_deposit': 'integer',
    'fees': 'integer',
    'dishwasher': 'boolean',
    'washer_dryer': 'text',
    'countertops': 'text',
    'floor_level': 'integer',
    'dog_walking': 'integer',
    'dog_park': 'boolean',
    'groceries': 'integer',
    'costco': 'integer',
    'gym': 'integer',
    'apt_gym': 'integer',
    'quiet_ac': 'boolean',
    'ac_filter_can_change': 'boolean',
    'parking': 'integer',
    'smart_thermostat': 'boolean',
    'electronic_lock': 'boolean',
    'trails': 'integer',
    'bike_lanes': 'integer',
    'to_work': 'integer',
    'toll_road': 'boolean',
    'walk_in_closet': 'boolean',
    'ceiling_fans': 'boolean',
    'guest_parking': 'integer',
    'notes': 'text'
}


def convert_data_types_from_strings(info, mapping):
    converted = {}
    for k, v in info.items():
        if v == '' or v is None:
            converted[k] = None
        else:
            data_type = mapping.get(k)
            match data_type:
                case 'integer':
                    converted[k] = int(v)
                case 'text':
                    converted[k] = v.strip()
                case 'boolean':
                    converted[k] = int(v)

    return converted