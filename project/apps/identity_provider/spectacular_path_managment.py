def custom_preprocessing_hook(endpoints):
    filtered = []
    for (path, path_regex, method, callback) in endpoints:
        # Remove all but DRF API endpoints
        if path.startswith("/openid/"):
            filtered.append((path, path_regex, method, callback))
    return filtered