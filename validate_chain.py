def is_response_valid(response) -> tuple[bool, list[str]]:
    errors = []

    # Must be dict
    if not isinstance(response, dict):
        errors.append("Response is not a JSON object.")

    else:
        required_keys = ["concept", "analogy", "explanation", "key_takeaway"]

        for key in required_keys:
            if key not in response:
                errors.append(f"Missing key: {key}")

    # Optional word limit check (flatten values)
    if isinstance(response, dict):
        all_text = " ".join(str(v) for v in response.values())
        word_count = len(all_text.split())

        if word_count > 150:
            errors.append(f"Response too long ({word_count} words)")

    return (len(errors) == 0, errors)