def json_update(data, input_value, output_value, parent_node='', parents=['']):
    output_key = list(output_value.keys())[0]
    input_key = list(input_value.keys())[0]
    
    for key, value in data.items():
        # check key is equal to input key 
        if key == input_key and value == input_value[input_key] and \
                output_key in data.keys() and parent_node in parents:
            #
            data[output_key] = output_value[output_key]

        elif isinstance(value, list):
            for idx, item in enumerate(value):
                # check type dict
                if isinstance(item, dict):
                    update(item, input_value, output_value, parent_node, list(data.keys()))
                    
    return data
