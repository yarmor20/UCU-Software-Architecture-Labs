import hazelcast
import threading

client = hazelcast.HazelcastClient()
queue = client.get_queue("queue_v2.0").blocking()


def produce():
    for i in range(105):
        value = "value-" + str(i)
        queue.put(value)
        print(value)


if __name__ == '__main__':
    producer_thread = threading.Thread(target=produce)
    producer_thread.start()
    producer_thread.join()

    client.shutdown()
