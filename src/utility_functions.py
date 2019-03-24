import inspect

def get_props(c, filter_values = []):
    props = {}
    query_key = None
    for (k, v) in c.__dict__.items():
        if k == 'key':
            query_key = v
        if k[:2] != '__' and not inspect.isroutine(v) and k not in filter_values: 
            props[k] =  c.__dict__[k] 
    return (query_key, list(props.keys()))
