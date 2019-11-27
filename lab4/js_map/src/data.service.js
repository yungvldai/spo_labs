import axios from 'axios';

function getData() {
  return axios.get('http://127.0.0.1:5000/');
}

export default { getData };