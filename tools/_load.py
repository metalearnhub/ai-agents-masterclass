import json
def load_source(path):
    """Accepts a get_page result saved to disk (raw dict, or the persisted [{'type':'text','text':...}] wrapper)."""
    d=json.load(open(path))
    if isinstance(d,list): d=json.loads(d[0]['text'])
    return d['source'] if 'source' in d else d
