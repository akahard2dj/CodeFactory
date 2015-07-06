class LRUCache:

    # @param capacity, an integer
    def __init__(self, capacity):
        self.cache = collections.OrderedDict()
        self.capacity = capacity
        
    # @return an integer
    def get(self, key):
        val = -1
        if key in self.cache:
            val = self.cache[key]
            del self.cache[key]
            self.cache[key] = val
        return val;
        

    # @param key, an integer
    # @param value, an integer
    # @return nothing
    def set(self, key, value):
        if key in self.cache:
            del self.cache[key]
        else:
            if len(self.cache)==self.capacity:
                for keyTemp in self.cache:
                    del self.cache[keyTemp]
                    break
        self.cache[key] = value
