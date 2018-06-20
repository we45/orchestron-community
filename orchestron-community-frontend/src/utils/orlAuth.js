import axios from 'axios'

var orl_url = process.env.ORL_URL || 'http://localhost:8080'

const instance = axios.create({
  baseURL: orl_url
})
export default instance
