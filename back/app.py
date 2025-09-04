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

@app.route("/spots")
def spots():
    result = api.query("""
[out:json]
[timeout:30]
;
(
  node
    ["tourism"="museum"]
    48.84393214092,
     2.3385652297246,
    48.855115166742,
     2.3594666277899);
  node
    ["leisure"="park"]
    (48.84393214092,2.3385652297246,48.855115166742,2.3594666277899);
  node
    ["leisure"="garden"]
    (48.84393214092,2.3385652297246,48.855115166742,2.3594666277899);
  node
    ["amenity"="public_building"]
    (48.84393214092,2.3385652297246,48.855115166742,2.3594666277899);
  node
    ["historic"]
    (48.84393214092,2.3385652297246,48.855115166742,2.3594666277899);
  node
    ["man_made"="tower"]
    (48.84393214092,2.3385652297246,48.855115166742,2.3594666277899);
  node
    ["man_made"="monument"]
    (48.84393214092,2.3385652297246,48.855115166742,2.3594666277899);
  node
    ["amenity"="place_of_worship"]
    (48.84393214092,2.3385652297246,48.855115166742,2.3594666277899);
  node
    ["amenity"="concert_hall"]
    (48.84393214092,2.3385652297246,48.855115166742,2.3594666277899);
  node
    ["tourism"="viewpoint"]
    (48.84393214092,2.3385652297246,48.855115166742,2.3594666277899);
  node
    ["historic"="castle"]
    (48.84393214092,2.3385652297246,48.855115166742,2.3594666277899);
  node
    ["historic"="ruins"]
    (48.84393214092,2.3385652297246,48.855115166742,2.3594666277899);
);
out ids geom;
    """)
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