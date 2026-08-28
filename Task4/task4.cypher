// 1. Index and make patent id unique
CREATE CONSTRAINT
FOR (p:Patent)
REQUIRE p.id IS UNIQUE;

// 2. Count rows, no need WITH HEADERS we do not write any headers -> output 5000
LOAD CSV FROM 'file:///patent_data_extracted.csv' AS row
RETURN count(row);

// 3. Create All Patent Nodes
LOAD CSV FROM 'file:///patent_data_extracted.csv' AS row
MERGE (:Patent {id: toInteger(row[0])}) // Find or create node from 1st col in row
MERGE (:Patent {id: toInteger(row[1])}); // 2nd col

// 4. Draw Relationships
LOAD CSV FROM 'file:///patent_data_extracted.csv' AS row
MATCH (fromPatent:Patent {id: toInteger(row[0])}) // Match the existing referencing patent node from row 1
MATCH (toPatent:Patent {id: toInteger(row[1])}) // row 2
MERGE (fromPatent)-[:REFS]->(toPatent);

// 5. Find all referenced patents
MATCH
  (referencingPatent:Patent {id: 3858243})-[:REFS]->(referencedPatent:Patent)
RETURN referencingPatent, referencedPatent;

// 6. Top 5 most referenced patents (Top 5 has > 2 citations)
MATCH (referencing:Patent)-[:REFS]->(referenced:Patent)
RETURN referenced.id AS Patent_Id, count(referencing) AS Reference_Cout
ORDER BY Reference_Cout DESC
LIMIT 5;

// 7. find links with 3 hops
MATCH p = (p1:Patent)-[:REFS*..3]-(p2:Patent)
WHERE
  p1.id < p2.id
  // p1 and p2 have no ref between
  AND
  NOT EXISTS {
  (p1)-[:REFS]-(p2)
  }
RETURN p, length(p) AS Hops
ORDER BY Hops DESC
LIMIT 10;

// 8. find shortest path between nodes
MATCH (p1:Patent {id: 2807431}), (p2:Patent {id: 3176316})
WHERE NOT EXISTS { (p1)-[:REFS]-(p2) }
MATCH path = SHORTESTPATH ((p1)-[:REFS*..6]-(p2))
RETURN path;

// Remove Constraint
SHOW CONSTRAINTS;
DROP CONSTRAINT constraint_cf53872b; // replace name