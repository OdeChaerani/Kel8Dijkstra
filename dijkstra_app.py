import streamlit as st
import heapq
import ast
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

def dijkstra_with_steps(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    queue = [(0, start)]
    visited_edges = []
    visited_nodes = set()
    step_data = []

    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        step_log = [f"✅ Memilih node '{current_node}' dari queue dengan jarak saat ini = {current_distance}."]
        visited_nodes.add(current_node)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                step_log.append(f"🔄 Update: {current_node} ➝ {neighbor}, jarak dari {distances[neighbor]} ➝ {distance}.")
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                visited_edges.append((current_node, neighbor))
            else:
                step_log.append(f"ℹ️ {current_node} ➝ {neighbor}, jarak tetap {distances[neighbor]} (karena < dari jarak yang dihitung melalui node saat ini).")

        # Visualisasi langkah saat ini
        fig, ax = plt.subplots()
        edge_colors = []
        edge_widths = []
        for u, v in G.edges():
            if (u, v) in visited_edges or (v, u) in visited_edges:
                edge_colors.append('green')
                edge_widths.append(3)
            else:
                edge_colors.append('gray')
                edge_widths.append(1.5)

        node_colors = []
        for n in G.nodes():
            if n == current_node:
                node_colors.append('orange')
            elif n in visited_nodes:
                node_colors.append('lightgreen')
            else:
                node_colors.append('skyblue')

        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors,
                width=edge_widths, node_size=500, font_size=11, ax=ax)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)

        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img = Image.open(buf)
        plt.close()

        step_data.append((img, "\n".join(step_log)))

    return distances, step_data

# Streamlit App
st.title("🚦 Visualisasi Algoritma Dijkstra Langkah per Langkah")

sample_graph = """{
    '0': {'1': 2, '2': 6},
    '1': {'0': 2, '3': 5},
    '2': {'0': 6, '3': 8},
    '3': {'1': 5, '2': 8, '4': 10, '5': 15},
    '4': {'3': 10, '6': 2},
    '5': {'3': 15, '6': 6},
    '6': {'4': 2, '5': 6}
}"""

graph_input = st.text_area("📋 Masukkan Graph Dictionary (format Python):", value=sample_graph, height=200)
start_node = st.text_input("🖱 Masukkan node awal:", value='0')

if st.button("🚀 Jalankan Dijkstra"):
    try:
        graph = ast.literal_eval(graph_input)
        if start_node not in graph:
            st.error("❌ Node awal tidak ditemukan di graph.")
        else:
            distances, steps = dijkstra_with_steps(graph, start_node)

            st.success(f"📊 Jarak Terpendek dari node {start_node}:")
            for node, dist in distances.items():
                st.write(f"{start_node} ➝ {node} = {dist}")

            st.markdown("---")
            st.subheader(f"📝 Detail Proses ({len(steps)} langkah):")

            for i, (img, log) in enumerate(steps, start=1):
                st.image(img, caption=f"🖼️ Langkah ke-{i}", use_column_width=True)
                st.markdown(f"Log Proses:")
                st.code(log)

    except Exception as e:
        st.error(f"⚠️ Terjadi kesalahan: {e}")
