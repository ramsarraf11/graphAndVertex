#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import networkx as nx
import matplotlib.pyplot as plt


class GraphGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graph GUI")

        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        self.graph = nx.DiGraph()
        self.positions = {}
        self.vertices = set()
        self.edges = set()
        self.history = []

        self.canvas.bind("<Button-1>", self.add_vertex)
        self.canvas.bind("<Button-3>", self.add_edge)
        self.root.bind("<Control-z>", self.undo)

        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.TOP)

        self.add_vertex_button = tk.Button(self.frame, text="Add Vertex", command=self.add_vertex_dialog)
        self.add_vertex_button.pack(side=tk.LEFT)

        self.add_weight_button = tk.Button(self.frame, text="Add Weight", command=self.add_weight_dialog)
        self.add_weight_button.pack(side=tk.LEFT)

        self.shortest_path_button = tk.Button(self.frame, text="Find Shortest Path", command=self.find_shortest_path)
        self.shortest_path_button.pack(side=tk.LEFT)

        self.undo_button = tk.Button(self.frame, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.frame, text="Clear", command=self.clear_graph)
        self.clear_button.pack(side=tk.LEFT)

    def add_vertex_dialog(self):
        name = simpledialog.askstring("Add Vertex", "Enter vertex name:")
        if name:
            self.add_vertex_by_name(name)

    def add_vertex_by_name(self, name):
        x, y = self.get_random_position()
        self.graph.add_node(name)
        self.positions[name] = (x, y)
        self.vertices.add(name)
        self.draw_graph()

    def add_vertex(self, event):
        name = simpledialog.askstring("Add Vertex", "Enter vertex name:")
        if name:
            x, y = event.x, event.y
            self.graph.add_node(name)
            self.positions[name] = (x, y)
            self.vertices.add(name)
            self.draw_graph()

    def add_edge(self, event):
        if not self.vertices:
            messagebox.showerror("Error", "Add at least one vertex first.")
            return

        source_vertex = simpledialog.askstring("Add Edge", "Enter source vertex name:")
        if source_vertex not in self.vertices:
            messagebox.showerror("Error", "Invalid source vertex.")
            return

        target_vertex = simpledialog.askstring("Add Edge", "Enter target vertex name:")
        if target_vertex not in self.vertices:
            messagebox.showerror("Error", "Invalid target vertex.")
            return

        weight = simpledialog.askinteger("Add Edge", "Enter weight:")
        if weight is None:
            return

        edge = (source_vertex, target_vertex, weight)
        self.graph.add_edge(source_vertex, target_vertex, weight=weight)
        self.edges.add(edge)
        self.history.append(("add_edge", edge))
        self.draw_graph()

    def add_weight_dialog(self):
        if not self.edges:
            messagebox.showerror("Error", "Add at least one edge first.")
            return

        source_vertex = simpledialog.askstring("Add Weight", "Enter source vertex name:")
        if source_vertex not in self.vertices:
            messagebox.showerror("Error", "Invalid source vertex.")
            return

        target_vertex = simpledialog.askstring("Add Weight", "Enter target vertex name:")
        if target_vertex not in self.vertices:
            messagebox.showerror("Error", "Invalid target vertex.")
            return

        weight = simpledialog.askinteger("Add Weight", "Enter weight:")
        if weight is None:
            return

        edge = (source_vertex, target_vertex, weight)
        if edge in self.edges:
            self.graph[source_vertex][target_vertex]["weight"] = weight
            self.history.append(("update_weight", edge))
            self.draw_graph()

    def find_shortest_path(self):
        if not self.vertices:
            messagebox.showerror("Error", "Add at least one vertex first.")
            return

        source_vertex = simpledialog.askstring("Find Shortest Path", "Enter source vertex name:")
        if source_vertex not in self.vertices:
            messagebox.showerror("Error", "Invalid source vertex.")
            return

        target_vertex = simpledialog.askstring("Find Shortest Path", "Enter target vertex name:")
        if target_vertex not in self.vertices:
            messagebox.showerror("Error", "Invalid target vertex.")
            return

        try:
            path = nx.dijkstra_path(self.graph, source_vertex, target_vertex)
            weight = nx.dijkstra_path_length(self.graph, source_vertex, target_vertex)
            messagebox.showinfo("Shortest Path", f"Path: {' -> '.join(path)}\nWeight: {weight}")
        except nx.NetworkXNoPath:
            messagebox.showinfo("Shortest Path", "No path found.")

    def undo(self, event=None):
        if self.history:
            action, item = self.history.pop()
            if action == "add_edge":
                self.graph.remove_edge(*item[:2])
                self.edges.remove(item)
            elif action == "update_weight":
                self.graph[item[0]][item[1]]["weight"] = item[2]
            self.draw_graph()

    def clear_graph(self):
        self.graph.clear()
        self.positions.clear()
        self.vertices.clear()
        self.edges.clear()
        self.history.clear()
        self.canvas.delete("all")

    def get_random_position(self):
        x = 100 + len(self.positions) * 50
        y = 300
        return x, y

    def draw_graph(self):
        self.canvas.delete("all")
        pos = self.positions.copy()
        for edge in self.edges:
            source, target, weight = edge
            self.canvas.create_line(pos[source], pos[target])
            self.canvas.create_text((pos[source][0] + pos[target][0]) // 2,
                                    (pos[source][1] + pos[target][1]) // 2,
                                    text=str(weight))
        for vertex, (x, y) in pos.items():
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="white")
            self.canvas.create_text(x, y, text=str(vertex))
        plt.figure(figsize=(8, 6))
        nx.draw(self.graph, with_labels=True, font_weight='bold')
        plt.show()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = GraphGUI()
    gui.run()

