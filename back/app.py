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
// Public Space
  node["amenity"="townhall"](SOUTH,WEST,NORTH,EAST);
  way["amenity"="townhall"](SOUTH,WEST,NORTH,EAST);
  relation["amenity"="townhall"](SOUTH,WEST,NORTH,EAST);

  node["amenity"="courthouse"](SOUTH,WEST,NORTH,EAST);
  way["amenity"="courthouse"](SOUTH,WEST,NORTH,EAST);
  relation["amenity"="courthouse"](SOUTH,WEST,NORTH,EAST);

  node["amenity"="marketplace"](SOUTH,WEST,NORTH,EAST);
  way["amenity"="marketplace"](SOUTH,WEST,NORTH,EAST);
  relation["amenity"="marketplace"](SOUTH,WEST,NORTH,EAST);
  
  node["amenity"="library"](SOUTH,WEST,NORTH,EAST);
  way["amenity"="library"](SOUTH,WEST,NORTH,EAST);
  relation["amenity"="library"](SOUTH,WEST,NORTH,EAST);
  
  node["leisure"="park"](SOUTH,WEST,NORTH,EAST);
  way["leisure"="park"](SOUTH,WEST,NORTH,EAST);
  relation["leisure"="park"](SOUTH,WEST,NORTH,EAST);

// Tourism

  node["tourism"="museum"](SOUTH,WEST,NORTH,EAST);
  way["tourism"="museum"](SOUTH,WEST,NORTH,EAST);
  relation["tourism"="museum"](SOUTH,WEST,NORTH,EAST);

  
  node["tourism"="wilderness_hut"](SOUTH,WEST,NORTH,EAST);
  way["tourism"="wilderness_hut"](SOUTH,WEST,NORTH,EAST);
  relation["tourism"="wilderness_hut"](SOUTH,WEST,NORTH,EAST);
  
  node["tourism"="alpine_hut"](SOUTH,WEST,NORTH,EAST);
  way["tourism"="alpine_hut"](SOUTH,WEST,NORTH,EAST);
  relation["tourism"="alpine_hut"](SOUTH,WEST,NORTH,EAST);

  node["amenity"="place_of_worship"](SOUTH,WEST,NORTH,EAST);
  way["amenity"="place_of_worship"](SOUTH,WEST,NORTH,EAST);
  relation["amenity"="place_of_worship"](SOUTH,WEST,NORTH,EAST);

  node["historic"="castle"](SOUTH,WEST,NORTH,EAST);
  way["historic"="castle"](SOUTH,WEST,NORTH,EAST);
  relation["historic"="castle"](SOUTH,WEST,NORTH,EAST);

  node["historic"="ruins"](SOUTH,WEST,NORTH,EAST);
  way["historic"="ruins"](SOUTH,WEST,NORTH,EAST);
  relation["historic"="ruins"](SOUTH,WEST,NORTH,EAST);

  node["tourism"="viewpoint"](SOUTH,WEST,NORTH,EAST);
  way["tourism"="viewpoint"](SOUTH,WEST,NORTH,EAST);
  relation["tourism"="viewpoint"](SOUTH,WEST,NORTH,EAST);

  node["historic"="archaeological_site"](SOUTH,WEST,NORTH,EAST);
  way["historic"="archaeological_site"](SOUTH,WEST,NORTH,EAST);
  relation["historic"="archaeological_site"](SOUTH,WEST,NORTH,EAST);

// Natural
  node["natural"="peak"](SOUTH,WEST,NORTH,EAST);
  way["natural"="peak"](SOUTH,WEST,NORTH,EAST);
  relation["natural"="peak"](SOUTH,WEST,NORTH,EAST);

node["natural"="saddle"](SOUTH,WEST,NORTH,EAST);
  way["natural"="saddle"](SOUTH,WEST,NORTH,EAST);
  relation["natural"="saddle"](SOUTH,WEST,NORTH,EAST);

  node["natural"="waterfall"](SOUTH,WEST,NORTH,EAST);
  way["natural"="waterfall"](SOUTH,WEST,NORTH,EAST);
  relation["natural"="waterfall"](SOUTH,WEST,NORTH,EAST);

  node["natural"="cave_entrance"](SOUTH,WEST,NORTH,EAST);
  way["natural"="cave_entrance"](SOUTH,WEST,NORTH,EAST);
  relation["natural"="cave_entrance"](SOUTH,WEST,NORTH,EAST);

  node["natural"="volcano"](SOUTH,WEST,NORTH,EAST);
  way["natural"="volcano"](SOUTH,WEST,NORTH,EAST);
  relation["natural"="volcano"](SOUTH,WEST,NORTH,EAST);

  node["natural"="beach"](SOUTH,WEST,NORTH,EAST);
  way["natural"="beach"](SOUTH,WEST,NORTH,EAST);
  relation["natural"="beach"](SOUTH,WEST,NORTH,EAST);

  node["natural"="glacier"](SOUTH,WEST,NORTH,EAST);
  way["natural"="glacier"](SOUTH,WEST,NORTH,EAST);
  relation["natural"="glacier"](SOUTH,WEST,NORTH,EAST);
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