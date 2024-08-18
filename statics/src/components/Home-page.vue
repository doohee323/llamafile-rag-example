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
            <input id="promptInput" type="text" placeholder="Enter prompt..."/>
            <button id="queryBtn" class="btn btn-primary float-right" @click="queryBtn()">Chat</button>
            <router-link id="uploadBtn" class="btn btn-primary float-right" :to="{name: 'Upload Image', params: {}}">Upload a File </router-link>
            <button id="clearBtn" class="btn btn-primary float-right" @click="clearInput()">Clear Context</button>
        </div>
    </div>
  </div>
</template>

<script>

import $ from 'jquery';
import {getCache} from "@/assets/cache";

export default {
    data() {
        this.API_URL = "http://localhost:8000/api/query";
        this.API_KEY = "not-needed";
        if (!window.message) {
            window.message = '';
        }
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
    methods: {
        queryBtn(){
          this.chat();
        },
        chat() {
            debugger;
            const promptInput = document.getElementById("promptInput");
            const queryBtn = document.getElementById("queryBtn");
            const resultText = document.getElementById("resultText");
            if (!promptInput.value) {
                alert("Please enter a prompt.");
                return;
            }
            window.message = promptInput.value;
            queryBtn.disabled = true;
            resultText.innerHTML += "<br/><br/><span style='color: lightblue;'>Prompt: " + promptInput.value + "</span><br/><br/>";
            $.ajax(this.API_URL, {
                method: "POST",
                timeout: 30000,
                data: JSON.stringify({
                    message: window.message,
                }),
                success: function(res) {
                    let value = res.message;
                    promptInput.value = "";
                    window.message = value;
                    let regex = /```(\w+)?\n?(.*?)```/gs;
                    resultText.innerHTML = resultText.innerHTML.replace(regex, (match, lang, code) => {
                        const languageClass = lang ? ` class="language-${lang}"` : '';
                        return `<pre><code${languageClass}>${code}</code></pre>`;
                    });
                    resultText.innerHTML += `<span style='color: red;'>${window.message}</span>`;
                    resultText.innerHTML += "<br/><span style='color: gray;'>[End of Response]</span><br/>";
                },
                error: function(e) {
                    console.log('API request failed with status:', e.status);
                    resultText.innerHTML += 'Failed to fetch data.';
                },
                complete: function() {
                    queryBtn.disabled = false;
                }
            });
        },
        clearInput() {
            document.getElementById("promptInput").value = "";
            document.getElementById("resultText").innerText = "How can I help you today?";
        },
  }
};
</script>