import pylibmc

from sparta.memcached.base import SpartaCache


class SpartaCacheWrapper(SpartaCache):
    """
    Wrapper around pylibmc.Client to support key_prefix.
    Also see https://github.com/memcached/memcached/wiki/Commands.
    """

    def __init__(
        self,
        client: pylibmc.Client,
        key_prefix: str,
    ):
        super().__init__(key_prefix)
        self.client = client

    def __repr__(self):
        return "<%s for %s>" % (self.__class__.__name__, self.client)

    def __str__(self):
        return "<%s for %s>" % (self.__class__.__name__, self.client)

    def __getitem__(self, key):
        return self.client.__getitem__(self.map_key(key))

    def __setitem__(self, key, value):
        return self.client.__setitem__(self.map_key(key), value)

    def __delitem__(self, key):
        return self.client.__delitem__(self.map_key(key))

    def __contains__(self, key):
        return self.client.__contains__(self.map_key(key))

    def add(self, key, *args, **kwargs):
        return self.client.add(self.map_key(key), *args, **kwargs)

    def append(self, key, *args, **kwargs):
        return self.client.append(self.map_key(key), *args, **kwargs)

    def cas(self, key, *args, **kwargs):
        return self.client.cas(self.map_key(key), *args, **kwargs)

    def decr(self, key, *args, **kwargs):
        return self.client.decr(self.map_key(key), *args, **kwargs)

    def delete(self, key, *args, **kwargs):
        return self.client.delete(self.map_key(key), *args, **kwargs)

    def get(self, key, *args, **kwargs):
        return self.client.get(self.map_key(key), *args, **kwargs)

    def gets(self, key, *args, **kwargs):
        return self.client.gets(self.map_key(key), *args, **kwargs)

    def incr(self, key, *args, **kwargs):
        return self.client.incr(self.map_key(key), *args, **kwargs)

    def prepend(self, key, *args, **kwargs):
        return self.client.prepend(self.map_key(key), *args, **kwargs)

    def replace(self, key, *args, **kwargs):
        return self.client.replace(self.map_key(key), *args, **kwargs)

    def set(self, key, *args, **kwargs):
        return self.client.set(self.map_key(key), *args, **kwargs)

    def touch(self, key, *args, **kwargs):
        return self.client.touch(self.map_key(key), *args, **kwargs)
