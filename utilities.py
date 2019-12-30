import bs4

def get_data(body, config, recursive = True):
    result = body
    for ancestor in config['path']:
        result = result.find(ancestor['selector'], ancestor['options'])
    if (result):
        return result.findAll(config['selector'], config['options'], recursive = recursive)
    return []

def scrape(resp, queue, visited, body_config, nav_config, data_config):
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')

    posts = get_data(soup, body_config, False)

    data = []
    for post in posts:
        post_data = {}
        for field in data_config.keys():
            results = get_data(post, data_config[field])
            if results:
                attribute = data_config[field]['attribute']
                raw_data = [ result.text for result in results if result ] if attribute == 'text' else [ result[attribute] for result in results if result ]
                post_data[field] = raw_data if not 'transform' in data_config[field] else data_config[field]['transform'](raw_data)
        if (post_data):
            data.append(post_data)

    nav = get_data(soup, nav_config)
    for item in nav:
        link = item[nav_config['attribute']]
        if not link in visited:
            visited.add(link)
            queue.put(link)
    
    return data
