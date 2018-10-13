const app = {
  state: {
    sidebar: {
      opened: true
    }
  },
  mutations: {
    TOGGLE_SIDEBAR: state => {
      // state.sidebar.opened = !state.sidebar.opened
      state.sidebar.opened = true
    }
  },
  actions: {
    ToggleSideBar: ({ commit }) => {
      commit('TOGGLE_SIDEBAR')
    }
  }
}

export default app
