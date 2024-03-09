# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 13:00:31 2024

@author: Alexander Behr
"""

from owlready2 import *
import types
import uuid

onto_path = "./ontologies/KG-DWSIM_EnzML_ELN_output_with_r4c.owl"
onto = get_ontology(onto_path).load()

### 
#reaction individual
reac_indv_name = "ABTS-Oxidation_r2"
#TODO: cat_names, educt_names, product_names could be retrieved automatically via individual reac_indv_name
#catalyst names
cat_names = ["Laccase"]
#educt names
educt_names = ["ABTS_red","Oxygen"]
#product names
product_names = ["ABTS_ox"]

#material and reaction iris
mat_class_iri = "SBO_0000240" #SBO material entity
reaction_class_iri = "SBO_0000200" #redox reaction http://biomodels.net/SBO/SBO_0000200
# uuid for unique identifier for the specified reaction (redox reaction with Laccase)
spec_reac_uuid =str(uuid.uuid4()).replace("-","_")
spec_reac_indv_uuid =str(uuid.uuid4()).replace("-","_")

# object properties 
reacComp_prop_str = "hasReactionComponent"
potCatBy_prop_str ="isPotentiallyCatalysedBy"
cat_prop_str = "hasCatalyst"
educt_prop_str = "has input"
product_prop_str = "has output"
reac_role_prop_str = "hasReactionRole"
###

with onto:
    ## First Axiom
    #(hasReactionComponent some ({Sub_Laccase})) and (isPotentiallyCatalysedBy some ({Sub_Laccase}) SubClassOf hasCatalyst some ({Sub_Laccase})
    for cat_name in cat_names:
        cat_sub_indv = onto.search_one(label = cat_name).instances()[0]
        reacComp_rel = onto.search_one(label = reacComp_prop_str)
        potCatBy_rel = onto.search_one(label = potCatBy_prop_str)
        cat_rel = onto.search_one(label = cat_prop_str) 
        
        gca1 = GeneralClassAxiom(reacComp_rel.some(OneOf([cat_sub_indv])) & potCatBy_rel.some(OneOf([cat_sub_indv]))) # Left side
        gca1.is_a.append(cat_rel.some(OneOf([cat_sub_indv]))) # Right side
        
        ## Second Axiom
        #'Laccase Reaction' and (hasCatalyst some ((material entity or chemical entity) and (inverse (hasReactionComponent some 'Laccase Reaction'))) SubClassOf 'Catalysed Laccase Reaction'
        material_class = onto.search_one(iri = "*"+mat_class_iri)
        reaction_class = onto.search_one(iri = "*"+reaction_class_iri)
        
        spec_reac_label = reaction_class.label.first() + " with " + cat_name# label of specific reaction
    
        spec_reaction_class = types.new_class(spec_reac_uuid, (reaction_class,))
        spec_reaction_class.label = spec_reac_label
        spec_reaction_indv = spec_reaction_class(spec_reac_indv_uuid)
        spec_reaction_indv.label = "indv_"+spec_reac_label
        
        #'Haber Bosch reaction' and (hasCatalyst some 'material entity' or 'chemical entity') and ( inverse (hasReactionComponent) some 'Haber Bosch reaction'))) SubClassOf 'catalysed Haber Bosch reaction'
        gca2 = GeneralClassAxiom(reaction_class & (cat_rel.some(material_class) & (reacComp_rel.inverse.some(reaction_class)))) # Left side
        gca2.is_a.append(spec_reaction_class) # Right side
        
        
        ## Third Axiom
        #(hasEductComponent some ABTS_red) and (hasEductComponent some Oxygen) and (hasProductComponent some ABTS_ox) SubClassOf hasReactionRole some ({Laccase_reaction_indv})
        educt_rel = onto.search_one(label = educt_prop_str)
        product_rel = onto.search_one(label = product_prop_str)
        reac_role_rel = onto.search_one(label = reac_role_prop_str)
        reac_indv = onto.search_one(label = reac_indv_name)
        
        gca_str = ""
        for educt_name in educt_names:
            #educt_class = onto.search_one(label = educt_name)
            if gca_str:
                gca_str += "& educt_rel.some(onto.{})".format(educt_name)
            else:
                gca_str += "educt_rel.some(onto.{})".format(educt_name)
                
        for product_name in product_names:
            #product_class = onto.search_one(label = product_name)
            if gca_str:
                gca_str += "& product_rel.some(onto.{})".format(product_name)
            else:
                gca_str += "product_rel.some(onto.{})".format(product_name)
        
        codestr = "gca3 = GeneralClassAxiom(" + gca_str + ")"
        code = compile(codestr, "<string>","exec")
        exec(code)
        
        gca3.is_a.append(reac_role_rel.some(OneOf([spec_reaction_indv]))) # Right side
        
        
        onto.save(file=onto_path.replace(".owl","_gca.owl"), format="rdfxml")      

#

