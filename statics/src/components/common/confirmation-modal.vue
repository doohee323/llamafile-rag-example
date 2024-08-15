<template>
  <div :id="id" :aria-labelledby="headerId" :tabindex="tabIndex" class="modal fade" role="dialog">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <form method="post">
          <input v-for="value in entries.map(paramValue)" :key="value" :name="paramName" :value="value" type="hidden">
          <div class="modal-header">
            <h5 :id="headerId" class="modal-title">{{ title }}</h5>
            <button :aria-label="messages.cancel" class="close" data-dismiss="modal" type="button">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body text-center">
            <div v-show="isOneEntry">
              <slot :entry="entry" name="one"></slot>
            </div>
            <div v-show="!isOneEntry">
              <slot :entries="entries" :entry-count="entryCount" name="multiple"></slot>
            </div>
            <p v-if="permanent">This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-dismiss="modal" type="button">
              Cancel
            </button>
            <button :class="`btn-${context}`" class="btn once" type="button" @click="confirm(this)">
              <slot name="confirm">Confirm</slot>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>

import $ from 'jquery';

export default {
  name: 'confirmation-modal',
  props: {
    id: {
      type: String,
      default: `confirm_1`,
    },
    title: {
      type: String,
      required: true,
    },
    entries: {
      type: Array,
      required: true,
    },
    context: {
      type: String,
      default: 'danger',
    },
    paramName: {
      type: String,
      required: true,
    },
    paramValue: {
      type: Function,
      default: e => e,
    },
    permanent: {
      type: Boolean,
      default: true,
    },
    tabIndex: {
      type: Number,
      default: -1,
    },
    confirm: {
      type: Function,
    },
  },
  data() {
    return {
      messages: {
        cancel: 'Cancel',
      },
    }
  },
  computed: {
    entry() {
      return this.entries[0] || {};
    },
    entryCount() {
      return this.entries.length;
    },
    headerId() {
      return `${this.id}_header`;
    },
    isOneEntry() {
      return this.entryCount === 1;
    },
  },
  methods: {
    show() {
      $(`#${this.id}`).modal('show');
    },
    hide() {
      $(`#${this.id}`).modal('hide');
    },
    data() {
      $(`#${this.id}`).modal('hide');
    },
  },
};

</script>