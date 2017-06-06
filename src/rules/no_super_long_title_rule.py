def test(entry):
    if 'title' not in entry:
        return {
            "passed": False,
            "error": "no title can be found"
        }
    else:
        title = entry["title"]
        if len(title.split(' ')) > 20:
            return {
                "passed": False,
                "error": title
            }
        else:
           return { "passed": True }
