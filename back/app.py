import overpy

api = overpy.Overpass()

from flask import render_template
from flask import Flask
from flask_cors import CORS

# enable CORS

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/")
def index():
    return render_template('index.html')
@app.route("/detail/<id>")
def detail(id):
    result = api.query("""[out:json][timeout:25];
(
  node(NODE_ID);
);
out body;
>;
out skel qt;
                     """.replace("NODE_ID",id))
    if len(result.nodes) != 0 : 
      return { "details":  result.nodes[0].tags }
    else:
        return {}

@app.route("/spots/<north>/<east>/<south>/<west>")
def spots(north,east,south,west):
    sports_query ="""
[out:json]
[timeout:60]
;
(
  node
    ["tourism"="museum"]
    (SOUTH,WEST,NORTH,EAST);
  node
    ["leisure"="park"]
    (SOUTH,WEST,NORTH,EAST);
  node
    ["leisure"="garden"]
    (SOUTH,WEST,NORTH,EAST);
  node
    ["amenity"="public_building"]
    (SOUTH,WEST,NORTH,EAST);
  node
    ["historic"]
    (SOUTH,WEST,NORTH,EAST);
  node
    ["man_made"="tower"]
    (SOUTH,WEST,NORTH,EAST);
  node
    ["man_made"="monument"]
    (SOUTH,WEST,NORTH,EAST);
  node
    ["amenity"="place_of_worship"]
    (SOUTH,WEST,NORTH,EAST);
  node
    ["amenity"="concert_hall"]
    (SOUTH,WEST,NORTH,EAST);
  node
    ["tourism"="viewpoint"]
    (SOUTH,WEST,NORTH,EAST);
  node
    ["historic"="castle"]
    (SOUTH,WEST,NORTH,EAST);
  node
    ["historic"="ruins"]
    (SOUTH,WEST,NORTH,EAST);
);
out ids geom;
    """.replace("SOUTH",south).replace("WEST",west).replace("NORTH",north).replace("EAST",east)
    result = api.query(sports_query)
    data = {
            "spots": [
                {
                    "id": element.id,
                    "lat": element.lat,
                    "lon": element.lon,
                }
                for element in result.nodes
            ]
        }
    return data