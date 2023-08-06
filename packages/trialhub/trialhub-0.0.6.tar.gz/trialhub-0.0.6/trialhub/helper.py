import itertools

# A helper function to break an iterable into chunks of size batch_size.
def chunks(iterable, batch_size=100):        
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))