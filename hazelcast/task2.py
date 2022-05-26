import hazelcast
from multiprocessing import Process


def racy_update(number):
    client = hazelcast.HazelcastClient()
    distributed_map = client.get_map("distributed_map2").blocking()

    key = "1"
    distributed_map.put(key, 0)

    print(f"Process #{number}. Starting...")
    for k in range(0, 1000):
        if k % 100 == 0:
            print(f"Process #{number}. At -> {k}")

        value = distributed_map.get(key)
        value += 1
        distributed_map.put(key, value)

    print(f"Process #{number}. Finished! Result -> {distributed_map.get(key)}")


def pessimistic_update(number):
    client = hazelcast.HazelcastClient()
    distributed_map = client.get_map("distributed_map2").blocking()

    key = "1"
    distributed_map.put(key, 0)

    print(f"Process #{number}. Starting...")
    for i in range(1000):
        distributed_map.lock(key)
        try:
            value = distributed_map.get(key)
            value += 1
            distributed_map.put(key, value)
        finally:
            distributed_map.unlock(key)

    print(f"Process #{number}. Finished! Result -> {distributed_map.get(key)}")


def optimistic_update(number):
    client = hazelcast.HazelcastClient()
    distributed_map = client.get_map("distributed_map2").blocking()

    key = "1"
    distributed_map.put(key, 0)

    print(f"Process #{number}. Starting...")
    for k in range(0, 1000):
        if k % 10 == 0:
            print(f"Process #{number}. At -> {k}")

        while True:
            old_value = distributed_map.get(key)
            new_value = old_value
            new_value += 1
            if distributed_map.replace_if_same(key, old_value, new_value):
                break

    print(f"Process #{number}. Finished! Result -> {distributed_map.get(key)}")


if __name__ == '__main__':
    numbers = [1, 2, 3]
    procs = []

    for index, number in enumerate(numbers):
        proc = Process(target=racy_update, args=(number,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
