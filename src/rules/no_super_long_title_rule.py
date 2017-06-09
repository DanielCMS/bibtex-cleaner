MAX_LEN = 20

def test(entry):
    if 'title' not in entry:
        return {
            "passed": False,
            "error": "no title can be found"
        }
    else:
        title = entry["title"]
        if len(title.split(' ')) > MAX_LEN:
            return {
                "passed": False,
                "error": title
            }
        else:
           return { "passed": True }
