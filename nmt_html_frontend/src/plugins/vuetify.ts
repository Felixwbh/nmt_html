import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import 'vuetify/src/stylus/app.styl';
import zhHans from 'vuetify/src/locale/zh-Hans';

Vue.use(Vuetify, {
  iconfont: 'md',
  lang: {
    locales: {zhHans},
    current: 'zh-Hans',
  },
});
