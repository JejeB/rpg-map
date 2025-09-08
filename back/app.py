import overpy

api = overpy.Overpass()

from flask import render_template
from flask import Flask,request, jsonify, make_response
from flask_cors import CORS
import uuid

# enable CORS

detail_query="""
[out:json][timeout:25];
(
  node(NODE_ID);
);
out body;
>;
out skel qt;
"""

spots_query ="""
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
    """

mini_db = {}

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}},supports_credentials=True)

def user_discover_spot(id,user_id):
    if user_id in mini_db:
      mini_db[user_id].append(id)
    else:
       mini_db[user_id] = [id]

@app.route("/detail/<id>")  
def detail(id):
    user_id = request.cookies.get('user_id')
    if user_id:
        user_discover_spot(id,user_id)
    print(mini_db)
    result = api.query(detail_query.replace("NODE_ID",id))
    if len(result.nodes) != 0 : 
      return { "details":  result.nodes[0].tags }
    else:
        return {}

def is_spot_discovered(id,user_id):
    if user_id in mini_db:
        if id in mini_db[user_id]:
            print("        {}".format(id))
            return True
    return False

@app.route("/spots/<north>/<east>/<south>/<west>")
def spots(north,east,south,west):
    user_id = request.cookies.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        mini_db[user_id] = []
    print(mini_db)
    result = api.query(spots_query.replace("SOUTH",south).replace("WEST",west).replace("NORTH",north).replace("EAST",east))
    data = {
            "spots": [
                {
                    "id": element.id,
                    "lat": element.lat,
                    "lon": element.lon,
                    "discovered": is_spot_discovered(str(element.id),str(user_id))
                }
                for element in result.nodes
            ]
        }
    resp = make_response(jsonify(data))
    resp.set_cookie('user_id', user_id, max_age=60*60*24*30)
    return resp