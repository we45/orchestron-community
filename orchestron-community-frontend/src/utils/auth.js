import axios from 'axios'
var api_url = process.env.API_URL || 'http://localhost:8000'
var jwtToken = 'JWT ' + localStorage.getItem('token')

const instance = axios.create({
  baseURL: api_url + '/api',
  headers: {
    'Authorization': jwtToken
  }
})
export default instance
