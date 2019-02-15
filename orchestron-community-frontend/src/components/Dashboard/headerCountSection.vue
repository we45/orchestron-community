<template>
    <div>
        <!-- <b-container fluid> -->
          <div class="row">
        <div class="col-md-4 col-sm-6 col-xs-12">
          <div class="info-box">
            <span class="info-box-icon bg-red">
              <font-awesome-icon icon="hourglass" />
            </span>
            <template v-if="openVul >0">
                <router-link :to="openVulUrl">
                  <div class="info-box-content">
                    <span class="info-box-text">Open Vulnerabilities</span>
                    <span class="info-box-number">{{ openVul }}</span>
                  </div>
                </router-link>
            </template>
            <template v-else>
                <div class="info-box-content">
                  <span class="info-box-text">Open Vulnerabilities</span>
                  <span class="info-box-number">{{ openVul }}</span>
                </div>
            </template>
          </div>
        </div>
            <!--closed Vul-->
        <div class="col-md-4 col-sm-6 col-xs-12">
          <div class="info-box">
            <span class="info-box-icon bg-green">
              <font-awesome-icon icon="hourglass-end"></font-awesome-icon>
            </span>
            <template v-if="closedVul > 0">
              <router-link :to="closedVulUrl">
                <div class="info-box-content">
                  <span class="info-box-text">Closed Vulnerabilities</span>
                  <span class="info-box-number">{{ closedVul }}</span>
                </div>
              </router-link>
            </template>
            <template v-else>
              <div class="info-box-content">
                <span class="info-box-text">Closed Vulnerabilities</span>
                <span class="info-box-number">{{ closedVul }}</span>
              </div>
            </template>
          </div>
        </div>

        <!-- <div class="col-md-3 col-sm-6 col-xs-12">
          <div class="info-box">
            <span class="info-box-icon bg-yellow">
              <font-awesome-icon icon="hourglass-half"></font-awesome-icon>
            </span>
            <template v-if="unCategorised > 0">
              <router-link :to="uncategorized_vul">
            <div class="info-box-content">
              <span class="info-box-text">Uncategorized</span>
              <span class="info-box-number">{{ unCategorised  }}</span>
            </div>
              </router-link>
            </template>
            <template v-else>
              <div class="info-box-content">
                <span class="info-box-text">Uncategorized</span>
                <span class="info-box-number">{{ unCategorised  }}</span>
              </div>
            </template>
          </div>
        </div> -->

        <!-- /.col -->
        <div class="col-md-4 col-sm-6 col-xs-12">
          <div class="info-box">
            <span class="info-box-icon bg-aqua">
              <font-awesome-icon icon="history"></font-awesome-icon>
            </span>

            <div class="info-box-content">
              <span class="info-box-text">Avg Days Vul Open</span>
              <span class="info-box-number">{{ grade }}</span>
            </div>
            <!-- /.info-box-content -->
          </div>
          <!-- /.info-box -->
        </div>
        <!-- /.col -->
      </div>
        <!-- </b-container> -->
    </div>
</template>

<script>
    export default {
      name: 'headerCountSection',
      props: {
        openVul: {
          type: Number,
          required: true
        },
        closedVul: {
          type: Number,
          required: true
        },
        grade: {
          required: true
        },
        openVulUrl: {
          type: String,
          required: true
        },
        closedVulUrl: {
          type: String,
          required: true
        },
        uncategorized_vul: {
          type: String,
          required: true
        },
        unCategorised: {
          type: Number
        }
      }
    }
</script>

<style scoped>
  .title {
    font-family: 'Avenir';
    font-size: 14px;
    line-height: 1.33;
    color: #6b7784;
  }

  .open-vul-count {
    font-family: 'Avenir';
    color: #FF4C4C;
    font-size: 54px;
    font-weight: 300;
    line-height: 0.33;
  }

  .closed-vul-count {
    font-family: 'Avenir';
    color: #00AB69;
    font-size: 54px;
    font-weight: 300;
    line-height: 0.33;
  }

  .org-grade-no-data {
    font-family: 'Avenir';
    color: #d11d55;
    font-size: 54px;
    font-weight: 300;
    line-height: 0.33;
  }

  .info-box {
  display: block;
  min-height: 90px;
  background: #fff;
  width: 100%;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
  border-radius: 2px;
  margin-bottom: 15px;
}
.info-box small {
  font-size: 14px;
}
.info-box .progress {
  background: rgba(0, 0, 0, 0.2);
  margin: 5px -10px 5px -10px;
  height: 2px;
}
.info-box .progress,
.info-box .progress .progress-bar {
  border-radius: 0;
}
.info-box .progress .progress-bar {
  background: #fff;
}
.info-box-icon {
  border-top-left-radius: 2px;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 2px;
  display: block;
  float: left;
  height: 90px;
  width: 90px;
  text-align: center;
  font-size: 45px;
  line-height: 90px;
  background: rgba(0, 0, 0, 0.2);
}
.info-box-icon > img {
  max-width: 100%;
}
.info-box-content {
  padding: 5px 10px;
  margin-left: 90px;
}
.info-box-number {
  display: block;
  /*font-weight: bold;*/
  /*font-size: 18px;*/
  /*font-family: 'Avenir';*/
  text-align: center;
  padding-top: 10%;
  font-family: 'Avenir';
  /*color: #FF4C4C;*/
  font-size: 30px;
  font-weight: 200;
  line-height: 0.33;
}

.info-box-text {
  display: block;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.info-box-text {
  font-family: 'Avenir';
  font-size: 14px;
  /*text-transform: uppercase;*/
}

.description-block > .description-header {
  margin: 0;
  padding: 0;
  font-weight: 600;
  font-size: 16px;
}
.description-block > .description-text {
  text-transform: uppercase;
}
.bg-red,
.bg-yellow,
.bg-aqua,
.bg-blue,
.bg-light-blue,
.bg-green,
.bg-navy,
.bg-teal,
.bg-olive,
.bg-lime,
.bg-orange,
.bg-fuchsia,
.bg-purple,
.bg-maroon,
.bg-black,
.bg-red-active,
.bg-yellow-active,
.bg-aqua-active,
.bg-blue-active,
.bg-light-blue-active,
.bg-green-active,
.bg-navy-active,
.bg-teal-active,
.bg-olive-active,
.bg-lime-active,
.bg-orange-active,
.bg-fuchsia-active,
.bg-purple-active,
.bg-maroon-active,
.bg-black-active,
.callout.callout-danger,
.callout.callout-warning,
.callout.callout-info,
.callout.callout-success,
.alert-success,
.alert-danger,
.alert-error,
.alert-warning,
.alert-info,
.label-danger,
.label-info,
.label-warning,
.label-primary,
.label-success,
.modal-primary .modal-body,
.modal-primary .modal-header,
.modal-primary .modal-footer,
.modal-warning .modal-body,
.modal-warning .modal-header,
.modal-warning .modal-footer,
.modal-info .modal-body,
.modal-info .modal-header,
.modal-info .modal-footer,
.modal-success .modal-body,
.modal-success .modal-header,
.modal-success .modal-footer,
.modal-danger .modal-body,
.modal-danger .modal-header,
.modal-danger .modal-footer {
  color: #fff !important;
}
.bg-gray {
  color: #000;
  background-color: #d2d6de !important;
}
.bg-gray-light {
  background-color: #f7f7f7;
}
.bg-black {
  background-color: #111111 !important;
}
.bg-red,
.callout.callout-danger,
.alert-danger,
.alert-error,
.label-danger,
.modal-danger .modal-body {
  background-color: #d11d55 !important;
}
.bg-yellow,
.callout.callout-warning,
.alert-warning,
.label-warning,
.modal-warning .modal-body {
  background-color: #ff9c2c !important;
}
.bg-aqua,
.callout.callout-info,
.alert-info,
.label-info,
.modal-info .modal-body {
  background-color: #008b8f !important;
}
.bg-blue {
  background-color: #0073b7 !important;
}
.bg-light-blue,
.label-primary,
.modal-primary .modal-body {
  background-color: #3c8dbc !important;
}
.bg-green,
.callout.callout-success,
.alert-success,
.label-success,
.modal-success .modal-body {
  background-color: #00a65a !important;
}
.bg-navy {
  background-color: #001f3f !important;
}
.bg-teal {
  background-color: #39cccc !important;
}
.bg-olive {
  background-color: #3d9970 !important;
}
.bg-lime {
  background-color: #01ff70 !important;
}
.bg-orange {
  background-color: #ff851b !important;
}
.bg-fuchsia {
  background-color: #f012be !important;
}
.bg-purple {
  background-color: #605ca8 !important;
}
.bg-maroon {
  background-color: #d81b60 !important;
}
.bg-gray-active {
  color: #000;
  background-color: #b5bbc8 !important;
}
.bg-black-active {
  background-color: #000000 !important;
}
.bg-red-active,
.modal-danger .modal-header,
.modal-danger .modal-footer {
  background-color: #d33724 !important;
}
.bg-yellow-active,
.modal-warning .modal-header,
.modal-warning .modal-footer {
  background-color: #db8b0b !important;
}
.bg-aqua-active,
.modal-info .modal-header,
.modal-info .modal-footer {
  background-color: #00a7d0 !important;
}
.bg-blue-active {
  background-color: #005384 !important;
}
.bg-light-blue-active,
.modal-primary .modal-header,
.modal-primary .modal-footer {
  background-color: #357ca5 !important;
}
.bg-green-active,
.modal-success .modal-header,
.modal-success .modal-footer {
  background-color: #008d4c !important;
}
.bg-navy-active {
  background-color: #001a35 !important;
}
.bg-teal-active {
  background-color: #30bbbb !important;
}
.bg-olive-active {
  background-color: #368763 !important;
}
.bg-lime-active {
  background-color: #00e765 !important;
}
.bg-orange-active {
  background-color: #ff7701 !important;
}
.bg-fuchsia-active {
  background-color: #db0ead !important;
}
.bg-purple-active {
  background-color: #555299 !important;
}
.bg-maroon-active {
  background-color: #ca195a !important;
}
[class^="bg-"].disabled {
  opacity: 0.65;
  filter: alpha(opacity=65);
}
.text-red {
  color: #dd4b39 !important;
}
.text-yellow {
  color: #f39c12 !important;
}
.text-aqua {
  color: #00c0ef !important;
}
.text-blue {
  color: #0073b7 !important;
}
.text-black {
  color: #111111 !important;
}
.text-light-blue {
  color: #3c8dbc !important;
}
.text-green {
  color: #00a65a !important;
}
.text-gray {
  color: #d2d6de !important;
}
.text-navy {
  color: #001f3f !important;
}
.text-teal {
  color: #39cccc !important;
}
.text-olive {
  color: #3d9970 !important;
}
.text-lime {
  color: #01ff70 !important;
}
.text-orange {
  color: #ff851b !important;
}
.text-fuchsia {
  color: #f012be !important;
}
.text-purple {
  color: #605ca8 !important;
}
.text-maroon {
  color: #d81b60 !important;
}
.link-muted {
  color: #7a869d;
}
.link-muted:hover,
.link-muted:focus {
  color: #606c84;
}
.link-black {
  color: #666;
}
.link-black:hover,
.link-black:focus {
  color: #999;
}
.hide {
  display: none !important;
}
.no-border {
  border: 0 !important;
}
.no-padding {
  padding: 0 !important;
}
.no-margin {
  margin: 0 !important;
}
.no-shadow {
  box-shadow: none !important;
}
.list-unstyled,
.chart-legend,
.contacts-list,
.users-list,
.mailbox-attachments {
  list-style: none;
  margin: 0;
  padding: 0;
}
.list-group-unbordered > .list-group-item {
  border-left: 0;
  border-right: 0;
  border-radius: 0;
  padding-left: 0;
  padding-right: 0;
}
.flat {
  border-radius: 0 !important;
}
.text-bold,
.text-bold.table td,
.text-bold.table th {
  font-weight: 700;
}
.text-sm {
  font-size: 12px;
}
.jqstooltip {
  padding: 5px !important;
  width: auto !important;
  height: auto !important;
}
.bg-teal-gradient {
  background: #39cccc !important;
  background: -webkit-gradient(linear, left bottom, left top, color-stop(0, #39cccc), color-stop(1, #7adddd)) !important;
  background: -ms-linear-gradient(bottom, #39cccc, #7adddd) !important;
  background: -moz-linear-gradient(center bottom, #39cccc 0%, #7adddd 100%) !important;
  background: -o-linear-gradient(#7adddd, #39cccc) !important;
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#7adddd', endColorstr='#39cccc', GradientType=0) !important;
  color: #fff;
}
.bg-light-blue-gradient {
  background: #3c8dbc !important;
  background: -webkit-gradient(linear, left bottom, left top, color-stop(0, #3c8dbc), color-stop(1, #67a8ce)) !important;
  background: -ms-linear-gradient(bottom, #3c8dbc, #67a8ce) !important;
  background: -moz-linear-gradient(center bottom, #3c8dbc 0%, #67a8ce 100%) !important;
  background: -o-linear-gradient(#67a8ce, #3c8dbc) !important;
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#67a8ce', endColorstr='#3c8dbc', GradientType=0) !important;
  color: #fff;
}
.bg-blue-gradient {
  background: #0073b7 !important;
  background: -webkit-gradient(linear, left bottom, left top, color-stop(0, #0073b7), color-stop(1, #0089db)) !important;
  background: -ms-linear-gradient(bottom, #0073b7, #0089db) !important;
  background: -moz-linear-gradient(center bottom, #0073b7 0%, #0089db 100%) !important;
  background: -o-linear-gradient(#0089db, #0073b7) !important;
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#0089db', endColorstr='#0073b7', GradientType=0) !important;
  color: #fff;
}
.bg-aqua-gradient {
  background: #00c0ef !important;
  background: -webkit-gradient(linear, left bottom, left top, color-stop(0, #00c0ef), color-stop(1, #14d1ff)) !important;
  background: -ms-linear-gradient(bottom, #00c0ef, #14d1ff) !important;
  background: -moz-linear-gradient(center bottom, #00c0ef 0%, #14d1ff 100%) !important;
  background: -o-linear-gradient(#14d1ff, #00c0ef) !important;
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#14d1ff', endColorstr='#00c0ef', GradientType=0) !important;
  color: #fff;
}
.bg-yellow-gradient {
  background: #f39c12 !important;
  background: -webkit-gradient(linear, left bottom, left top, color-stop(0, #f39c12), color-stop(1, #f7bc60)) !important;
  background: -ms-linear-gradient(bottom, #f39c12, #f7bc60) !important;
  background: -moz-linear-gradient(center bottom, #f39c12 0%, #f7bc60 100%) !important;
  background: -o-linear-gradient(#f7bc60, #f39c12) !important;
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#f7bc60', endColorstr='#f39c12', GradientType=0) !important;
  color: #fff;
}
.bg-purple-gradient {
  background: #605ca8 !important;
  background: -webkit-gradient(linear, left bottom, left top, color-stop(0, #605ca8), color-stop(1, #9491c4)) !important;
  background: -ms-linear-gradient(bottom, #605ca8, #9491c4) !important;
  background: -moz-linear-gradient(center bottom, #605ca8 0%, #9491c4 100%) !important;
  background: -o-linear-gradient(#9491c4, #605ca8) !important;
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#9491c4', endColorstr='#605ca8', GradientType=0) !important;
  color: #fff;
}
.bg-green-gradient {
  background: #00a65a !important;
  background: -webkit-gradient(linear, left bottom, left top, color-stop(0, #00a65a), color-stop(1, #00ca6d)) !important;
  background: -ms-linear-gradient(bottom, #00a65a, #00ca6d) !important;
  background: -moz-linear-gradient(center bottom, #00a65a 0%, #00ca6d 100%) !important;
  background: -o-linear-gradient(#00ca6d, #00a65a) !important;
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#00ca6d', endColorstr='#00a65a', GradientType=0) !important;
  color: #fff;
}
.bg-red-gradient {
  background: #dd4b39 !important;
  background: -webkit-gradient(linear, left bottom, left top, color-stop(0, #dd4b39), color-stop(1, #e47365)) !important;
  background: -ms-linear-gradient(bottom, #dd4b39, #e47365) !important;
  background: -moz-linear-gradient(center bottom, #dd4b39 0%, #e47365 100%) !important;
  background: -o-linear-gradient(#e47365, #dd4b39) !important;
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#e47365', endColorstr='#dd4b39', GradientType=0) !important;
  color: #fff;
}
.bg-black-gradient {
  background: #111111 !important;
  background: -webkit-gradient(linear, left bottom, left top, color-stop(0, #111111), color-stop(1, #2b2b2b)) !important;
  background: -ms-linear-gradient(bottom, #111111, #2b2b2b) !important;
  background: -moz-linear-gradient(center bottom, #111111 0%, #2b2b2b 100%) !important;
  background: -o-linear-gradient(#2b2b2b, #111111) !important;
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#2b2b2b', endColorstr='#111111', GradientType=0) !important;
  color: #fff;
}
.bg-maroon-gradient {
  background: #d81b60 !important;
  background: -webkit-gradient(linear, left bottom, left top, color-stop(0, #d81b60), color-stop(1, #e73f7c)) !important;
  background: -ms-linear-gradient(bottom, #d81b60, #e73f7c) !important;
  background: -moz-linear-gradient(center bottom, #d81b60 0%, #e73f7c 100%) !important;
  background: -o-linear-gradient(#e73f7c, #d81b60) !important;
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#e73f7c', endColorstr='#d81b60', GradientType=0) !important;
  color: #fff;
}
.description-block .description-icon {
  font-size: 16px;
}
.no-pad-top {
  padding-top: 0;
}
.position-static {
  position: static !important;
}
.list-header {
  font-size: 15px;
  padding: 10px 4px;
  font-weight: bold;
  color: #666;
}
.list-seperator {
  height: 1px;
  background: #f4f4f4;
  margin: 15px 0 9px 0;
}
.list-link > a {
  padding: 4px;
  color: #777;
}
.list-link > a:hover {
  color: #222;
}
.font-light {
  font-weight: 300;
}
.user-block:before,
.user-block:after {
  content: " ";
  display: table;
}
.user-block:after {
  clear: both;
}
.user-block img {
  width: 40px;
  height: 40px;
  float: left;
}
.user-block .username,
.user-block .description,
.user-block .comment {
  display: block;
  margin-left: 50px;
}
.user-block .username {
  font-size: 16px;
  font-weight: 600;
}
.user-block .description {
  color: #999;
  font-size: 13px;
}
.user-block.user-block-sm .username,
.user-block.user-block-sm .description,
.user-block.user-block-sm .comment {
  margin-left: 40px;
}
.user-block.user-block-sm .username {
  font-size: 14px;
}
.img-sm,
.img-md,
.img-lg,
.box-comments .box-comment img,
.user-block.user-block-sm img {
  float: left;
}
.img-sm,
.box-comments .box-comment img,
.user-block.user-block-sm img {
  width: 30px !important;
  height: 30px !important;
}
.img-sm + .img-push {
  margin-left: 40px;
}
.img-md {
  width: 60px;
  height: 60px;
}
.img-md + .img-push {
  margin-left: 70px;
}
.img-lg {
  width: 100px;
  height: 100px;
}
.img-lg + .img-push {
  margin-left: 110px;
}
.img-bordered {
  border: 3px solid #d2d6de;
  padding: 3px;
}
.img-bordered-sm {
  border: 2px solid #d2d6de;
  padding: 2px;
}
.attachment-block {
  border: 1px solid #f4f4f4;
  padding: 5px;
  margin-bottom: 10px;
  background: #f7f7f7;
}
.attachment-block .attachment-img {
  max-width: 100px;
  max-height: 100px;
  height: auto;
  float: left;
}
.attachment-block .attachment-pushed {
  margin-left: 110px;
}
.attachment-block .attachment-heading {
  margin: 0;
}
.attachment-block .attachment-text {
  color: #555;
}
.connectedSortable {
  min-height: 100px;
}
.ui-helper-hidden-accessible {
  border: 0;
  clip: rect(0 0 0 0);
  height: 1px;
  margin: -1px;
  overflow: hidden;
  padding: 0;
  position: absolute;
  width: 1px;
}
.sort-highlight {
  background: #f4f4f4;
  border: 1px dashed #ddd;
  margin-bottom: 10px;
}
.full-opacity-hover {
  opacity: 0.65;
  filter: alpha(opacity=65);
}
.full-opacity-hover:hover {
  opacity: 1;
  filter: alpha(opacity=100);
}
.chart {
  position: relative;
  overflow: hidden;
  width: 100%;
}
.chart svg,
.chart canvas {
  width: 100% !important;
}
</style>
