# Pinned UCO gUFO Profile dependency

The directory `4b98b9881aa29ed80f39b589d15725fa696c921a` is the exact content of the user-provided GitHub source archive:

- archive: `UCO-Profile-gufo-4b98b9881aa29ed80f39b589d15725fa696c921a.zip`
- archive SHA-256: `e8298fa86e24432947901c8b574378bee4b3d3d8cf946a25f37d912908d0c8d6`
- upstream commit: `4b98b9881aa29ed80f39b589d15725fa696c921a`
- upstream repository: `https://github.com/ucoProject/UCO-Profile-gufo`
- license: Apache-2.0, with additional notices in `THIRD_PARTY_LICENSES.md`

The original source snapshot is retained intact for auditability. GitHub source archives do not include the working-tree contents of Git submodules, so Gate 4 reconstructs the runtime closure at the exact gitlink revisions recorded by the parent commit:

- `dependencies/UCO`: `7ebb3957e9e9a2e1bb9c66cd1ede8c912a726344`
- `dependencies/CDO-Shapes-gufo`: `1b13dd56308261f451db3e304ce7a5e044ed0297`
- UCO `dependencies/collections-ontology`: `619e7b02646321174635fd04be658e338bf7d1d7`
- UCO `dependencies/error`: `101aca952ef854505f49725d852de00e6e192344`

The CDO snapshot contains the generated gUFO ontology and gUFO SHACL shapes referenced by the profile catalogs. Build-only nested submodules that are not referenced by the runtime catalogs are not represented as part of the executed closure.
