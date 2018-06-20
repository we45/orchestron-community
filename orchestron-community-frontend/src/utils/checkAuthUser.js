
export function notValidUser() {
  localStorage.removeItem('username')
  localStorage.removeItem('token')
  localStorage.removeItem('superuser')
  localStorage.removeItem('admin')
  localStorage.removeItem('email')
  localStorage.removeItem('org')
}

export default notValidUser
