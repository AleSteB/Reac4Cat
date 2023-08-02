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

# Save and show the interactive visualization
nt.show_buttons(filter_=['physics'])
nt.show('ontology_interactive.html')