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

from rdflib import OWL, Graph, URIRef

NS_OWL = OWL

srcdir = Path(__file__).parent


def test_disjointedness_symmetry() -> None:
    """
    This test confirms that owl:disjointWith statements are entered specified in both directions.  (While the effect of a disjointedness assertion does not require this symmetric entry, the extra explicitness is meant to assist with modeling comprehension.)
    """
    # The expected-set is all owl:disjointWith statements backwards and forwards.
    # This test will derive the expected set from the computed set.
    expected: set[tuple[URIRef, URIRef]] = set()
    computed: set[tuple[URIRef, URIRef]] = set()

    profile_graph = Graph()
    profile_graph.parse(srcdir / "generated-local.ttl")
    logging.debug("len(profile_graph) = %d.", len(profile_graph))

    for triple in profile_graph.triples((None, NS_OWL.disjointWith, None)):
        assert isinstance(triple[0], URIRef)
        assert isinstance(triple[2], URIRef)
        computed.add((triple[0], triple[2]))

    for pair in computed:
        expected.add(pair)
        expected.add((pair[1], pair[0]))

    try:
        assert expected == computed
    except AssertionError:
        lines_to_copy_paste = "\n".join(
            (
                "<%s> <%s> <%s> ." % (x[0], NS_OWL.disjointWith, x[1])
                for x in (expected - computed)
            )
        )
        logging.info(
            "This can be addressed by copying the following lines into the profile Turtle file.  Automated format-checking should handle syntactically normalizing them.\n%s"
            % lines_to_copy_paste
        )
        raise
