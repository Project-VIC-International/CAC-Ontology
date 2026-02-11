# Duplicate Detection Report

## Source Checked
- **URL**: https://www.justice.gov/usao-ndfl/pr/tallahassee-man-sentenced-twenty-years-federal-prison-child-exploitation-crime
- **Collection Time**: 2026-01-07T04:00:43Z

## Duplicate Check Results
- **Status**: NEW SOURCE (no prior collection found)
- **Method**: URL exact match against existing KG
- **Existing documents checked**: Searched `examples_knowledge_graphs/*.ttl` for matching URL

### URL Match Query
```sparql
PREFIX observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>

SELECT ?doc ?collectedAt WHERE {
  ?doc uco-core:hasFacet ?urlFacet .
  ?urlFacet a observable:URLFacet ;
            observable:url ?url .
  FILTER(STR(?url) = "https://www.justice.gov/usao-ndfl/pr/tallahassee-man-sentenced-twenty-years-federal-prison-child-exploitation-crime")
}
```
**Result**: 0 matches

## Entity Resolution (Near-Duplicate Check)
- **URL Similarity Check**: No similar URLs found in existing KG
- **Title Match Check**: No existing documents with matching title "Tallahassee Man Sentenced"
- **Content Similarity**: N/A (first collection of this source)

## Decision
- **Action**: PROCEED with collection
- **Reason**: No duplicate or near-duplicate detected

## Content Hashes (for future deduplication)
- **Normalized text SHA-256**: `72d619874021101fc6062a834d8eb070033f09722602142dc5ba5a5f96ef4581`
- **Normalized text size**: 3068 bytes
