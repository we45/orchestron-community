<template>
  <el-breadcrumb class="app-breadcrumb" separator="/">
    <transition-group name="breadcrumb">
      <el-breadcrumb-item v-for="(item,index)  in levelList" :key="item.path" v-if="item.meta.title">
        <span v-if="item.redirect==='noredirect'||index==levelList.length" class="no-redirect">{{item.meta.title}}</span>
        <router-link v-else :to="item.redirect||item.path">{{item.meta.title}}</router-link>
      </el-breadcrumb-item>
    </transition-group>
  </el-breadcrumb>
</template>

<script>
  var breadCumList = []
var unique_list= []
export default {
  created() {
    this.getBreadcrumb()
  },
  data() {
    return {
      levelList: null
    }
  },
  watch: {
    $route() {
      this.getBreadcrumb()
    }
  },
  methods: {
    getBreadcrumb() {
        let matched = this.$route.matched.filter(item => item.name)
        const first = matched[0]
        var ss = first.path.split(":")
        var main_path = first.path
        if(ss[0] !== undefined){
          var path_data = ss[0]
        }
        if(ss[1] !== undefined){
          var str0 = ss[1].split("/")[0]
          var str1 = this.$route.params[str0]
          var path_data = main_path.replace(':'+str0,str1+'/')
        }
        if(ss[2] !== undefined){
          var str0 = ss[1].split("/")[0]
          var str1 = this.$route.params[str0]
          var str2 = ss[2].split("/")[0]
          var str3 = this.$route.params[str2]
          var path_data = main_path.replace(':'+str0,str1).replace(':'+str2,str3+'/')
        }
        if(ss[3] !== undefined){
         var str0 = ss[1].split("/")[0]
          var str1 = this.$route.params[str0]
          var str2 = ss[2].split("/")[0]
          var str3 = this.$route.params[str2]
          var str4 = ss[3].split("/")[0]
          var str5 = this.$route.params[str4]
          var path_data = main_path.replace(':'+str0,str1).replace(':'+str2,str3).replace(':'+str4,str5)
        }
        if(ss[4] !== undefined){
         var str0 = ss[1].split("/")[0]
          var str1 = this.$route.params[str0]
          var str2 = ss[2].split("/")[0]
          var str3 = this.$route.params[str2]
          var str4 = ss[3].split("/")[0]
          var str5 = this.$route.params[str4]
          var str6 = ss[4].split("/")[0]
          var str7 = this.$route.params[str6]
          var path_data = main_path.replace(':'+str0,str1).replace(':'+str2,str3).replace(':'+str4,str5).replace(':'+str6,str7)
        }
        if(ss[5] !== undefined){
         var str0 = ss[1].split("/")[0]
          var str1 = this.$route.params[str0]
          var str2 = ss[2].split("/")[0]
          var str3 = this.$route.params[str2]
          var str4 = ss[3].split("/")[0]
          var str5 = this.$route.params[str4]
          var str6 = ss[4].split("/")[0]
          var str7 = this.$route.params[str6]
          var str8 = ss[5].split("/")[0]
          var str9 = this.$route.params[str8]
          var path_data = main_path.replace(':'+str0,str1).replace(':'+str2,str3).replace(':'+str4,str5).replace(':'+str6,str7).replace(':'+str8,str9)
        }
        function CheckFunction(){
          for(var item in unique_list){
            if(unique_list[item] === first.name){
              breadCumList[item].path = path_data
              matched = breadCumList
              this.levelList = matched
              return false
            }
          }
          return true
        }
      var chehh = CheckFunction()
      
      if(chehh){
          unique_list.push(first.name);
          breadCumList.push({"path": path_data, meta: { title: first.name}})
          if(breadCumList.length > 7){
              breadCumList.shift();
              unique_list.shift();
          }
          matched = breadCumList
          this.levelList = matched
          if(breadCumList.length !== 1){
            localStorage.setItem('breadCum', JSON.stringify(breadCumList))
          }
          else if(breadCumList.length == 1){
            const breadCumLocal = window.localStorage.getItem('breadCum');
            const breadLocalList = JSON.parse(breadCumLocal);
            if(breadLocalList !== null){
              unique_list = []
              breadCumList = breadLocalList
              for(const ss of breadCumList){
                unique_list.push(ss.meta.title)
              }
              matched = breadCumList
              this.levelList = matched
            }
            else{
              matched = breadCumList
              this.levelList = matched
            }
          }
          // else{
          //    unique_list = []
          //     for(const ss of breadCumList){
          //       unique_list.push(ss.meta.title)
          //     }
          // }

      }
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .app-breadcrumb.el-breadcrumb {
    display: inline-block;
    font-family: 'Avenir';
    font-size: 14px;
    line-height: 50px;
    margin-left: 10px;
    .no-redirect {
      color: #97a8be;
      cursor: text;
    }
  }
</style>
