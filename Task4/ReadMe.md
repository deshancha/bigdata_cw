```
source .venv/bin/activate
cd Task4
python src/data_extractor.py  
```

Index and make patent id unique
```
CREATE CONSTRAINT FOR (p:Patent) REQUIRE p.id IS UNIQUE;
```

Count rows, no need WITH HEADERS we do not write any headers
```
LOAD CSV FROM 'file:///patent_data_extracted.csv' AS row
RETURN count(row);
```


Create All Patent Nodes
```
LOAD CSV FROM 'file:///patent_data_extracted.csv' AS row
// Find or create node from first column in row and assign to fromPatent
MERGE (:Patent {id: toInteger(row[0])})
// Find or create node from second column in row and assign to toPatent
MERGE (:Patent {id: toInteger(row[1])})
```

Draw the relationships 
```
LOAD CSV FROM 'file:///patent_data_extracted.csv' AS row
// Match the existing citing patent node
MATCH (fromPatent:Patent {id: toInteger(row[0])})
// Match the existing cited patent node
MATCH (toPatent:Patent {id: toInteger(row[1])})
// Draw the relationship link between them
MERGE (fromPatent)-[:REFS]->(toPatent);
```

Find all patents that a patent referenced
```
MATCH (referencingPatent:Patent {id: 3858243})-->(referencedPatent:Patent)
RETURN referencingPatent, referencedPatent;
```

Top 5 most referenced patents (Top 5 has > 3 citations)
```
MATCH (referencing:Patent)-[:REFS]->(referenced:Patent)
RETURN referenced.id AS Patent_Id, count(referencing) AS Reference_Cout
ORDER BY Reference_Cout DESC
LIMIT 5;
```

4 Hops 

Find possibilities of 3 Refs ( 4 Hops)
```
MATCH p = (p1:Patent)-[:REFS*..3]-(p2:Patent)
WHERE p1.id < p2.id AND p1.id <> p2.id
// Ensure p1 and p2 have NO direct reference between them
AND NOT EXISTS { (p1)-[:REFS]->(p2) }
AND NOT EXISTS { (p2)-[:REFS]->(p1) }
RETURN DISTINCT p1.id, p2.id, length(p) AS Hops
ORDER BY Hops DESC
LIMIT 10;
```

more than 4 it looks they have immediate refs

NMow draw shortest path

```
MATCH p = shortestPath((p1:Patent {id: 1600859})-[:REFS*..6]-(p2:Patent {id: 3858245}))
RETURN p;
```