<template>
  <div id="app">
    <div class="align-left loading">
      <img alt="" src="./assets/loading.gif"/>
    </div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <router-link :to="{name: 'Home'}" class="nav-link">Home</router-link>
        </li>
      </ul>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>

import {getCache, setCache} from '@/assets/cache.js'

export default {
  components: {},
  data() {
    return {
    };
  },
  methods: {
  },
  mounted() {
    let apiUrl = getCache('config', 'apiUrl');
    if (apiUrl === '') {
      apiUrl = document.location.protocol + '//' + document.location.hostname;
      if (document.location.hostname === 'localhost') {
        apiUrl += ':8000/api';
      } else {
        apiUrl += '/api';
      }
      setCache('config', 'apiUrl', apiUrl);
    }
  },
}
</script>
