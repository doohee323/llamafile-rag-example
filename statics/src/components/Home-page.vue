<template>
  <div>
    <div class="pricing-header px-3 py-3 pt-md-5 pb-md-4 mx-auto text-center">
      <h1 class="display-5">Rag with Llamafile</h1>
      <p class="lead"></p>
    </div>
    <div class="container-fluid">
        <div class="chat">
            <div id="resultText"></div>
        </div>
        <div class="input-area">
            <input type="text" ref="promptInput" v-model="promptInput" placeholder="Enter prompt..." @keydown="enterFn"/>
            <button class="btn btn-primary float-right" :disabled="chatBtn" @click="chatFn">Chat</button>
            <router-link id="uploadBtn" class="btn btn-primary float-right" :to="{name: 'Upload Image', params: {}}">Import</router-link>
            <button class="btn btn-primary float-right" :disabled="applyBtn" @click="applyFn('applyidx')">Apply</button>
            <button class="btn btn-primary float-right" @click="reloadFn">Reload</button>
            <button class="btn btn-primary float-right" @click="resetFn">Reset</button>
        </div>
    </div>
  </div>
</template>

<script>

import $ from 'jquery';
import {getCache, setCache} from "@/assets/cache";

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
        this.mountedFn();
    },
    methods: {
        enterFn(e) {
            if (e.keyCode === 13) {
                this.chatFn();
            }
        },
        chatFn() {
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
                    _this.chatBtn = false
                    _this.setHistory();
                    _this.setFocuse();
                }
            });
        },
        applyFn(evt, cb) {
            let tmtidx = getCache('chat', 'tmtidx');
            let _this = this;
            let url = this.API_SERVER + '/api/' + evt;
            $.ajax(url, {
                method: "POST",
                timeout: 30000,
                data: JSON.stringify({
                    filename: tmtidx,
                }),
                success: function(res) {
                    _this.promptInput = "";
                    _this.loadResultText(getCache('chat', 'resultText'));
                    _this.resultText.innerHTML += `<br/><span style='color: red;'>${res.message}</span>`;
                    _this.resultText.innerHTML += "<br/><span style='color: gray;'>[End of Response]</span>";
                    setCache('chat', 'tmtidx', '');
                    _this.applyBtn = true;
                    if (cb) cb();
                },
                error: function(e) {
                    console.log('API request failed with status:', e.status);
                    _this.resultText.innerHTML += 'Failed to fetch data.';
                },
                complete: function() {
                    _this.chatBtn = false;
                    _this.setHistory();
                    setTimeout(function () {
                        _this.rescrollHistory();
                        _this.$refs.promptInput.focus();
                    }, 300);
                }
            });
        },
        reloadFn(e) {
            this.resultText.innerHTML += `<br/><span style='color: red;'>Reloading...</span>`;
            e.currentTarget.disabled = true;
            this.applyFn('reload', () => {
                e.srcElement.disabled = false;
            });
        },
        resetFn(e) {
            this.resultText.innerHTML += `<br/><span style='color: red;'>Resetting...</span>`;
            e.currentTarget.disabled = true;
            setCache('chat', 'tmtidx', '');
            setCache('chat', 'resultText', '');
            const _this = this;
            this.applyFn('reset', () => {
                e.srcElement.disabled = false;
                _this.mountedFn();
            });
        },
        setHistory() {
            setCache('chat', 'resultText', this.resultText.innerHTML);
        },
        loadResultText(resultTextHtml) {
            let regex = /```(\w+)?\n?(.*?)```/gs;
            if (resultTextHtml === '') {
                resultTextHtml = 'How can I help you today?';
            }
            this.resultText.innerHTML = resultTextHtml.replace(regex, (match, lang, code) => {
                const languageClass = lang ? ` class="language-${lang}"` : '';
                return `<pre><code${languageClass}>${code}</code></pre>`;
            });
        },
        rescrollHistory() {
            const $chatElm = $('.chat');
            $chatElm.scrollTop($chatElm[0].scrollHeight);
        },
        setFocuse(){
            const _this = this;
            setTimeout(function () {
                _this.rescrollHistory();
                _this.$refs.promptInput.focus();
            }, 300);
        },
        mountedFn() {
            this.applyBtn = getCache('chat', 'tmtidx') === '';
            this.loadResultText(getCache('chat', 'resultText'));
            this.setFocuse();
        },
    }
};
</script>