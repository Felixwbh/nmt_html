import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    snackbar: {
      show: false,
      msg: '',
      color: 'blue',
    },
    user: {
      id: -1,
      username: '',
    },
  },
  mutations: {
    showSnackbar(state) {
      state.snackbar.show = true;
    },
    hideSnackbar(state) {
      state.snackbar.show = false;
    },
    setSnackbarMsg(state, msg) {
      state.snackbar.msg = msg;
    },
    setSnackbarColor(state, color) {
      state.snackbar.color = color;
    },
    setUsername(state, username) {
      state.user.username = username;
    },
    setUserID(state, id) {
      state.user.id = id;
    },
  },
  actions: {
    showInfo(context, msg) {
      context.commit('setSnackbarMsg', msg);
      context.commit('setSnackbarColor', 'blue');
      context.commit('showSnackbar');
    },
    showError(context, msg) {
      context.commit('setSnackbarMsg', msg);
      context.commit('setSnackbarColor', 'red');
      context.commit('showSnackbar');
    },
    login(context, user: { id: number, username: string }) {
      context.commit('setUsername', user.username);
      context.commit('setUserID', user.id);
    },
    logout(context) {
      context.commit('setUsername', '');
      context.commit('setUserID', -1);
    },
  },
});
