stations = {
    'required': ['name'],
    'all': ['name'],
}


trains = {
    'required': ['station_from_id', 'station_to_id', 'date_dep'],
}
trains['all'] = trains['required'] + ['time_dep', 'time_dep_till', 'another_ec', 'search']


coaches = {
    'required': ['station_from_id', 'station_to_id', 'date_dep', 'train', 'model', 'coach_type']
}
coaches['all'] = coaches['required'] + ['round_trip', 'another_ec']


def validate(data, fields_name):
    return all([attr in data for attr in globals()[fields_name]['required']])


def prepare_params(data, fields_name):
    request_params = {}
    for attr, val in data.items():
        if attr in globals()[fields_name]['all']:
            request_params[attr] = val
    return request_params
