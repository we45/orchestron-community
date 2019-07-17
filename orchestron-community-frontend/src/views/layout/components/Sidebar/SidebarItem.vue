<template>
    <div class="menu-wrapper" style="background-color: #F04E23; color:#FFFFFF;">
        <br/>
        <br/>
        <br/>
        <template v-for="item in routes" v-if="!item.hidden&&item.children">
            <router-link v-if="item.children.length===1 && !item.children[0].children && !item.alwaysShow || item.children.length >= 1 "
                :to="item.path+'/'+item.children[0].path"
                :key="item.children[0].name">
                <el-menu-item :index="item.path+'/'+item.children[0].path"
                    :class="{'submenu-title-noDropdown':!isNest}"
                    style="color:#FFFFFF;">
                    <template v-if="item.children[0].meta.icon == 'Dashboard'">
                        <div>
                          <span class="demo-icon icon-asset-7dashboard"
                              style="font-size: 28px;width: 30%;">&#xe800;</span>
                          <span v-if="item.children[0].meta.title" style="width: 60%;">{{ item.children[0].meta.title }}</span>
                        </div>
                    </template>
                    <template v-if="item.children[0].meta.icon == 'project'">
                         <div>
                          <span class="demo-icon icon-asset-8projects"
                              style="font-size: 26px;width: 30%; ">&#xe801;</span>
                          <span v-if="item.children[0].meta.title" style="width: 60%;" >{{ item.children[0].meta.title }}</span>
                        </div>
                    </template>
                    <template v-else-if="item.children[0].meta.icon == 'webhook'">
                        <div>
                          <span class="demo-icon icon-asset-10webhooks"
                                style="font-size: 38px;width: 26%;">&#xe803;</span>
                          <span v-if="item.children[0].meta&&item.children[0].meta.title" style="width: 60%;">{{item.children[0].meta.title}}</span>
                        </div>
                    </template>
                    <template v-else-if="item.children[0].meta.icon == 'Engagements'">
                        <div>
                          <span class="demo-icon icon-asset-15engagements2"
                                style="font-size: 31px;width: 28%;">&#xe805;</span>
                          <span v-if="item.children[0].meta&&item.children[0].meta.title" style="width: 60%;" >{{item.children[0].meta.title}}</span>
                        </div>
                    </template>

                      <template v-else-if="item.children[0].meta.icon == 'report'">
                                    <span class="demo-icon icon-asset-11bulk-actions"
                                          style="font-size: 26px;width: 30%;">&#xe804;</span>
                        <span v-if="item.children[0].meta.title" style="width: 60%;">{{ item.children[0].meta.title }}</span>
                      </template>


                    <!--  <template v-else-if="item.children[0].meta.icon == 'Engagements'">
                        <span class="demo-icon icon-asset-15engagements2"
                              style="font-size: 28px;">&#xe805;</span>
                        <span v-if="item.children[0].meta&&item.children[0].meta.title" style="margin-left: 8%;">{{item.children[0].meta.title}}</span>
                    </template> -->
                    <template v-else-if="item.children[0].meta.icon == 'settings'">
                        <span class="demo-icon icon-asset-9settings"
                              style="font-size: 24px;width: 30%;">&#xe802;</span>
                        <span v-if="item.children[0].meta&&item.children[0].meta.title" style="width: 60%;">{{item.children[0].meta.title}}</span>
                    </template>
                </el-menu-item>
            </router-link>
        </template>
    </div>
</template>

<script>
export default {
  name: 'SidebarItem',
  props: {
    routes: {
      type: Array
    },
    isNest: {
      type: Boolean,
      default: false
    }
  }
}
</script>
<style>
@font-face {
      font-family: 'fontello';
      src: url('/static/fonts/fontello.eot?80380630');
      src: url('/static/fonts/fontello.eot?80380630#iefix') format('embedded-opentype'),
           url('/static/fonts/fontello.woff?80380630') format('woff'),
           url('/static/fonts/fontello.ttf?80380630') format('truetype'),
           url('/static/fonts/fontello.svg?80380630#fontello') format('svg');
      font-weight: normal;
      font-style: normal;
    }

  .demo-icon
    {
      font-family: "fontello";
      font-style: normal;
      font-weight: normal;
      speak: none;
      display: inline-block;
      text-decoration: inherit;
      width: 1em;
      margin-right: .2em;
      text-align: center;
      font-variant: normal;
      text-transform: none;
      line-height: 1em;
      margin-left: .2em;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

</style>
<style>
  .router-link-active{
    background-color: #F5F5F5;
    color: #F04E23;
  }
  .router-link-exact-active{
    background-color: #F5F5F5;
    color: #F04E23;
  }
  .is-active{
    color: rgb(240, 78, 35)!important;
  }
  /*.submenu-title-noDropdown {
    width: 10px!important;
  }*/
  .submenu-title-noDropdown:hover{
    color: rgb(240, 78, 35)!important;
  }


</style>
