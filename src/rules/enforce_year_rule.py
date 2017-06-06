def test(entry):
    if 'year' not in entry:
        return {
            "passed": False,
            "error": "item does not have year specified"
        }
    else:
        return { "passed": True }
