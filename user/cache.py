from django.core.cache import caches,cache


def set_code(key,value,timeout):
    return cache.set(key,value,timeout)


def get_code(key):
    # print(f'{key} from get code')
    # print(f'{cache.get(key)} from getcod')
    return cache.get(key) 


# This function increase value by one
def incrKey(key, value, timeout=None):
    return caches['auth'].incr(key, delta=value)


# This function set value
def setKey(key, value, timeout=None):
    return caches['auth'].set(key , value, timeout=timeout)


# This function set value if key exist then give error
def addKey(key, value, timeout=None):
    return caches['auth'].add(key, value, timeout=timeout)


# this function get value by key
def getKey(key):
    return caches['auth'].get(key)


# this function delete value by key
def deleteKey(key):
    return caches['auth'].delete(key)


# this function delete value by pattern
def getAllKey(pattern):
    return caches['auth'].keys(pattern)