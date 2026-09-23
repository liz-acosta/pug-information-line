import pug_information

def dtmf_response(caller_input: str) -> str:
    response_text = pug_information.DTMF_RESPONSES.get(caller_input, pug_information.FALLBACK_RESPONSE)
    return response_text

def speech_response(caller_input: list) -> str:
    transcript = caller_input[0].get("text", "").lower()
    for keyword, response in pug_information.SPEECH_RESPONSES.items():
        if keyword in transcript:
            response_text = response
            return response_text
        else:
            return pug_information.FALLBACK_RESPONSE 

def find_pug_rescues(zip_code: str) -> str:
    """
    Return a plain-English summary of pug rescues near zip_code
    Uses a hardcoded regional lookup keyed by the first digit of the zip —
    reliable for live demos with no external API dependency
    """
    zip_clean = zip_code.strip().replace(" ", "")
    region = zip_clean[0] if zip_clean and zip_clean[0].isdigit() else None
    rescues = pug_information.PUG_RESCUES_BY_REGION.get(region, pug_information.DEFAULT_RESCUES)

    lines = [
        f"{name} in {city}, {state} — {phone}" for name, city, state, phone in rescues
    ]
    summary = "; ".join(lines)

    pug_rescue_result = (
        f"Great news! I found {len(rescues)} pug rescue organizations near {zip_code}: "
        f"{summary}. I'd recommend calling ahead — availability changes quickly, "
        "and they can tell you about any pugs coming in soon too."
    )

    return pug_rescue_result

def handle_caller_input(input_data):

    response = pug_information.FALLBACK_RESPONSE

    dtmf_digits = input_data.get("dtmf", {}).get("digits")
    speech_results = input_data.get("speech", {}).get("results", [])

    rescue_inputs = ["local", "pug", "rescues"]

    if dtmf_digits == "3" or speech_results in rescue_inputs:
        response = 
    

    if dtmf_digits:
        response = dtmf_response(dtmf_digits)

    elif speech_results:
        response = speech_response(speech_results)

    return response