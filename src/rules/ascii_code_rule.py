def __is_ascii(string):
    return all(ord(c) < 128 for c in string)

def test(entry):
    for value in entry.values():
        if not __is_ascii(value):
            return {
                "passed": False,
                "error": "non-ascii characaters detected in " + value
            }

    return { "passed": True }
