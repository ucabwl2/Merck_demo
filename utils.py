import json
import uuid
from IPython.display import IFrame

default_query = """
    MATCH (n)
    WITH n, rand() AS random
    ORDER BY random
    LIMIT 100
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN n AS source_node,
           id(n) AS source_id,
           r,
           m AS target_node,
           id(m) AS target_id
    """

def vis_network(nodes, edges, physics=False):
    html = """
    <html>
    <head>
      <link href="vis/dist/vis.css" rel="stylesheet" type="text/css">
    </head>
    <body>
    <div id="{id}"></div>
    <script type="text/javascript">
      var nodes = {nodes};
      var edges = {edges};
      var container = document.getElementById("{id}");
      var data = {{
        nodes: nodes,
        edges: edges
      }};
      var options = {{
          nodes: {{
              shape: 'dot',
              size: 25,
              font: {{
                  size: 14
              }}
          }},
          edges: {{
              font: {{
                  size: 14,
                  align: 'middle'
              }},
              color: 'gray',
              arrows: {{
                  to: {{enabled: true, scaleFactor: 0.5}}
              }},
              smooth: {{enabled: false}}
          }},
          physics: {{
              enabled: {physics}
          }}
      }};
      var network = new vis.Network(container, data, options);
    </script>
    </body>
    </html>
    """

    unique_id = str(uuid.uuid4())
    html = html.format(id=unique_id, nodes=json.dumps(nodes), edges=json.dumps(edges), physics=json.dumps(physics))

    with open("vis/dist/vis.js","r",encoding='utf-8') as fp:
        vis_js = fp.readline()

    
    html = "<script>" + vis_js  + "</script>" + html

    filename = "figure/graph-{}.html".format(unique_id)


    file = open(filename, "w")
    file.write(html)
    file.close()

    return IFrame(src=filename,width="100%",height=400)

def draw(data=None, physics=False):
    # The options argument should be a dictionary of node labels and property keys; it determines which property
    # is displayed for the node label. For example, in the movie graph, options = {"Movie": "title", "Person": "name"}.
    # Omitting a node label from the options dict will leave the node unlabeled in the visualization.
    # Setting physics = True makes the nodes bounce around when you touch them!
    """
    Args:
        data: py2neo result with source_node,  r, target_node
    """

    if data is None:
        raise ValueError('data must be provided')

    nodes = []
    edges = []

    def get_vis_info(node, *args):
        node_label = [x for x in list(node.labels) if x != 'Hetio'][0]
        vis_label = node['name']

        return {"id": vis_label, "label": vis_label, "group": node_label}

    for row in data:
        source_node = row.start_node
        rel = row
        target_node = row.end_node
        source_info = get_vis_info(source_node)

        if source_info not in nodes:
            nodes.append(source_info)

        if rel is not None:
            target_info = get_vis_info(target_node)

            if target_info not in nodes:
                nodes.append(target_info)

            edges.append({"from": source_info["id"], "to": target_info["id"], "label": type(rel).__name__})

    return vis_network(nodes, edges, physics=physics)
