import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, vnode_count=100):
        self.vnode_count = vnode_count
        self.ring = []
        self.vnode_map = {}  # hash → server_id

    def _hash(self, key):
        return int(hashlib.sha1(key.encode()).hexdigest(), 16) % (2**32)

    def add_server(self, server_id):
        for i in range(self.vnode_count):
            vnode_key = f"{server_id}-vnode-{i}"
            h = self._hash(vnode_key)
            self.vnode_map[h] = server_id
            bisect.insort(self.ring, h)

    def remove_server(self, server_id):
        for i in range(self.vnode_count):
            vnode_key = f"{server_id}-vnode-{i}"
            h = self._hash(vnode_key)
            if h in self.vnode_map:
                self.ring.remove(h)
                del self.vnode_map[h]

    def get_server(self, key):
        h = self._hash(key)
        idx = bisect.bisect(self.ring, h) % len(self.ring)
        vnode_hash = self.ring[idx]
        return self.vnode_map[vnode_hash]

# Example usage
ring = ConsistentHashRing()
ring.add_server("A")
ring.add_server("B")
ring.add_server("C")

print(ring.get_server("airpods"))
print(ring.get_server("laptop"))
