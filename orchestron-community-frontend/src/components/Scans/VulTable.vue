<template>
    <div>
      <b-container fluid style="background-color: #FFFFFF;">
            <b-col cols="12">
                <br>
                <p>List of Vuls</p>
                <b-row>
                    <b-col md="6" class="my-1">
                        <b-form-input v-model="filter" placeholder="Type to Search" class="inline-form-control"/>
                    </b-col>
                    <b-col md="2"></b-col>
                    <b-col md="4" class="my-1">
                      <b-form-select :options="pageOptions" v-model="perPage"/>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col md="6" class="my-1">
                    </b-col>
                    <b-col md="6" class="my-1">
                        <b-pagination :total-rows="totalRows" :per-page="perPage" v-model="currentPage" class="my-1" align="right"/>
                    </b-col>
                </b-row>
                <b-table show-empty
                    stacked="md"
                    :items="dataItems"
                    :fields="fields"
                    :current-page="currentPage"
                    :per-page="perPage"
                    :filter="filter"
                    :sort-by.sync="sortBy"
                    :sort-desc.sync="sortDesc"
                    @filtered="onFiltered"
                    class="m2_top">
                    <template slot="sev" slot-scope="row">
                        <div class="high-vul-severity-line" v-if="row.item.sev===3"></div>
                        <div class="medium-vul-severity-line" v-if="row.item.sev===2"></div>
                        <div class="low-vul-severity-line" v-if="row.item.sev===1"></div>
                        <div class="info-vul-severity-line" v-if="row.item.sev===0"></div>
                    </template>
                    <template slot="name" slot-scope="row">
                      <router-link :to="row.item.url">
                        <p class="title">{{row.item.name}}</p>
                      </router-link>
                        <b-row>
                            <b-col cols="4">
                                <p>
                                    <span class="sub-title">CWE</span>
                                    <span class="sub-divider">:</span>
                                    <span class="sub-value">{{ row.item.cwe }}</span>
                                </p>
                            </b-col>
                        </b-row>
                    </template>
                </b-table>
            </b-col>
        </b-container>
    </div>
</template>

<script>
  const items = []
  export default {
    name: 'VulTable',
    data() {
      return {
        counter: 45,
        max: 200,
        items: '',
        fields: [
          { key: 'sev', label: ' ', sortable: true, 'class': 'title' },
          { key: 'name', label: 'Vulnerability Name', sortable: true, 'class': 'title' }
        ],
        currentPage: 1,
        perPage: 5,
        totalRows: items.length,
        pageOptions: [5, 10, 15],
        sortBy: null,
        sortDesc: false,
        filter: null,
        modalInfo: { title: '', content: '' }
      }
    },
    props: {
      dataItems: {
        type: Array,
        required: true
      }
    },
    created: function() {
      this.items = this.dataItems
    },
    computed: {
      sortOptions() {
        return this.fields
          .filter(f => f.sortable)
          .map(f => { return { text: f.label, value: f.key } })
      }
    },
    methods: {
      onFiltered(filteredItems) {
        this.totalRows = filteredItems.length
        this.currentPage = 1
      },
      viewIndividualVul(app, name, cwe) {
        const encodedApp = btoa(unescape(encodeURIComponent(app)))
        const encodedName = btoa(unescape(encodeURIComponent(name)))
        const encodedCwe = btoa(unescape(encodeURIComponent(cwe)))
        this.$router.push({ path: '/org/individual_vul/' + encodedApp + '/' + encodedName + '/' + encodedCwe })      }
    }
  }

</script>

<style scoped>
  .title {
    font-family: 'Avenir';
    font-size: 14px;
    font-weight: 600;
    line-height: 0.99;
    text-align: left;
    color: #232328;
  }

  .high-vul-severity-line {
    width: 5px;
    height: 38px;
    background-color: #d11d55;
    margin-top: 15%;
  }

  .medium-vul-severity-line {
    width: 5px;
    height: 38px;
    background-color: #ff9c2c;
    margin-top: 15%;
  }

  .low-vul-severity-line {
    width: 5px;
    height: 38px;
    background-color: #008b8f;
    margin-top: 15%;
  }

  .info-vul-severity-line {
    width: 5px;
    height: 38px;
    background-color: #1d1e52;
    margin-top: 15%;
  }

  .sub-title {
    width: 200px;
    height: 12px;
    font-family: 'Avenir';
    font-size: 12px;
    font-weight: 600;
    line-height: 1.33;
    text-align: left;
    color: #6b7784;
  }

  .sub-divider {
    width: 10px;
    height: 12px;
    font-family: 'Avenir';
    font-size: 12px;
    font-weight: 600;
    line-height: 1.33;
    text-align: center;
    color: #6b7784;
  }

  .sub-value {
    width: 100px;
    height: 12px;
    font-family: 'Avenir';
    font-size: 12px;
    font-weight: 600;
    line-height: 1.33;
    text-align: center;
    color: #6b7784;
  }

  .inline-form-control {
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    outline: none;
    width: 100%;
    padding: 7px;
    border: none;
    border-bottom: 1px solid #ddd;
    background: transparent;
    margin-bottom: 10px;
    font: 16px 'Avenir';
    height: 45px;
    position: relative;
    display: inline-block;
  }
</style>
