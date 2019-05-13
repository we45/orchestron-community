import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import Chartkick from 'chartkick'
import VueChartkick from 'vue-chartkick'
import Chart from 'chart.js'
import Vue2Filters from 'vue2-filters'
import vSelect from 'vue-select'
import ToggleButton from 'vue-js-toggle-button'
import Notifications from 'vue-notification'
import Vuelidate from 'vuelidate'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'normalize.css/normalize.css'// A modern alternative to CSS resets
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en'
import '@/styles/index.scss' // global css
import App from './App'
import router from './router'
import store from './store'
import '@/utils/filters.js'
// import Clipboard from 'v-clipboard'
import VueClipboard from 'vue-clipboard2'
 

import { library } from '@fortawesome/fontawesome-svg-core'
import { faHourglass, faHourglassEnd, faHourglassHalf, faHistory
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faHourglass)
library.add(faHourglassEnd)
library.add(faHourglassHalf)
library.add(faHistory)

Vue.component('font-awesome-icon', FontAwesomeIcon)
// Vue.use(Clipboard)
Vue.use(VueClipboard)
VueClipboard.config.autoSetContainer = true
Vue.use(BootstrapVue)
Vue.use(Vue2Filters)
Vue.use(VueChartkick, { Chartkick })
Vue.use(ElementUI, { locale })
Vue.component('v-select', vSelect)
Vue.use(require('vue-moment'))
Vue.use(Notifications)
Vue.use(Vuelidate)
Vue.use(ToggleButton)

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})
