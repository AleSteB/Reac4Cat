# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 10:48:42 2024

@author: Alexander Behr
"""

import os
from owlready2 import *



def indv_extraction(URL,IRI_file):
    onto = get_ontology(URL).load()
    
    indv_list = list(onto.individuals())
    iri_list = [i.iri for i in indv_list]
    with open(IRI_file, 'w') as f:
        for entry in iri_list:    
            f.write(str(entry)+"\n")
            
        
# URL: link to ontologie
# IRI-file: txt-file with the IRI's
# onto: name of the output-file
working_dir = os.getcwd()

#URL = "https://raw.githubusercontent.com/nfdi4cat/Ontology-Overview-of-NFDI4Cat/main/ontologies/AFO.ttl"


def ontology_simplification(URL,IRI_file,onto_path):
    
    # meth: methods can be found here [http://robot.obolibrary.org/extract]
    meth = "BOT"
    
    bashCommand = "java -jar {}/robot/robot.jar extract --input {} --method {} --term-file {} --output {} ".format(working_dir,URL, meth, IRI_file, onto_path)
    
    os.system(bashCommand)
    
    object_props = ["ends after", "has participant", "participates in", "temporally related to", "has role", "has characteristic", "composed primarily of","has modifier"]
    class_props = ["occurrent", "continuant","specifically dependent continuant"]#,""]
    
    onto = get_ontology("./"+ onto_path).load()
    
    for prop_name in object_props:
        prop = onto.search_one(label = prop_name)
        prop.domain = None
        prop.range = None
    
    
    for class_name in class_props:
        prop = onto.search_one(label = class_name)
        if prop:
            for rel in prop.is_a:
                try:
                    if rel.property.iri == "http://purl.obolibrary.org/obo/BFO_0000050":
                        prop.is_a.remove(rel)
                except:
                    pass
    
    onto.save(file="./"+onto_path, format="rdfxml")
    
    
   
URL = working_dir + "/ontologies/KG-DWSIM_EnzML_ELN_output_with_r4c_gca.owl" 
IRI_file = "iri_individuals.txt"
onto_path = "ontologies/KG-DWSIM_EnzML_ELN_output_with_r4c_gca_robotted.owl"


indv_extraction(URL,IRI_file)
ontology_simplification(URL,IRI_file,onto_path)
