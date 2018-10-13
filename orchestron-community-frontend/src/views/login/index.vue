<template>
    <div>
        <b-row>
            <b-col cols="3"></b-col>
            <b-col cols="6">
                <b-card style="margin-top: 10%;">
                    <img src="/static/img/login-logo.png" style="height: 220px;width: 100%;border-style:none;border: none;">
                  <form @submit.prevent="onSubmit">
                    <p v-if="isFormInvalid" style="color: #F04E23;" class="text-center">* Invalid Email or Password</p>
                    <b-form-input v-model="email"
                        type="email" placeholder="Email"
                        class="inline-form-control" :state="!$v.email.$invalid"></b-form-input>
                    <br>
                    <br>
                    <br>
                    <b-form-input v-model="password"
                        type="password"
                        placeholder="Password"
                        class="inline-form-control" :state="!$v.password.$invalid"></b-form-input>
                    <br>
                    <br>
                    <br>
                    <button class="login-button"
                        v-if="$v.email.$invalid && $v.password.$invalid || !$v.email.$invalid
                        && $v.password.$invalid || $v.email.$invalid && !$v.password.$invalid"
                        disabled="disabled">Login</button>
                    <button class="login-button" v-if="!$v.email.$invalid && !$v.password.$invalid" @click="onSubmit">Login</button>
                </form>
                </b-card>
            </b-col>
            <b-col cols="3"></b-col>
        </b-row>
    </div>
</template>

<script>
  import conf from '../../../configure.json'
import axios from 'axios'
import validUserCheck from '@/utils/auth'
import { required, minLength, email } from 'vuelidate/lib/validators'
export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      isFormInvalid: false,
      isLogin: false
    }
  },
  validations: {
    email: {
      required,
      email,
      minLength: minLength(1)
    },
    password: {
      required,
      minLength: minLength(1)
    }
  },
  created() {
    this.checkLogedInfo()
  },
  methods: {
    onSubmit() {
      this.isLogin = true
      if(this.isLogin){
      const baseURL = conf.API_URL
      const loginUrl = baseURL + '/api/user/token/'
      axios.post(loginUrl, {
        email: this.email,
        password: this.password
      })
        .then(res => {
          localStorage.setItem('username', res.data.username)
          localStorage.setItem('token', res.data.token)
          localStorage.setItem('superuser', res.data.superuser)
          localStorage.setItem('admin', res.data.admin)
          localStorage.setItem('email', res.data.email)
          localStorage.setItem('org', res.data.org)
          const token = localStorage.getItem('token')
          if (token && token!=='undifined') {
            this.$router.go('/org/dashboard')
          } else {
            this.$router.push({ path: '/' })
            this.isFormInvalid = true
            localStorage.removeItem('username')
            localStorage.removeItem('token')
            localStorage.removeItem('superuser')
            localStorage.removeItem('admin')
            localStorage.removeItem('email')
            localStorage.removeItem('org')
          }
        }).catch(error => {
          console.log('error',error.response.data)
          localStorage.removeItem('username')
          localStorage.removeItem('token')
          localStorage.removeItem('superuser')
          localStorage.removeItem('admin')
          localStorage.removeItem('email')
          localStorage.removeItem('org')
          this.$router.push({ path: '/' })
          this.isFormInvalid = true
        })
        }
    },
    checkLogedInfo() {
      if(!this.isLogin){
      const token = localStorage.getItem('token')
      if (token) {
        validUserCheck.get('/user/profile/')
          .then(res => {
            this.$router.push('/org/dashboard')
          }).catch(error => {
            if (error.res.status === 404) {
              this.$router.push('/not_found')
            } else if (error.res.status === 403) {
              this.$router.push('/forbidden')
            } else {
              this.$router.push('/error')
            }
        })
        }
      }
    }
  }
}
</script>

<style scoped>
.inline-form-control{
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    outline: none;
    width: 100%;
    padding: 7px;
    border: none;
    border-bottom: 1px solid #F04E23;
    background: transparent;
    margin-bottom: 10px;
    font: 16px 'Avenir';
    height: 45px;
    position: relative;
    display: inline-block;
}
.inline-form-control:hover{
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    outline: none;
    width: 100%;
    padding: 7px;
    border: none;
    border-bottom: 1px solid #F04E23;
    background: transparent;
    margin-bottom: 10px;
    font: 16px 'Avenir';
    height: 45px;
    position: relative;
    display: inline-block;
}
.inline-form-control:focus{
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    outline: none;
    width: 100%;
    padding: 7px;
    border: none;
    border-bottom: 1px solid #F04E23;
    background: transparent;
    margin-bottom: 10px;
    font: 16px 'Avenir';
    height: 45px;
    position: relative;
    display: inline-block;
}
.inline-form-control:active{
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    outline: none;
    width: 100%;
    padding: 7px;
    border: none;
    border-bottom: 1px solid #F04E23;
    background: transparent;
    margin-bottom: 10px;
    font: 16px 'Avenir';
    height: 45px;
    position: relative;
    display: inline-block;
}

.login-button {
    position: relative;
    background-color: #F04E23;
    border: none;
    font-size: 24px;
    color: #FFFFFF;
    padding: 16px;
    width: 100%;
    text-align: center;
    -webkit-transition-duration: 0.4s; /* Safari */
    transition-duration: 0.4s;
    text-decoration: none;
    overflow: hidden;
    cursor: pointer;
    border-radius: 8px;
}

.login-button:after {
    content: "";
    background: #F04E23;
    display: block;
    position: absolute;
    padding-top: 300%;
    padding-left: 350%;
    margin-left: -20px!important;
    margin-top: -120%;
    opacity: 0;
    transition: all 0.8s
}

.login-button:active:after {
    padding: 0;
    margin: 0;
    opacity: 1;
    transition: 0s
}
</style>