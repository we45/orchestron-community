<template>
    <div>
        <b-container fluid style="background-color: #FFFFFF;">
            <b-col cols="12">
                <b-btn @click="createModal" class="btn-orange">Create</b-btn>
                <br>
                <br>
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
                    <template slot="name" slot-scope="row">
                        <p class="title" v-if="row.item.isAdmin">{{row.item.name}}</p>
                        <p class="title" v-else="row.item.isAdmin">{{row.item.name}} - Admin</p>
                    </template>
                    <template slot="email" slot-scope="row">{{row.item.email}}</template>
                    <template slot="actions" slot-scope="row">
                        <b-button size="sm" @click="deleteUser(row.item.id)" class="mr-1 btn-orange" style="float: right">
                            Delete
                        </b-button>
                        <b-button size="sm" @click="updateUser(row.item.id)" class="mr-1 btn-orange" style="float: right">
                            Update
                        </b-button>
                    </template>
                </b-table>
            </b-col>
        </b-container>
    </div>
</template>

<script>
const items = []

export default {
  name: 'UserTable',
  data() {
    return {
      counter: 45,
      max: 200,
      items: '',
      fields: [
        { key: 'name', label: 'Name', sortable: true, 'class': 'title' },
        { key: 'email', label: 'Email', sortable: true, 'class': 'title' },
        { key: 'actions', label: ' ', 'class': 'title', sortable: false }
      ],
      currentPage: 1,
      perPage: 5,
      totalRows: items.length,
      pageOptions: [5, 10, 15],
      sortBy: null,
      sortDesc: false,
      filter: null,
      showModal: false
    }
  },
  props: {
    dataItems: {
      type: Array,
      required: true
    }
  },
  beforeUpdate() {
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
    },
    createModal() {
      this.$emit('createModal', this.showModal)
    },
    updateUser(id) {
      this.$emit('updateModal', { id: id, show: this.showModal })
    },
    deleteUser(id) {
      this.$emit('deleteModal', { id: id, show: this.showModal })
    }
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

  .btn-orange {
    color: #ff542c;
    background-color: #FFFFFF;
    border-color: #ff542c;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange:focus,
  .btn-orange.focus {
    color: #ff542c;
    background-color: #FFFFFF;
    border-color: #ff542c;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
  }

  .btn-orange:hover {
    color: #FFFFFF;
    background-color: #ff542c;
    border-color: #FFFFFF;
    font-family: 'Avenir';
    border-radius: 14px;
    padding: 3px 12px;
    margin-bottom: 0;
    font-size: 14px;
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
