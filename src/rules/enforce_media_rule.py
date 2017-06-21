def test(entry):
    if 'booktitle' not in entry and 'journal' not in entry:
        return {
            "passed": False,
            "error": "item does not have media specified"
        }
    else:
        return { "passed": True }
