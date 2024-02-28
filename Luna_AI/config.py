import json


def load_api(filepath=r'C:\Users\evryt\PycharmProjects\Luna_AI\.conf\config.json'):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data


class ApiConfig:
    config_data = load_api()

    @staticmethod
    def get_api_keys():
        api_keys = []
        key_filepath = ApiConfig.config_data['api_config']['key_filepath']
        with open(key_filepath, 'r') as file:
            for line in file:
                api_keys.append(line.strip())
        return api_keys
        # uses the configuration path for the API keys and returns the api keys to a list

    @staticmethod
    def get_application_path():
        app_filepath = ApiConfig.config_data['api_config']['application_paths']['applications']
        return app_filepath
        # returns file paths for all applications as a list

    @staticmethod
    def get_voiceID():
        voice_id = ApiConfig.config_data['api_config']['voice_id']
        return voice_id
        # returns the ElevenLabs voiceID

    @staticmethod
    def get_memory_filepath(key_high):
        try:
            return ApiConfig.config_data['api_config']['memory_filepath'][key_high]
        except KeyError:
            print(f'Key {key_high} not found in API configuration')
        # Memory File locations, returns the specific path based on the key_high input when calling the method

    @staticmethod
    def get_static_config(key_low, key_high):
        try:
            return ApiConfig.config_data['api_config']['static'][key_low][key_high]
        except KeyError:
            print(f'Keys, {key_low} & {key_high} not found in static configuration')
            # returns the static configuration values for GPT, Recognizer and Rand interaction

    @staticmethod
    def get_websearch_url():
        web_search = ApiConfig.config_data['api_config']['static']['web_search']
        return web_search

    @staticmethod
    def get_function_triggers(key_low, key_high):
        filepath = ApiConfig.config_data['api_config']['memory_filepath']['function_replies']
        with open(filepath, 'r') as file:
            data = json.load(file)
        function_triggers = data[key_low][key_high]
        return function_triggers

    @staticmethod
    def get_interactions(key_low, key_high):
        filepath = ApiConfig.config_data['api_config']['memory_filepath']['interactions']
        with open(filepath, 'r') as file:
            data = json.load(file)
        interactions = data[key_low][key_high]
        return interactions

    @staticmethod
    def get_memory_triggers(key_low, key_high):
        filepath = ApiConfig.config_data['api_config']['memory_filepath']['memories']
        with open(filepath, 'r') as file:
            data = json.load(file)
        memory_triggers = data[key_low][key_high]
        return memory_triggers


class LoadConfig:
    try:
        api_keys = ApiConfig.get_api_keys()
        voice_ID = ApiConfig.get_voiceID()

        gpt_version = ApiConfig.get_static_config('gpt_config', 'gpt_version')
        temperature = ApiConfig.get_static_config('gpt_config', 'temperature')
        max_tokens = ApiConfig.get_static_config('gpt_config', 'max_tokens')
        top_p = ApiConfig.get_static_config('gpt_config', 'top_p')
        freq_pen = ApiConfig.get_static_config('gpt_config', 'freq_pen')
        pres_pen = ApiConfig.get_static_config('gpt_config', 'pres_pen')

        threshold = ApiConfig.get_static_config('recognizer', 'threshold')

        web_search = ApiConfig.get_websearch_url()
        app_path = ApiConfig.get_application_path()

        luna_talks = ApiConfig.get_function_triggers('Conversation','triggers')

        tell_time = ApiConfig.get_function_triggers('Time Request', 'triggers')
        time_answer = ApiConfig.get_function_triggers('Time Request', 'response')

        open_app = ApiConfig.get_function_triggers('Open Request', 'triggers')
        app_name = ApiConfig.get_function_triggers('Open Request', 'applications')
        app_response = ApiConfig.get_function_triggers('Open Request', 'response')

        check_cal = ApiConfig.get_function_triggers('Calendar Request', 'triggers')
        cal_response = ApiConfig.get_function_triggers('Calendar Request', 'response')

        send_message = ApiConfig.get_function_triggers('Send Message', 'triggers')

        google_search = ApiConfig.get_function_triggers('Google Search', 'triggers')
        search_responses = ApiConfig.get_function_triggers('Google Search', 'responses')

        print('Configuration file loading...\n')

        print(f'Api keys: {api_keys}\n')
        print(f'voice ID: {voice_ID}\n')
        print(f'GPT settings: \ngpt version: {gpt_version}\ntemperature: {temperature}\nmax tokens: {max_tokens}\ntop p: '
              f'{top_p}\nfrequency penalty: {freq_pen}\npresistence penalty: {pres_pen}\n')
        print(f'Recorder Threshold: {threshold}\n')
        print(f'Web search URL: {web_search}\n')
        print(f'Application paths: {app_path}\n')
        print(f'Luna triggers loaded {luna_talks}\n{tell_time}\n{open_app}\n{check_cal}\n{send_message}\n{google_search}\n')
        print('Configuration loaded properly')
    except Exception as e:
        print(f'Configuration did not load properly: {e}')
