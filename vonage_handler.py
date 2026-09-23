from vonage_voice import (
    NccoAction,
    Talk,
    Connect,
    Input,
    Dtmf,
    Speech,
    WebsocketEndpoint,
)
from config import settings
import json
from typing import List, Dict
import asyncio
from vonage import Vonage, Auth
from vonage_voice import CreateCallRequest, Phone, ToPhone


class VonageHandler:
    def __init__(self):
        self.client = Vonage(
            Auth(
                api_key=settings.vonage_api_key,
                api_secret=settings.vonage_api_secret,
                application_id=settings.vonage_application_id,
                private_key=settings.vonage_private_key_path,
            )
        )

    def build_welcome_menu_ncco(self) -> List[Dict]:
        """
        Build the welcome menu NCCO with IVR options
        Demonstrates: Effective IVR with self-service + escape routes
        """
        webhook = f"{settings.ngrok_url}/ivr/menu-selection"
        
        greeting = "Welcome to the pug information line. Press 1 or say 'learn about pugs' to hear more about this ancient dog breed. Press 2 or say 'pug care needs' to learn about how to care for a pug. Press 3 or say 'local pug rescues' if you are ready to adopt a pug."

        speech_input_context = ["learn about pugs", "pug care needs", "local pug rescues"]
        
        dtmf_options = Dtmf(maxDigits=1, timeOut=3)
        speech_options = Speech(language='en-US', endOnSilence=3, context=speech_input_context)

        ncco: list[NccoAction] = [
        Talk(text=greeting, language="en-US", style=11, bargeIn=True),
        Input(type=['dtmf', 'speech'], dtmf=dtmf_options, speech=speech_options, eventUrl=[webhook], eventMethod="POST")]
        # ncco = [
        #     {"action": "talk", "text": greeting, "style": 11, "bargeIn": True},
        #     {
        #         "action": "input",
        #         "type": ["dtmf"],
        #         "dtmf": {"maxDigits": 1, "timeOut": 3},
        #         "eventUrl": [webhook],
        #         "eventMethod": "POST",
        #     },
        # ]

        return [action.model_dump(by_alias=True, exclude_none=True) for action in ncco]
    
    def get_zip_code_ncco(self) -> List[Dict]:
        """
        Build the welcome menu NCCO with IVR options
        Demonstrates: Effective IVR with self-service + escape routes
        """
        webhook = f"{settings.ngrok_url}/ivr/menu-selection"
        
        greeting = "You selected local pug rescues. Please use the keypad to enter your zipcode followed by the pound key."

        
        dtmf_options = Dtmf(maxDigits=5, timeOut=5, submitOnHash=True)
        

        ncco: list[NccoAction] = [
        Talk(text=greeting, language="en-US", style=11, bargeIn=True),
        Input(type=['dtmf'], dtmf=dtmf_options, eventUrl=[webhook], eventMethod="POST")]
        # ncco = [
        #     {"action": "talk", "text": greeting, "style": 11, "bargeIn": True},
        #     {
        #         "action": "input",
        #         "type": ["dtmf"],
        #         "dtmf": {"maxDigits": 1, "timeOut": 3},
        #         "eventUrl": [webhook],
        #         "eventMethod": "POST",
        #     },
        # ]

        return [action.model_dump(by_alias=True, exclude_none=True) for action in ncco]
    
    def build_response_ncco(response_text):
        
        ncco: list[NccoAction] = [
        Talk(text=greeting, language="en-US", style=11, bargeIn=True),
        Input(type=['dtmf', 'speech'], dtmf=dtmf_options, speech=speech_options, eventUrl=[webhook], eventMethod="POST")]
        


    def build_customer_greeting_ncco(
        self,
        uuid: str,
        call_info: dict = None,
        department_info: str = None,
    ) -> List[Dict]:
        """
        Build personalized greeting for customer
        Demonstrates: CRM integration for personalization
        """

        greeting = "Unfortunately, we don't have any customer records associated with this number."

        # If the customer has an entry in the database
        if department_info:
            customer_name = call_info.get("customer")["name"]
            greeting = f"Hello {customer_name}, welcome back. The information you requested is as follows: {department_info}."

        greeting_ncco = [{"action": "talk", "text": greeting, "style": 11}]
        recording_ncco = self.build_recording_ncco(uuid)
        return greeting_ncco + recording_ncco

    def build_operator_greeting_ncco(
        self,
        uuid: str,
        call_info: dict = None,
    ) -> List[Dict]:
        """
        Build the operator greeting for customer
        Demonstrates: Escape route + customer follow up
        """

        greeting = "I'm sorry, all operators are currently busy. We will call you back in a moment when an operator becomes available."

        ncco = [
            {"action": "talk", "text": greeting, "style": 11},
        ]

        # Schedule callback in configured seconds
        from_number = call_info.get("from")
        asyncio.create_task(self.schedule_callback(from_number, uuid, call_info))

        return ncco

    def build_recording_ncco(self, uuid: str) -> list[Dict]:
        """
        Build the recording NCCO
        Demonstrates: Logging customer interactions in CRM
        """

        webhook = f"{settings.ngrok_url}/webhooks/recording?uuid={uuid}"

        greeting = "Thank you for calling. Please leave a message about the quality of this call. Press the pound key when you are done."

        ncco = [
            {"action": "talk", "style": 11, "text": greeting},
            {
                "action": "record",
                "endOnKey": "#",
                "beepStart": True,
                "endOnSilence": 3,
                "transcription": {
                    "eventUrl": [webhook],
                    "eventMethod": "POST",
                    "language": "en-US",
                },
            },
            {
                "action": "talk",
                "text": "Thank you for your message. Goodbye.",
                "style": 11,
            },
        ]

        return ncco

    async def schedule_callback(
        self, phone_number: str, uuid: str, call_info: dict = None
    ):
        """
        Simulate calling a customer back instead of making them wait on hold
        Demonstrates: Graceful error handling with follow-up contact
        """

        delay_seconds = 10
        try:
            print(f"Scheduling callback to {phone_number} in {delay_seconds} seconds")

            customer_name = call_info.get("customer")["name"]
            greeting = "Hello. We are calling you back."

            if customer_name:
                greeting = f"Hello {customer_name}. We are calling you back."

            # Wait for the specified delay
            for i in range(delay_seconds, 0, -1):
                print(f"Calling {phone_number} in {i} seconds ... ")
                await asyncio.sleep(1)

            ncco = [{"action": "talk", "text": greeting, "style": 11}]

            print(f"Now returning call to: ==> {phone_number}")

            call = CreateCallRequest(
                ncco=ncco,
                to=[ToPhone(number=phone_number)],
                from_=Phone(number=settings.vonage_virtual_number),
            )

            response = self.client.voice.create_call(call)

            return response.status

        except Exception as e:
            print(f"Error in callback scheduling: {str(e)}")

    def build_error_ncco(self) -> List[Dict]:
        """
        Build NCCO for error handling
        Demonstrates: Graceful error handling
        """

        greeting = "Sorry, I didn't understand that input. Please try again."
        greeting_ncco = [{"action": "talk", "text": greeting, "style": 11}]
        return greeting_ncco


vonage_handler = VonageHandler()
