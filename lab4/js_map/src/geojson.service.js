import axios from 'axios';
import parser from './parse-stream';
import osmtogeojson from 'osmtogeojson';

function getRelation(id) {
  return axios.get(`https://www.openstreetmap.org/api/0.6/relation/${id}/full`) // test 1114193
}

function convert(osm_data) {
  let osm_json = parser.parseFromString(osm_data);
  return osmtogeojson(osm_json);
}

function compileLayer(id, color, opacity) {
  return {
    id,
    "type": "fill",
    source: id,
    "paint": {
      "fill-color": color,
      "fill-opacity": opacity
    },
    "filter": ["==", "$type", "Polygon"],
  };
}

export default {
  getRelation, convert, compileLayer
};
