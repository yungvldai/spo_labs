import utils
from flask import Flask
from flask_cors import CORS, cross_origin


root_query = {'vibid': '27820001217417', 'type': '222'}
root_query.update(utils.COMMON)


root_page = utils.get_data(root_query)
json_response = root_page[7].drop([0, 12]).to_json()


app = Flask(__name__)
cors = CORS(app)


app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
@cross_origin()
def index():
    return json_response
