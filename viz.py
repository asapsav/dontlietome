import json
import networkx as nx
import matplotlib.pyplot as plt

# Your JSON data
data = {
  "claim": "The moon does not exist",
  "olog": {
    "nodes": [
      {
        "id": "1",
        "text": "The moon exists",
        "type": "fact",
        "source": "Astronomical observations and scientific consensus"
      },
      {
        "id": "2",
        "text": "Conspiracy theories",
        "type": "motivation",
        "details": "Some individuals may promote the idea that the moon does not exist as part of a larger conspiracy theory."
      },
      {
        "id": "3",
        "text": "Misinterpretation of evidence",
        "type": "error",
        "details": "Some may misinterpret or disregard scientific evidence due to lack of knowledge or confirmation bias."
      },
      {
        "id": "4",
        "text": "Moon landing hoaxes",
        "type": "related-claim",
        "details": "Related to false claims that the moon landings were faked and therefore promote the idea that the moon might not be real."
      },
      {
        "id": "5",
        "text": "Satellite imagery",
        "type": "evidence",
        "details": "Photos and data from satellites and space missions provide evidence of the moon's existence."
      }
    ],
    "edges": [
      {
        "source": "2",
        "target": "1",
        "relation": "contradicts"
      },
      {
        "source": "3",
        "target": "1",
        "relation": "misunderstands"
      },
      {
        "source": "4",
        "target": "1",
        "relation": "misrepresents"
      },
      {
        "source": "5",
        "target": "1",
        "relation": "supports"
      }
    ]
  }
}

# Create a directed graph
G = nx.DiGraph()

# Add nodes with attributes
for node in data["olog"]["nodes"]:
    G.add_node(node["id"], label=node["text"])

# Add edges
for edge in data["olog"]["edges"]:
    G.add_edge(edge["source"], edge["target"], label=edge["relation"])

# Draw the graph
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'))
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Show the gra
plt.savefig("olog_graph.png", format="PNG")

# Show the graph
plt.show()
