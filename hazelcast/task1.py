import hazelcast


if __name__ == "__main__":
    # Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
    hz = hazelcast.HazelcastClient()

    # Create Distributed Map
    map = hz.get_map("distributed_map1").blocking()
    for i in range(1, 1001):
        map.put(i, "value" + str(i))

    # Shutdown this Hazelcast Client
    hz.shutdown()
