import rdflib
from pyvis.network import Network

# Load the OWL file
owl_file = './Reac4Cat.owl'
g = rdflib.Graph()
g.parse(owl_file)

# Initialize a pyvis Network for visualization
nt = Network(notebook=True)

# Extract class hierarchy
for s, p, o in g.triples((None, rdflib.RDFS.subClassOf, None)):
    if isinstance(s, rdflib.URIRef) and isinstance(o, rdflib.URIRef):
        nt.add_node(str(s), label=str(s))
        nt.add_node(str(o), label=str(o))
        nt.add_edge(str(s), str(o))

# Extract individuals
for s, p, o in g.triples((None, None, None)):
    if isinstance(s, rdflib.URIRef) and isinstance(o, rdflib.URIRef):
        nt.add_node(str(s), label=str(s))
        nt.add_node(str(o), label=str(o))
        nt.add_edge(str(s), str(o))

# Extract object properties
for s, p, o in g.triples((None, None, None)):
    if isinstance(s, rdflib.URIRef) and isinstance(p, rdflib.URIRef) and isinstance(o, rdflib.URIRef):
        nt.add_node(str(s), label=str(s))
        nt.add_node(str(o), label=str(o))
        nt.add_edge(str(s), str(o), label=str(p))

# Save the interactive visualization to an HTML file
nt.show_buttons(filter_=['physics'])
html_file_path = 'ontology_interactive.html'
nt.save_graph(html_file_path)
print(f"Interactive visualization saved to '{html_file_path}'")