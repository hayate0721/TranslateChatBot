import boto3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Language code mapping
LANGUAGE_CODE_MAPPING = {
    'Japanese': 'ja',
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',

}

def lambda_handler(event, context):
    try:
        translate = boto3.client('translate')
        
        # Extract slots
        language_name = event['sessionState']['intent']['slots']['Language']['value']['interpretedValue']
        text_to_translate = event['sessionState']['intent']['slots']['Text']['value']['interpretedValue']
        
        # Validate and map language code
        language_code = LANGUAGE_CODE_MAPPING.get(language_name)
        if not language_code:
            raise ValueError(f"Unsupported language: {language_name}")
        if not text_to_translate:
            raise ValueError("Text to translate must be provided.")
        
        logging.info(f"Translating text '{text_to_translate}' to language '{language_name}' (code: '{language_code}')")
        
        # Perform translation
        result = translate.translate_text(
            Text=text_to_translate,
            SourceLanguageCode='auto',
            TargetLanguageCode=language_code
        )
        
        translated_text = result['TranslatedText']
        
        # Construct the response
        return {
            'sessionState': {
                'dialogAction': {
                    'type': 'Close'
                },
                'intent': {
                    'name': 'TranslateText',
                    'slots': {
                        'Language': {
                            'value': {
                                'originalValue': language_name,
                                'interpretedValue': language_name
                            }
                        },
                        'Text': {
                            'value': {
                                'originalValue': text_to_translate,
                                'interpretedValue': translated_text
                            }
                        }
                    },
                    'state': 'Fulfilled', 
                    'confirmationState': 'None'
                },
                'sessionAttributes': {}
            },
            'messages': [
                {
                    'contentType': 'PlainText',
                    'content': f'{translated_text}'
                }
            ]
        }
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return {
            'sessionState': {
                'dialogAction': {
                    'type': 'Close'
                },
                'intent': {
                    'name': 'TranslateText',
                    'slots': {
                        'Language': {
                            'value': {
                                'originalValue': language_name,
                                'interpretedValue': language_name
                            }
                        },
                        'Text': {
                            'value': {
                                'originalValue': text_to_translate,
                                'interpretedValue': ''
                            }
                        }
                    },
                    'state': 'Failed',
                    'confirmationState': 'None'
                },
                'sessionAttributes': {}
            },
            'messages': [
                {
                    'contentType': 'PlainText',
                    'content': f'An error occurred: {str(e)}'
                }
            ]
        }
