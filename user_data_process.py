def get_social_networks(social_networks):
    if social_networks is None:
        return None
    if len(social_networks) == 0:
        return None

    for social_network in social_networks:
        if social_network['type'] == 'LINKEDIN':
            return f"https://www.linkedin.com/in/{social_network['profile']}"
    return None

def process_field_value(field_value):
    # print(field_value)
    key = field_value['name']
    value = None

    if "value" in field_value:
        value = field_value['value']
        return key, value
    elif "values" in field_value:
        values = field_value['values']
        if values is None:
            return key, None
        value_str = ""
        for value in values:
            value_str += value['text'] + ", "
        value_str = value_str[:-2]
        return key, value_str
    else:
        return key, None
    

    return key, value_str

def process_user_data(response, user_id):
    person = response['data']['person']
    
    user_dict = {}
    user_dict['name'] = f"{person['firstName']} {person['lastName']}"   
    user_dict['organization'] = person['organization']
    user_dict['job_title'] = person['jobTitle'] if person['jobTitle'] is not None else None
    user_dict['biography'] = person['biography']
    user_dict['email'] = person['email'] if person['email'] is not None else None
    user_dict['website_url'] = person['websiteUrl']
    user_dict['connection_status'] = person['userInfo']['connectionStatus']
    user_dict['has_sent_request'] = person['userInfo']['hasSentRequest']
    user_dict['linkedin_url'] = get_social_networks(person['socialNetworks'])
    user_dict['mobile_phone'] = person['mobilePhone']
    user_dict['user_id'] = user_id
    
    for field_value in person['withEvent']['fields']:
        key, value = process_field_value(field_value)
        user_dict[key] = value

    return user_dict
