import heapq

def dijkstra(graph, start):
    # Inisialisasi jarak ke semua node ke infinity
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0

    # Priority queue
    queue = [(0, start)]

    step = 1  # Buat hitung langkah

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        print(f"\nLangkah {step}:")
        print(f"Ambil node '{current_node}' dari queue dengan jarak {current_distance}.")

        # Jika jarak saat ini lebih besar dari jarak yang sudah dicatat, skip
        if current_distance > distances[current_node]:
            print(f"  --> Skip node '{current_node}', jaraknya lebih besar dari jarak yang sudah dicatat.")
            step += 1
            continue

        # Periksa semua tetangga dari current_node
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            print(f"  --> Cek tetangga '{neighbor}' (jarak saat ini: {distances[neighbor]}), jarak baru: {distance}")

            # Jika ditemukan jarak lebih pendek
            if distance < distances[neighbor]:
                print(f"    ! Update jarak ke '{neighbor}' dari {distances[neighbor]} ke {distance}")
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
            else:
                print(f"    ! Tidak perlu update jarak ke '{neighbor}'")

        step += 1

    return distances

# Contoh graf
graph = {
    '0': {'1': 2, '2': 6},
    '1': {'0': 2, '3': 5},
    '2': {'0': 6, '3': 8},
    '3': {'1': 5, '2': 8, '4': 10, '5': 15},
    '4': {'3': 10, '6': 2},
    '5': {'3': 15, '6': 6},
    '6': {'4': 2, '5': 6}
}

# Jalankan dari node '0'
start_node = '0'
distances = dijkstra(graph, start_node)

# Hasil akhir
print("\n=== Hasil Jarak Terpendek ===")
for node, distance in distances.items():
    print(f"{start_node} -> {node} = {distance}")
