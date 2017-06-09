MIN_LEN = 3

def test(entry):
    if 'title' not in entry:
        return {
            "passed": False,
            "error": "no title can be found"
        }
    else:
        title = entry["title"]
        if len(title.split(' ')) < MIN_LEN:
            return {
                "passed": False,
                "error": title
            }
        else:
           return { "passed": True }
