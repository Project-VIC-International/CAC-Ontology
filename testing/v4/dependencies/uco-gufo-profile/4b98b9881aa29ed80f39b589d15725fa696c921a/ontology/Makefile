#!/usr/bin/make -f

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

SHELL := /bin/bash

top_srcdir := $(shell cd .. ; pwd)

uco_srcdir := $(top_srcdir)/dependencies/UCO

generated_dependencies_ttls := \
  $(top_srcdir)/dependencies/CDO-Shapes-gufo/dependencies/formatted-gufo.ttl \
  $(uco_srcdir)/tests/uco_monolithic.ttl

test_pys := $(wildcard test_*.py)

ttl_basenames := $(wildcard uco-*.ttl)

all: \
  catalog-v001.xml

# .empty.ttl is retained to guarantee rdfpipe takes at least one file as
# an input when building generated-dependencies.ttl and -local.ttl.
.empty.ttl:
	test -r $@

.pytest.done.log: \
  $(test_pys) \
  $(top_srcdir)/.venv.done.log \
  generated-local.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && pytest \
	    --log-level=DEBUG
	touch $@

catalog-v001.xml: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/etc/domain_directories.tsv \
  $(top_srcdir)/etc/dependency_files.tsv \
  $(uco_srcdir)/ontology/uco/master/catalog-v001.xml \
  $(uco_srcdir)/src/create-catalog-v001.xml.py \
  generated-ontology.ttl
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && python3 $(uco_srcdir)/src/create-catalog-v001.xml.py \
	    --catalog-xml $(uco_srcdir)/ontology/uco/master/catalog-v001.xml \
	    _$@ \
	    $(top_srcdir)/etc/domain_directories.tsv \
	    $(top_srcdir)/etc/dependency_files.tsv \
	    "$(top_srcdir)" \
	    generated-ontology.ttl
	mv _$@ $@

check: \
  .pytest.done.log \
  all

clean:
	@rm -rf \
	  __pycache__
	@rm -f \
	  .*.done.log \
	  _* \
	  catalog-v001.xml \
	  generated-*.ttl

generated-dependencies.ttl: \
  $(generated_dependencies_ttls) \
  $(top_srcdir)/.venv.done.log \
  $(uco_srcdir)/ontology/owl/owl.ttl \
  .empty.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(generated_dependencies_ttls) \
	    .empty.ttl \
	    > _$@
	# Check for conflicts when merging ontology files.
	source $(top_srcdir)/venv/bin/activate \
	  && pyshacl \
	    --shacl $(uco_srcdir)/ontology/owl/owl.ttl \
	    _$@
	mv _$@ $@

# OWL shapes not run against this file, as there may be axioms needed
# from generated-dependencies.ttl.
generated-local.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(ttl_basenames) \
  .empty.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(ttl_basenames) \
	    .empty.ttl \
	    > _$@
	mv _$@ $@

generated-ontology.ttl: \
  generated-dependencies.ttl \
  generated-local.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    generated-dependencies.ttl \
	    generated-local.ttl \
	    > _$@
	# Check for conflicts when merging ontology files.
	source $(top_srcdir)/venv/bin/activate \
	  && pyshacl \
	    --shacl $(uco_srcdir)/ontology/owl/owl.ttl \
	    _$@
	mv _$@ $@
