<template>
  <div>
  <el-menu class="navbar navbar-expand-sm" mode="horizontal">
    <!--<hamburger :toggleClick="toggleSideBar" :isActive="sidebar.opened"></hamburger>-->
    <img src="/static/img/logo.png" height="50px"/>
    <el-dropdown class="avatar-container" trigger="click">
      <div class="avatar-wrapper">
        <img class="user-avatar" src="/static/img/org.png" height="50px">
        <i class="el-icon-caret-bottom"></i>
      </div>
      <el-dropdown-menu class="user-dropdown" slot="dropdown">
        <router-link class="inlineBlock" to="/org/profile">
          <el-dropdown-item>
            Profile
          </el-dropdown-item>
        </router-link>
        <el-dropdown-item divided>
            <span style="display:block;" @click="logout">LogOut</span>
        </el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </el-menu>
    <breadcrumb></breadcrumb>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Breadcrumb from '@/components/Breadcrumb'
import Hamburger from '@/components/Hamburger'

export default {
  components: {
    Breadcrumb,
    Hamburger
  },
  computed: {
    ...mapGetters([
      'sidebar'
    ])
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch('ToggleSideBar')
    },
    logout() {
      localStorage.removeItem('username')
      localStorage.removeItem('token')
      localStorage.removeItem('superuser')
      localStorage.removeItem('admin')
      localStorage.removeItem('email')
      localStorage.removeItem('org')
      this.$router.push('/')
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.navbar {
  height: 50px;
  line-height: 50px;
  border-radius: 0px !important;
  .hamburger-container {
    /*line-height: 58px;*/
    /*height: 50px;*/
    /*float: left;*/
    /*padding: 0 10px;*/
  }
  .avatar-container {
    height: 50px;
    display: inline-block;
    position: absolute;
    right: 35px;
    .avatar-wrapper {
      cursor: pointer;
      margin-top: 5px;
      position: relative;
      .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 10px;
      }
      .el-icon-caret-bottom {
        position: absolute;
        right: -20px;
        top: 25px;
        font-size: 12px;
      }
    }
  }
}
</style>

