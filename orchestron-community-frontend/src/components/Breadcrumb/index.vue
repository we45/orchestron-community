<template>
  <div>
    <b-container fluid>
      <br>
      <ol class="breadcrumb breadcrumb-arrow">
        <template v-for="(item,index)  in levelList">
          <li>
            <router-link :to="item.path" class="routerTag">{{item.title}}</router-link>
          </li>
        </template>
      </ol>
    </b-container>
  </div>
</template>

<script>

export default {
  created() {
    this.getBreadcrumb()
  },
  data() {
    return {
      levelList: '',
      breadCrumbList: []
    }
  },
  watch: {
    $route() {
      this.getBreadcrumb()
    }
  },
  methods: {
    checkPathExistValue(val) {
      return this.breadCrumbList.some(function(el) {
        return el.title === val
      })
    },
    getBreadcrumb() {
      const matched = this.$route.matched.filter(item => item.name)
      const first = matched[0]
      const firstPathSplit = first.path.split(':')
      var main_path = first.path
      var path_data = ''
      if (firstPathSplit[0] !== undefined) {
        path_data = firstPathSplit[0]
      }
      if (firstPathSplit[1] !== undefined) {
        const pathOne = firstPathSplit[1].split('/')[0]
        const pathTwo = this.$route.params[pathOne]
        path_data = main_path.replace(':' + pathOne, pathTwo + '/')
      }
      if (firstPathSplit[2] !== undefined) {
        const pathOne = firstPathSplit[1].split('/')[0]
        const pathTwo = this.$route.params[pathOne]
        const pathThree = firstPathSplit[2].split('/')[0]
        const pathFour = this.$route.params[pathThree]
        path_data = main_path.replace(':' + pathOne, pathTwo).replace(':' + pathThree, pathFour + '/')
      }
      if (firstPathSplit[3] !== undefined) {
        const pathOne = firstPathSplit[1].split('/')[0]
        const pathTwo = this.$route.params[pathOne]
        const pathThree = firstPathSplit[2].split('/')[0]
        const pathFour = this.$route.params[pathThree]
        const pathFive = firstPathSplit[3].split('/')[0]
        const pathSix = this.$route.params[pathFive]
        path_data = main_path.replace(':' + pathOne, pathTwo).replace(':' + pathThree, pathFour).replace(':' + pathFive, pathSix)
      }
      if (firstPathSplit[4] !== undefined) {
        const pathOne = firstPathSplit[1].split('/')[0]
        const pathTwo = this.$route.params[pathOne]
        const pathThree = firstPathSplit[2].split('/')[0]
        const pathFour = this.$route.params[pathThree]
        const pathFive = firstPathSplit[3].split('/')[0]
        const pathSix = this.$route.params[pathFive]
        const pathSeven = firstPathSplit[4].split('/')[0]
        const pathEight = this.$route.params[pathSeven]
        path_data = main_path.replace(':' + pathOne, pathTwo).replace(':' + pathThree, pathFour).replace(':' + pathFive, pathSix).replace(':' + pathSeven, pathEight)
      }
      if (firstPathSplit[5] !== undefined) {
        const pathOne = firstPathSplit[1].split('/')[0]
        const pathTwo = this.$route.params[pathOne]
        const pathThree = firstPathSplit[2].split('/')[0]
        const pathFour = this.$route.params[pathThree]
        const pathFive = firstPathSplit[3].split('/')[0]
        const pathSix = this.$route.params[pathFive]
        const pathSeven = firstPathSplit[4].split('/')[0]
        const pathEight = this.$route.params[pathSeven]
        const pathNine = firstPathSplit[5].split('/')[0]
        const pathTen = this.$route.params[pathNine]
        path_data = main_path.replace(':' + pathOne, pathTwo).replace(':' + pathThree, pathFour).replace(':' + pathFive, pathSix).replace(':' + pathSeven, pathEight).replace(':' + pathNine, pathTen)
      }

      const getBread = localStorage.getItem('breadcrumbs')
      if (getBread) {
        const convertedObj = JSON.parse(getBread)
        if (convertedObj.length > 0) {
          this.breadCrumbList = convertedObj
        }
      }
      if (this.breadCrumbList.length > 0) {
        if (this.checkPathExistValue(first.name) === false) {
          this.breadCrumbList.push(
            { title: first.name, path: path_data }
          )
        }
        if (this.breadCrumbList.length > 5) {
          this.breadCrumbList.shift()
        }
      } else {
        this.breadCrumbList.push(
          { title: first.name, path: path_data }
        )
      }
      if (this.breadCrumbList.length === 1) {
        localStorage.setItem('breadcrumbs', JSON.stringify(this.breadCrumbList))
        const getBread = localStorage.getItem('breadcrumbs')
        const convertedObj = JSON.parse(getBread)
        this.breadCrumbList = convertedObj
      }

      if (this.breadCrumbList > 1) {
        if (this.checkPathExistValue(first.name) === false) {
          this.breadCrumbList.push(
            { title: first.name, path: path_data }
          )
        }
        if (this.breadCrumbList.length > 5) {
          this.breadCrumbList.shift()
        }
      }

      // if(this.breadCrumbList.length < 1){
      //   console.log("bread crumb ", this.breadCrumbList)
      //     localStorage.setItem('breadcrumbs', JSON.stringify(this.breadCrumbList))
      // }

      // const getBread = localStorage.getItem('breadcrumbs')

      // const getBread = localStorage.getItem('breadcrumbs')
      // const convertedObj = JSON.parse(getBread)
      // this.levelList = convertedObj

      let i = 0
      for (const item of this.breadCrumbList) {
        if (item.title === first.name) {
          this.breadCrumbList = this.breadCrumbList.slice(0, i + 1)
          const matched = this.breadCrumbList
          this.levelList = matched
        }
        i = i + 1
      }
      if (first.name === 'Dashboard') {
        this.levelList = []
        this.breadCrumbList = []
        this.breadCrumbList.push(
          { title: first.name, path: path_data }
        )
        this.levelList = this.breadCrumbList
      }
      localStorage.setItem('breadcrumbs', JSON.stringify(this.levelList))
      if (this.levelList === null) {
        this.levelList = []
        this.breadCrumbList = []
        this.breadCrumbList.push(
          { title: first.name, path: path_data }
        )
        this.levelList = this.breadCrumbList
      }
    }
  }
}
</script>

<style>
.breadcrumb-arrow {
    height: 26px;
    padding: 0;
    line-height: 26px;
    list-style: none;
    background-color: transparent;

}
.breadcrumb-arrow li:first-child a {
    border-radius: 4px 0 0 4px;
    -webkit-border-radius: 4px 0 0 4px;
    -moz-border-radius: 4px 0 0 4px
}
.breadcrumb-arrow li, .breadcrumb-arrow li .routerTag, .breadcrumb-arrow li span {
    display: inline-block;
    vertical-align: top
}
.breadcrumb-arrow li:not(:first-child) {
    margin-left: -5px
}
.breadcrumb-arrow li+li:before {
    padding: 0;
    content: ""
}
.breadcrumb-arrow li span {
    padding: 0 5px
}
.breadcrumb-arrow li .routerTag, .breadcrumb-arrow li:not(:first-child) span {
    height: 26px;
    padding: 0 10px 0 25px;
    line-height: 26px
}
.breadcrumb-arrow li:first-child .routerTag {
    padding: 0 5px
}
.breadcrumb-arrow li .routerTag {
    position: relative;
    color: #fff;
    text-decoration: none;
    background-color: #F37653;
    border: 1px solid #F37653;
  font-family: 'Avenir';
}
.breadcrumb-arrow li:first-child .routerTag {
    padding-left: 5px
}
.breadcrumb-arrow li .routerTag:after, .breadcrumb-arrow li .routerTag:before {
    position: absolute;
    top: -1px;
    width: 0;
    height: 0;
    content: '';
    border-top: 14px solid transparent;
    border-bottom: 13px solid transparent
}
.breadcrumb-arrow li .routerTag:before {
    right: -10px;
    z-index: 3;
    border-left-color: #F37653;
    border-left-style: solid;
    border-left-width: 10px
}
.breadcrumb-arrow li .routerTag:after {
    right: -11px;
    z-index: 2;
    border-left: 10px solid #FFFFFF;
}
.breadcrumb-arrow li .routerTag:focus, .breadcrumb-arrow li .routerTag:hover {
    background-color: #F37653;
    border: 1px solid #F37653;
}
.breadcrumb-arrow li .routerTag:focus:before, .breadcrumb-arrow li .routerTag:hover:before {
    border-left-color: #F37653;
}
.breadcrumb-arrow li .routerTag:active {
    background-color: #F37653;
    border: 1px solid #F37653;
}
.breadcrumb-arrow li .routerTag:active:after, .breadcrumb-arrow li .routerTag:active:before {
    border-left-color: #F37653;
}
.breadcrumb-arrow li span {
    color: #434a54
}
</style>
