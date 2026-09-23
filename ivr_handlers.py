import pug_information


def dtmf_response(caller_input: str) -> str:
    print(f"CALLER INPUT IS DTMF: ===> {caller_input}")
    response_text = pug_information.DTMF_RESPONSES.get(caller_input)
    return response_text + pug_information.FAREWELL


def speech_response(caller_input: list) -> str:
    print(f"CALLER INPUT IS SPEECH: ===> {caller_input}")
    transcript = caller_input[0].get("text", "").lower()
    for keyword, response in pug_information.SPEECH_RESPONSES.items():
        if keyword in transcript:
            response_text = response
            return response_text + pug_information.FAREWELL


def find_pug_rescues(zip_code: str) -> str:
    """
    Return a plain-English summary of pug rescues near zip_code
    Uses a hardcoded regional lookup keyed by the first digit of the zip —
    reliable for live demos with no external API dependency
    """
    zip_clean = zip_code.strip().replace(" ", "")
    region = zip_clean[0] if zip_clean and zip_clean[0].isdigit() else None
    rescues = pug_information.PUG_RESCUES_BY_REGION.get(
        region, pug_information.DEFAULT_RESCUES
    )

    lines = [
        f"{name} in {city}, {state} — {phone}" for name, city, state, phone in rescues
    ]
    summary = "; ".join(lines)

    pug_rescue_result = (
        f"Great news! I found {len(rescues)} pug rescue organizations near {zip_code}: "
        f"{summary}. I'd recommend calling ahead — availability changes quickly, "
        "and they can tell you about any pugs coming in soon too."
        + pug_information.FAREWELL
    )

    return pug_rescue_result
