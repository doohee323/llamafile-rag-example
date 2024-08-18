<template>
  <div>
    <div class="pricing-header px-3 py-3 pt-md-5 pb-md-4 mx-auto text-center">
      <h1 class="display-5">Working on Llamafile</h1>
      <p class="lead"></p>
    </div>
    <div class="container-fluid">
        <div class="chat">
            <div id="resultText">How can I help you today?</div>
        </div>
        <div class="input-area">
            <input type="text" v-model="promptInput" placeholder="Enter prompt..."/>
            <button class="btn btn-primary float-right" :disabled="chatBtn" @click="chatFn()">Chat</button>
            <router-link id="uploadBtn" class="btn btn-primary float-right" :to="{name: 'Upload Image', params: {}}">Upload a File </router-link>
            <button class="btn btn-primary float-right" :disabled="applyBtn" @click="applyFn()">Apply Context</button>
        </div>
    </div>
  </div>
</template>

<script>

import $ from 'jquery';
import {getCache} from "@/assets/cache";

export default {
    data() {
        this.API_SERVER = "http://localhost:8000";
        this.API_KEY = "not-needed";
        this.$root.hasAuth = getCache('session', 'hasAuth') === 'true';
        return {
            chatBtn: false,
            applyBtn: false,
            promptInput: '',
            hasAuth: this.$root.hasAuth
        };
    },
    props: [],
    mounted() {
        $('.loading').hide();
        this.resultText = document.getElementById("resultText");
    },
    methods: {
        chatFn() {
            debugger;
            if (this.promptInput === '') {
                alert("Please enter a prompt.");
                return;
            }
            this.chatBtn = true;
            this.resultText.innerHTML += "<br/><br/><span style='color: lightblue;'>Prompt: " + this.promptInput + "</span><br/><br/>";
            let _this = this;
            $.ajax(this.API_SERVER + '/api/query', {
                method: "POST",
                timeout: 30000,
                data: JSON.stringify({
                    message: this.promptInput,
                }),
                success: function(res) {
                    _this.promptInput = "";
                    let regex = /```(\w+)?\n?(.*?)```/gs;
                    _this.resultText.innerHTML = _this.resultText.innerHTML.replace(regex, (match, lang, code) => {
                        const languageClass = lang ? ` class="language-${lang}"` : '';
                        return `<pre><code${languageClass}>${code}</code></pre>`;
                    });
                    _this.resultText.innerHTML += `<span style='color: red;'>${res.message}</span>`;
                    _this.resultText.innerHTML += "<br/><span style='color: gray;'>[End of Response]</span><br/>";
                },
                error: function(e) {
                    console.log('API request failed with status:', e.status);
                    _this.resultText.innerHTML += 'Failed to fetch data.';
                },
                complete: function() {
                    _this.chatBtn = false;
                }
            });
        },
        applyFn() {
            debugger;
            let _this = this;
            $.ajax(this.API_SERVER + '/api/applyidx', {
                method: "POST",
                timeout: 30000,
                data: JSON.stringify({
                    message: '11.txt',
                }),
                success: function(res) {
                    _this.promptInput = "";
                    let regex = /```(\w+)?\n?(.*?)```/gs;
                    _this.resultText.innerHTML = _this.resultText.innerHTML.replace(regex, (match, lang, code) => {
                        const languageClass = lang ? ` class="language-${lang}"` : '';
                        return `<pre><code${languageClass}>${code}</code></pre>`;
                    });
                    _this.resultText.innerHTML += `<span style='color: red;'>${res.message}</span>`;
                    _this.resultText.innerHTML += "<br/><span style='color: gray;'>[End of Response]</span><br/>";
                },
                error: function(e) {
                    console.log('API request failed with status:', e.status);
                    _this.resultText.innerHTML += 'Failed to fetch data.';
                },
                complete: function() {
                    _this.chatBtn = false;
                }
            });
        },
    }
};
</script>