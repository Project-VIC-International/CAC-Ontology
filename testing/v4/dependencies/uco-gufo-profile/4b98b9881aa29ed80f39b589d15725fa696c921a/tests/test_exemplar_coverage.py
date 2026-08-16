#!/usr/bin/env python3

# Portions of this file contributed by NIST are governed by the
# following statement:
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to Title 17 Section 105 of the
# United States Code, this software is not subject to copyright
# protection within the United States. NIST assumes no responsibility
# whatsoever for its use by other parties, and makes no guarantees,
# expressed or implied, about its quality, reliability, or any other
# characteristic.
#
# We would appreciate acknowledgement if the software is used.

import logging
from pathlib import Path
from typing import Optional, Set

from rdflib import OWL, RDF, RDFS, Graph, URIRef
from rdflib.query import ResultRow

NS_OWL = OWL
NS_RDF = RDF
NS_RDFS = RDFS

srcdir = Path(__file__).parent
top_srcdir = srcdir.parent


def test_exemplar_profile_coverage() -> None:
    """
    This test confirms that for each class C in the profile ontology (or
    ontologies) designated a class, or a subclass of some C'; and each
    property P designated a property, or a subproperty of some P';
    C (/P) is used in the exemplars graph.

    The transitive import closure of the ontology graph is brought in
    for subclass and subproperty entailment.  But, only concepts locally
    defined and/or mapped in this repository are checked for review-
    subjects. (Else, each dependent ontology graphs would also incur
    review-subject needs.)

    For gUFO, instances of a gufo:Type are also included in the review.
    """
    exemplar_graph = Graph()
    profile_graph = Graph()
    tbox_graph = Graph()
    combined_graph = Graph()

    exemplar_filepath = srcdir / "exemplars.ttl"
    ontology_filepath = top_srcdir / "ontology" / "generated-ontology.ttl"
    profile_filepath = top_srcdir / "ontology" / "generated-local.ttl"

    logging.debug("Loading exemplars graph %r.", exemplar_filepath)
    exemplar_graph.parse(exemplar_filepath)
    logging.debug("len(exemplar_graph) = %d.", len(exemplar_graph))

    logging.debug("Loading TBox graph %r.", ontology_filepath)
    tbox_graph.parse(ontology_filepath)
    logging.debug("len(tbox_graph) = %d.", len(tbox_graph))

    logging.debug("Loading profile graph %r.", profile_filepath)
    profile_graph.parse(profile_filepath)
    logging.debug("len(profile_graph) = %d.", len(profile_graph))

    combined_graph = exemplar_graph + tbox_graph

    classes_mapped: Set[URIRef] = set()
    classes_with_exemplars: Set[URIRef] = set()

    for triple in profile_graph.triples((None, NS_RDF.type, NS_OWL.Class)):
        assert isinstance(triple[0], URIRef)
        classes_mapped.add(triple[0])

    for triple in profile_graph.triples((None, NS_RDFS.subClassOf, None)):
        assert isinstance(triple[0], URIRef)
        classes_mapped.add(triple[0])

    gufo_type_query = """\
PREFIX gufo: <http://purl.org/nemo/gufo#>
SELECT ?nClass
WHERE {
  # owl:Class restriction is to not pick up Relators.
  ?nClass
    a owl:Class ;
    a/rdfs:subClassOf* gufo:Type ;
    .
}
"""
    for gufo_type_query_result in tbox_graph.query(gufo_type_query):
        assert isinstance(gufo_type_query_result, ResultRow)
        assert isinstance(gufo_type_query_result[0], URIRef)
        classes_mapped.add(gufo_type_query_result[0])

    result: Optional[bool]

    class_query = """\
ASK {
  ?nIndividual a/rdfs:subClassOf* ?nClass .
}
"""
    for class_mapped in sorted(classes_mapped):
        result = None
        for class_result in combined_graph.query(
            class_query, initBindings={"nClass": class_mapped}
        ):
            assert isinstance(class_result, bool)
            result = class_result
        if result is True:
            classes_with_exemplars.add(class_mapped)
        else:
            logging.debug("class_mapped = %r.", class_mapped)
            logging.debug("result = %r.", result)

    try:
        assert classes_mapped <= classes_with_exemplars
    except AssertionError:
        logging.info("These mapped classes have no exemplar instances:")
        undemonstrated_classes = classes_mapped - classes_with_exemplars
        for undemonstrated_class in sorted(undemonstrated_classes):
            logging.info("* %s", str(undemonstrated_class))
        raise

    properties_mapped: Set[URIRef] = set()
    properties_with_exemplars: Set[URIRef] = set()

    for n_property_class in {
        NS_OWL.AnnotationProperty,
        NS_OWL.DatatypeProperty,
        NS_OWL.ObjectProperty,
    }:
        for triple in profile_graph.triples((None, NS_RDF.type, n_property_class)):
            assert isinstance(triple[0], URIRef)
            properties_mapped.add(triple[0])
    for triple in profile_graph.triples((None, NS_RDFS.subPropertyOf, None)):
        assert isinstance(triple[0], URIRef)
        properties_mapped.add(triple[0])

    property_query = """\
ASK {
  ?nIndividual1 ?nUsedProperty ?nIndividual2 .
  ?nUsedProperty rdfs:subPropertyOf* ?nProperty .
}
"""
    for property_mapped in sorted(properties_mapped):
        result = None
        for property_result in combined_graph.query(
            property_query, initBindings={"nProperty": property_mapped}
        ):
            assert isinstance(property_result, bool)
            result = property_result
        if result is True:
            properties_with_exemplars.add(property_mapped)

    try:
        assert properties_mapped <= properties_with_exemplars
    except AssertionError:
        logging.info("These mapped properties have no exemplar instances:")
        undemonstrated_properties = properties_mapped - properties_with_exemplars
        for undemonstrated_property in sorted(undemonstrated_properties):
            logging.info("* %s", str(undemonstrated_property))
        raise
