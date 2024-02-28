import json


def load_api(filepath=r'config path here'): # Put your own config path here and it'll load the config.
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
    # returns the web search URL

    @staticmethod
    def get_function_triggers(key_low, key_high):
        filepath = ApiConfig.config_data['api_config']['memory_filepath']['function_replies']
        with open(filepath, 'r') as file:
            data = json.load(file)
        function_triggers = data[key_low][key_high]
        return function_triggers
    # depending on what you need, this basically is used to run the functions, check LoadConfig for more information

    @staticmethod
    def get_interactions(key_low, key_high):
        filepath = ApiConfig.config_data['api_config']['memory_filepath']['interactions']
        with open(filepath, 'r') as file:
            data = json.load(file)
        interactions = data[key_low][key_high]
        return interactions
    # not yet implemented, those are basically unprompted interactions that Luna will have with you

    @staticmethod
    def get_memory_triggers(key_low, key_high):
        filepath = ApiConfig.config_data['api_config']['memory_filepath']['memories']
        with open(filepath, 'r') as file:
            data = json.load(file)
        memory_triggers = data[key_low][key_high]
        return memory_triggers
    # Not yet implemented, I'll be trying to build a memory retention and recall system for luna, allowing her to 'remember' people, situations, feelings, etc


class LoadConfig:
    try:
        api_keys = ApiConfig.get_api_keys()
        voice_ID = ApiConfig.get_voiceID()
        # api keys and the ID of Luna's voice

        gpt_version = ApiConfig.get_static_config('gpt_config', 'gpt_version')
        temperature = ApiConfig.get_static_config('gpt_config', 'temperature')
        max_tokens = ApiConfig.get_static_config('gpt_config', 'max_tokens')
        top_p = ApiConfig.get_static_config('gpt_config', 'top_p')
        freq_pen = ApiConfig.get_static_config('gpt_config', 'freq_pen')
        pres_pen = ApiConfig.get_static_config('gpt_config', 'pres_pen')
        # GPT settings, those are what make luna sound like she does

        threshold = ApiConfig.get_static_config('recognizer', 'threshold')
        # Microphone threshold, nothing important unless you have a shit mic

        web_search = ApiConfig.get_websearch_url()
        app_path = ApiConfig.get_application_path()
        # Web search URL and thep aths to applications are assigned here

        luna_talks = ApiConfig.get_function_triggers('Conversation', 'triggers')
        # Triggers to luna just responding to your speech are assigned to luna_talks

        tell_time = ApiConfig.get_function_triggers('Time Request', 'triggers')
        time_answer = ApiConfig.get_function_triggers('Time Request', 'response')
        # Lunas functionality to tell the time is dependent on these

        open_app = ApiConfig.get_function_triggers('Open Request', 'triggers')
        app_name = ApiConfig.get_function_triggers('Open Request', 'applications')
        app_response = ApiConfig.get_function_triggers('Open Request', 'response')
        # This is one of the AI's most powerful functions in my opinion, it opens apps as a subprocess based on the app_name index, it's a very sexy piece of code
        # The values above represent the trigger words for the functionality, the app names and the responses she uses when launching them (She generated those herself

        check_cal = ApiConfig.get_function_triggers('Calendar Request', 'triggers')
        cal_response = ApiConfig.get_function_triggers('Calendar Request', 'response')
        # Triggers and responses for checking the calendar are assigned in this part

        send_message = ApiConfig.get_function_triggers('Send Message', 'triggers')
        # Triggers to send a message are assigned here

        google_search = ApiConfig.get_function_triggers('Google Search', 'triggers')
        search_responses = ApiConfig.get_function_triggers('Google Search', 'responses')
        # Google search triggers and responses are assigned here

        # The whole below section is JUST for debuging purposes. It prints out all the assigned values and throws an exception if one of the values did not assign correctly.
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
