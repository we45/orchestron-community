import Vue from 'vue'

Vue.filter('decode', function(value) {
  return atob(value)
})

Vue.filter('checkSev', function(value) {
  let info = 0
  let low = 0
  let medium = 0
  let high = 0
  if (value.hasOwnProperty(0)) {
    info = value[0]
  } else if (value.hasOwnProperty(1)) {
    low = value[1]
  } else if (value.hasOwnProperty(2)) {
    medium = value[2]
  } else if (value.hasOwnProperty(3)) {
    high = value[3]
  }
  const total = (info + low + medium + high)
  return total
})
