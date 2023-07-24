NEO4J_URI = 'neo4j://localhost:7687'
NEO4J_USERNAME = 'neo4j'
NEO4J_PASSWORD = 'Z1414wjw!'

NEO4J_AURA_URI = 'neo4j+s://566e3d71.databases.neo4j.io'



link_prediction_queyr_1 = """
MATCH p0 = (:Compound {identifier: "DB00631"})-[:INCLUDES]-(:PharmacologicClass {identifier: "N0000000233"})-[:INCLUDES]-(:Compound {identifier: "DB00993"})-[:TREATS]-(:Disease {identifier: "DOID:2377"})
MATCH p1 = (:Compound {identifier: "DB00631"})-[:RESEMBLES]-(:Compound {identifier: "DB00242"})-[:TREATS]-(:Disease {identifier: "DOID:2377"})
MATCH p2 = (:Compound {identifier: "DB00631"})-[:BINDS]-(:Gene {name: "RRM1"})-[:ASSOCIATES]-(:Disease {identifier: "DOID:2377"})
MATCH p3 = (:Compound {identifier: "DB00631"})-[:BINDS]-(:Gene {name: "RRM2"})-[:BINDS]-(:Compound {identifier: "DB00242"})-[:TREATS]-(:Disease {identifier: "DOID:2377"})
MATCH p4 = (:Compound {identifier: "DB00631"})-[:BINDS]-(:Gene {name: "RRM1"})-[:BINDS]-(:Compound {identifier: "DB00242"})-[:TREATS]-(:Disease {identifier: "DOID:2377"})


RETURN [p0, p1, p2, p3, p4]

"""