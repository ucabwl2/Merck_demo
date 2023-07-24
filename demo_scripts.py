
from config import *
from py2neo import Graph,Node,Relationship
import pandas as pd
from utils import draw

graph = Graph(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def discovery_drugs_for_disease(name, limit):
    query = f'match (f:Compound)-[r:TREATS]-(d:Disease) ' \
    f'where d.name=~".*{name}.*" return f.name as drugs, f.identifier as drug_id, ' \
    f'd.name as target_disease limit {limit};'
    print(f"疾病 {name} 的治疗药物搜索结果（仅展示 {limit} 条）：")
    return  graph.run(query).to_data_frame()

def discovery_gene_for_treatment(disease_name, drug_name, output="table",gene_amount=1,limit=10,*args):
    if gene_amount == 1:

        query = 'match (s:Compound {name:$drug_name} )-[p]-(o:Gene)-' \
        '[p2]-(t:Disease {name:$disease_name}) return s,p,o, p2,t limit $limit;'
        print(f"药物成分 {drug_name} 与疾病 {disease_name} 共同关联的基因有： \n")
        print(f"(关系路径： 药物 -> 基因 <- 疾病)\n")

    elif gene_amount == 2:
        query = 'match (c:Compound {name:$drug_name} )-[r1]-(g1:Gene)-[r2]-(g2:Gene)-' \
        '[r3]-(d:Disease {name:$disease_name}) return c,r1,g1,r2,g2,r3,d limit $limit;'
        print(f"药物成分 {drug_name} 与疾病 {disease_name} 共同关联的基因有： \n")
        print(f"(关系路径： 药物 -> 基因 - 基因 <- 疾病)\n")
    result = graph.run(query, drug_name=drug_name, disease_name=disease_name, limit=limit)

    if output=="table":
        records = []
        if gene_amount == 1:
            col = ["Drug","rel_1","gene","rel_2","Disease"]
            for r in result:
                records.append([r['s']['name'],
                                type(r['p']).__name__,
                                r['o']['name'],
                                type(r['p2']).__name__,
                                r['t']['name']
                ])
        elif gene_amount == 2:
            col = ["Drug","rel_1","gene","rel_2","gene","rel_3","Disease"]
            for r in result:
                records.append([r['c']['name'],
                                type(r['r1']).__name__,
                                r['g1']['name'],
                                type(r['r2']).__name__,
                                r['g2']['name'],
                                type(r['r3']).__name__,
                                r['d']['name'],
                ])
            
        else:
            raise NotImplementedError('invalid value for amount')
        return pd.DataFrame(records,columns=col)
    else:
        return draw(result.to_subgraph())


def discovery_similarity_of_drugs(drug_1="Amoxicillin",drug_2="Norethindrone", limit=15, output='table'):
    query = """
    match (c1:Compound {name: $drug_1})-[r1]-(g1:Gene)-[r2]-(g2:Gene)-[r3]-(c2:Compound {name: $drug_2}) 
    return c1,r1,g1,r2,g2,r3,c2 limit $limit
    """
    print(f"(关系路径： 药物 - 基因 - 基因 - 药物)\n")
    print(f"药物成分 {drug_1} 与药物成分 {drug_2} 共同关联的基因路径有： \n")

    result = graph.run(query, drug_1=drug_1, drug_2=drug_2, limit=limit)
    if output == 'table':
        records = []
        col = ['drug_1','rel_1','gene_1','rel_2','gene_2','rel_3','drug_2']
        for r in result:
            records.append([r['c1']['name'],
                            type(r['r1']).__name__,
                            r['g1']['name'],
                            type(r['r2']).__name__,
                            r['g2']['name'],
                            type(r['r3']).__name__,
                            r['c2']['name'],
            ])
        
        return pd.DataFrame(records,columns=col)
    elif output == 'graph':
        return draw(result.to_subgraph())
    else:
        raise NotImplementedError(f"output format {output} not valid")


def link_prediction_demo(*args):
    link_prediction_query_1 = """
MATCH p0 = (:Compound {identifier: "DB00631"})-[:INCLUDES]-(:PharmacologicClass {identifier: "N0000000233"})-[:INCLUDES]-(:Compound {identifier: "DB00993"})-[:TREATS]-(:Disease {identifier: "DOID:2377"})
MATCH p1 = (:Compound {identifier: "DB00631"})-[:RESEMBLES]-(:Compound {identifier: "DB00242"})-[:TREATS]-(:Disease {identifier: "DOID:2377"})
MATCH p2 = (:Compound {identifier: "DB00631"})-[:BINDS]-(:Gene {name: "RRM1"})-[:ASSOCIATES]-(:Disease {identifier: "DOID:2377"})
MATCH p3 = (:Compound {identifier: "DB00631"})-[:BINDS]-(:Gene {name: "RRM2"})-[:BINDS]-(:Compound {identifier: "DB00242"})-[:TREATS]-(:Disease {identifier: "DOID:2377"})
MATCH p4 = (:Compound {identifier: "DB00631"})-[:BINDS]-(:Gene {name: "RRM1"})-[:BINDS]-(:Compound {identifier: "DB00242"})-[:TREATS]-(:Disease {identifier: "DOID:2377"})
MATCH p5 = (:Compound {identifier: "DB00631"})-[:BINDS]-(:Gene {name: "DCK"})-[:BINDS]-(:Compound {identifier: "DB00242"})-[:TREATS]-(:Disease {identifier: "DOID:2377"})
MATCH p6 = (:Compound {identifier: "DB00631"})-[:BINDS]-(:Gene {name: "POLA1"})-[:BINDS]-(:Compound {identifier: "DB00242"})-[:TREATS]-(:Disease {identifier: "DOID:2377"})
MATCH p7 = (:Compound {identifier: "DB00631"})-[:RESEMBLES]-(:Compound {identifier: "DB06213"})-[:RESEMBLES]-(:Compound {identifier: "DB00242"})-[:TREATS]-(:Disease {identifier: "DOID:2377"})
RETURN p0, p1, p2, p3, p4, p5, p6, p7
"""
    result = graph.run(link_prediction_query_1)
    g = result.to_subgraph()
    return draw(data=g)