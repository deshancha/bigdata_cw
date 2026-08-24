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
MATCH (patent:Patent {id: 3858243})-->(citedPatent:Patent)
RETURN patent.id AS Patent_Id, citedPatent.id AS Cited_Patent_Id;
```

