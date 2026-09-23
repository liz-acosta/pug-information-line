from vonage_voice import (
    NccoAction,
    Talk,
    Input,
    Dtmf,
    Speech,
)
from config import settings

from typing import List, Dict


def build_welcome_menu_ncco() -> List[Dict]:
    """
    Build the welcome menu NCCO with IVR options
    """
    webhook = f"{settings.ngrok_url}/ivr/menu-selection"
    print(f"WEBHOOK IS: ===> {webhook}")
    print("Building welcome menu NCCO ... ")

    greeting = "Welcome to the pug information line. Press 1 or say 'learn about pugs' to hear more about this ancient dog breed. Press 2 or say 'pug care needs' to learn about how to care for a pug. Press 3 or say 'local pug rescues' if you are ready to adopt a pug."

    speech_input_context = ["learn about pugs", "pug care needs", "local pug rescues"]

    dtmf_options = Dtmf(maxDigits=1, timeOut=3)
    speech_options = Speech(
        language="en-US", endOnSilence=3, context=speech_input_context
    )

    ncco: list[NccoAction] = [
        Talk(text=greeting, language="en-US", style=11, bargeIn=True),
        Input(
            type=["dtmf", "speech"],
            dtmf=dtmf_options,
            speech=speech_options,
            eventUrl=[webhook],
            eventMethod="POST",
        ),
    ]

    return [action.model_dump(by_alias=True, exclude_none=True) for action in ncco]


def get_zip_code_ncco() -> List[Dict]:
    """
    Build the NCCO to get the zip code input to look up pug rescues
    """
    webhook = f"{settings.ngrok_url}/ivr/menu-selection"

    print("Building zip code NCCO ... ")

    greeting = "You selected local pug rescues. Please use the keypad to enter your zipcode followed by the pound key."

    dtmf_options = Dtmf(maxDigits=5, timeOut=5, submitOnHash=True)

    ncco: list[NccoAction] = [
        Talk(text=greeting, language="en-US", style=11, bargeIn=True),
        Input(type=["dtmf"], dtmf=dtmf_options, eventUrl=[webhook], eventMethod="POST"),
    ]

    return [action.model_dump(by_alias=True, exclude_none=True) for action in ncco]


def build_response_ncco(response_text):
    """
    Build the response NCCO
    """

    ncco: list[NccoAction] = [
        Talk(
            text=response_text,
            language="en-US",
            style=11,
        ),
    ]

    return [action.model_dump(by_alias=True, exclude_none=True) for action in ncco]


def build_error_ncco() -> List[Dict]:
    """
    Build NCCO for error handling
    """

    print("Building error NCCO ... ")

    greeting = "Sorry, I didn't understand that input. Please try again."

    ncco: list[NccoAction] = [
        Talk(
            text=greeting,
            language="en-US",
            style=11,
        ),
    ]

    return [action.model_dump(by_alias=True, exclude_none=True) for action in ncco]
