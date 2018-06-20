import axios from 'axios'

const minioinstance = axios.create({
  headers: {
    'Authorization': 'JWT ' + localStorage.getItem('token')
  }
})
export default minioinstance
