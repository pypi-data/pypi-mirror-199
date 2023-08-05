def parse_id(url):
    return url.split("/")[-1]


def parse_embedded_id(raw_data, entity_type):
    url = raw_data["_links"][entity_type]["href"]
    return parse_id(url)


def parse_link(data, path):
    loc = data["_links"]
    for key in path.split("."):
        loc = loc[key]
    return loc["href"]
