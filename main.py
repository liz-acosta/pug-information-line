from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from vonage_handler import (
    build_welcome_menu_ncco,
    build_response_ncco,
    get_zip_code_ncco,
    build_error_ncco,
)
from ivr_handlers import dtmf_response, speech_response, find_pug_rescues


from config import settings
from pug_information import RESCUE_INPUTS

app = FastAPI(title="Customer Service Call Flow API")


# Webhook: Answer the call
@app.get("/answer")
async def incoming_call(request: Request):
    """
    Handle incoming call
    """
    try:
        data = request.query_params

        print(f"INCOMING CALL: ===> {data}")

        # Build the welcome menu NCCO
        ncco = build_welcome_menu_ncco()

        return ncco

    except Exception as e:
        print(f"Error handling incoming call: {str(e)}")
        ncco = build_error_ncco()
        return ncco


# Webhook: Call status events
@app.post("/event")
async def event(request: Request):
    data = await request.json()
    print(f"Call event: {data.get('status', 'unknown')} | UUID: {data.get('uuid')}")
    return JSONResponse(content={"status": "ok"})


# Webhook: Handle the IVR menu selection
@app.post("/ivr/menu-selection")
async def handle_dtmf(request: Request):
    """
    Handle DTMF or speech input from IVR menu
    """

    try:
        print("Routing call to menu selection ... ")

        data = await request.json()
        dtmf_digits = data.get("dtmf", {}).get("digits")
        speech_results = data.get("speech", {}).get("results", [])

        if dtmf_digits:
            print(f"CALLER INPUT IS DTMF: ===> {dtmf_digits}")
            if dtmf_digits == "3":
                print("Caller requested local pug rescues, getting zip code now ... ")
                ncco = get_zip_code_ncco()
                return ncco
            elif len(dtmf_digits) == 5:
                response_text = find_pug_rescues(dtmf_digits)
            else:
                response_text = dtmf_response(dtmf_digits)

        elif speech_results:
            print(f"CALLER INPUT IS SPEECH: ===> {speech_results}")
            if any(
                word in speech_results[0].get("text", "").lower()
                for word in RESCUE_INPUTS
            ):
                print("Caller requested local pug rescues, getting zip code now ... ")
                ncco = get_zip_code_ncco()
                return ncco
            else:
                response_text = speech_response(speech_results)

        else:
            print("ERROR: Unrecognized input")
            raise ValueError(f"Unrecognized caller input")

        ncco = build_response_ncco(response_text)

        return ncco

    except Exception as e:
        print(f"Error handling caller input: {str(e)}")
        error_ncco = build_error_ncco()
        main_menu_necco = build_welcome_menu_ncco()
        return error_ncco + main_menu_necco


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
    )
