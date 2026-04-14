from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from vonage_handler import vonage_handler
from vonage import Vonage, Auth
from vonage_voice import CreateCallRequest
from database import db
import requests
from config import settings
import asyncio
from datetime import datetime
from vonage_jwt.jwt import JwtClient

app = FastAPI(title="Customer Service Call Flow API")

# In-memory store for active calls (for demo purposes)
active_calls = {}

# Department mapping for DTMF selections
DEPARTMENT_MAP = {"1": "billing", "2": "support", "3": "account", "0": "operator"}

DEPARTMENT_KEYS = {
    "billing": "billing_info",
    "support": "support_notes",
    "account": "support_notes",
}


@app.get("/voice/incoming")
async def incoming_call(request: Request):
    """
    Handle incoming call.
    Demonstrates: Initial IVR menu + graceful error handling
    """
    try:
        body = request.query_params
        from_number = body.get("from")
        to_number = body.get("to")
        uuid = body.get("uuid")

        print(f"INCOMING CALL: ===> {body}")

        # Store call info
        active_calls[uuid] = {
            "from": from_number,
            "to": to_number,
            "start_time": datetime.now(),
            # Get customer data if it is in the database, returns None if not in database
            "customer": db.get_customer_by_phone(from_number),
        }
        print(f"STORING CALL INFO: ===> {active_calls[uuid]}")

        # Build the welcome menu NCCO
        ncco = vonage_handler.build_welcome_menu_ncco()

        return JSONResponse(content=ncco)

    except Exception as e:
        print(f"Error handling incoming call: {str(e)}")
        ncco = vonage_handler.build_error_ncco()
        return JSONResponse(content=ncco)


@app.post("/ivr/menu-selection")
async def handle_dtmf(request: Request):
    """
    Handle DTMF input from IVR menu.
    Demonstrates: Skills-based routing + escape routes for complex calls
    """

    try:
        print("Routing call to menu selection ... ")

        body = await request.json()
        dtmf = body.get("dtmf").get("digits")
        uuid = body.get("uuid")
        department = DEPARTMENT_MAP[dtmf]

        print(f"MENU SELECTION: ===>  {dtmf}")
        print(f"DTMF INPUT: ===>  {dtmf} for call: ===> {uuid}")
        print(f"DEPARTMENT: ===> {department}")

        # Validate DTMF input
        if dtmf not in DEPARTMENT_MAP:
            print(f"Invalid DTMF: {dtmf}")
            ncco = vonage_handler.build_error_ncco()
            return JSONResponse(content=ncco)

        # Get call info from in-memory
        call_info = active_calls.get(uuid, {})
        customer = call_info.get("customer")
        # Add the selected department to the call info
        active_calls[uuid]["department"] = department

        print(f"EXISTING CUSTOMER INFO: ===> {customer}")

        # If caller selects OPERATOR, build operator greeting, which will also schedule a call back
        if department == "operator":
            print(f"Operator requested by: ===> {call_info.get('from')}")
            ncco = vonage_handler.build_operator_greeting_ncco(uuid, call_info)
            return JSONResponse(content=ncco)

        # Route to department
        if customer:
            # Personalized routing with CRM integration
            print(
                f"Routing known customer: ===> {customer['name']} to department: ===> {department}"
            )

            # Get the customer data related to selected department
            active_calls[uuid]["customer_id"] = customer["id"]
            department_key = DEPARTMENT_KEYS.get(department, "support_notes")
            department_info = customer.get(department_key, "account information")
            ncco = vonage_handler.build_customer_greeting_ncco(
                uuid, call_info, department_info
            )

        else:
            # General routing
            print(f"Routing call to: ===> {department}")
            ncco = vonage_handler.build_customer_greeting_ncco(uuid, call_info)

        return JSONResponse(content=ncco)

    except Exception as e:
        print(f"Error handling DTMF: {str(e)}")
        ncco = vonage_handler.build_error_ncco()
        return JSONResponse(content=ncco)


@app.post("/webhooks/recording")
async def handle_recording(request: Request):
    """
    Handle recording completion and transcription.
    Demonstrates: CRM logging of interactions + error handling
    """

    try:
        print("Handling message recording ... ")

        body = await request.json()
        uuid = request.query_params.get("uuid")
        transcription_url = body.get("transcription_url")

        # Get call info from in-memory
        call_info = active_calls.get(uuid, {})
        phone_number = call_info["from"]

        print(f"Transcription obtained for call from: ===> {phone_number}")
        print("TRANSCRIPTION URL: ===> ", transcription_url)

        # Get customer from database if entry exists, otherwise this returns None
        customer = db.get_customer_by_phone(phone_number)
        print(f"CUSTOMER IN DATABASE: ===> {customer}")

        if transcription_url:

            # Get the transcription
            jwt_client = JwtClient(
                application_id=settings.vonage_application_id,
                private_key=settings.vonage_private_key_path,
            )
            jwt_token = jwt_client.generate_application_jwt()

            response = requests.get(
                transcription_url,
                headers={"Authorization": f"Bearer {jwt_token.decode()}"},
            )

            # Get transcription
            transcription_data = response.json()

            for channel in transcription_data.get("channels", []):
                for segment in channel.get("transcript", []):
                    sentence = segment.get("sentence")
                    transcription = sentence

            # If the customer is in the database, make an entry of this interaction
            if customer:
                department = call_info["department"]

                # Log the interaction
                interaction_id = db.log_interaction(
                    customer_id=customer["id"],
                    call_type=department,
                    message="Customer left voicemail",
                    transcription=transcription,
                    agent_name="IVR System",
                )

                print(
                    f"Logged interaction: ===> {interaction_id} for customer: ===> {customer["id"],}"
                )

            else:
                # If customer is not in the database, add them
                result = db.insert_customer_and_log_interaction(
                    phone_number=call_info.get("from"),
                    call_type=department,
                    support_notes="New customer",
                    transcription=transcription,
                )

                print(
                    f"Created customer {result['customer_id']} with interaction {result['interaction_id']}"
                )

        return JSONResponse(content={"status": "recorded"})

    except Exception as e:
        print(f"Error handling recording: {str(e)}")
        return JSONResponse(
            content={"status": "error", "message": str(e)}, status_code=500
        )


async def schedule_callback(
    phone_number: str, original_uuid: str, delay_seconds: int = 60
):
    """
    Schedule a callback to the customer after delay.
    Demonstrates: Graceful error handling with follow-up contact.
    """

    try:
        print(
            f"Scheduling callback to: ===> {phone_number} in: ===> {delay_seconds} seconds"
        )
        customer = db.get_customer_by_phone(phone_number)

        if customer:
            greeting = f"Hello {customer["name"]}. We are calling you back. You can hang up now."
        else:
            greeting = "Hello. We are calling you back. You can hang up now."

        # Wait for the specified delay
        for i in range(delay_seconds, 0, -1):
            print(f"Calling {phone_number} in {i} seconds ... ")
            await asyncio.sleep(1)

        client = Vonage(
            Auth(
                api_key=settings.vonage_api_key,
                api_secret=settings.vonage_api_secret,
                application_id=settings.vonage_application_id,
                private_key=settings.vonage_private_key_path,
            )
        )

        ncco = [
            {
                "action": "talk",
                "text": greeting,
                "language": "en-US",
                "voice_name": "Amy",
            }
        ]

        call = CreateCallRequest(
            to=[{"type": "phone", "number": phone_number}],
            ncco=ncco,
            random_from_number=True,
        )

        client.voice.create_call(call)

    except Exception as e:
        print(f"Error in callback scheduling: {str(e)}")


@app.on_event("startup")
async def startup_event():
    """Initialize database and log startup."""
    print("Application starting up")
    print(f"Database path: {settings.database_path}")
    print(f"Callback base URL: {settings.callback_base_url}")
    print("Sample customers seeded into database")


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown."""
    print("Application shutting down")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
    )
