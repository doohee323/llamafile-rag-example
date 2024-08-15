<template>
  <div>
    <div class="pricing-header px-3 py-3 pt-md-5 pb-md-4 mx-auto text-center">
      <h1 class="display-5">Local data</h1>
      <p class="lead"></p>
    </div>
    <div class="container-fluid">
      <div class="col-lg-12">
          <router-link :to="{name: 'Upload Image', params: {}}"
                       class="btn btn-primary float-right">
            <span class="fas fa-upload"></span>
            Upload a File
          </router-link>
      </div>
    </div>
  </div>
</template>

<script>

import $ from 'jquery';
import {checkLogin} from "@/assets/forms";
import {getCache} from "@/assets/cache";

export default {
  data() {
    this.$root.hasAuth = getCache('session', 'hasAuth') === 'true';
    return {
      hasAuth: this.$root.hasAuth
    };
  },
  props: [],
  mounted() {
    $('.loading').hide();
    $('.cluster-link').click(function (e) {
      let url = $(e.currentTarget).attr('href');
      url = url.replaceAll('sl-336363860990', $('#aws-account').val());
      window.open(url, "_blank");
    });
  },
};
</script>