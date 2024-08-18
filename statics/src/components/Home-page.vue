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
            <button id="stopBtn" class="btn btn-primary float-right" @click="stop()">Stop</button>
            <button id="clearBtn" class="btn btn-primary float-right" @click="clearInput()">Clear Context</button>
            <router-link id="uploadBtn" class="btn btn-primary float-right" :to="{name: 'Upload Image', params: {}}">Upload a File </router-link>
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
        this.controller = null; // Store the AbortController instance for managing fetch cancellations
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
            const promptInput = document.getElementById("promptInput");
            const queryBtn = document.getElementById("queryBtn");
            const stopBtn = document.getElementById("stopBtn");
            const resultText = document.getElementById("resultText");
            let apiResponse;
            if (!promptInput.value) {
                alert("Please enter a prompt.");
                return;
            }
            window.message = promptInput.value;
            queryBtn.disabled = true;
            stopBtn.disabled = false;
            resultText.innerHTML += "<br/><br/><span style='color: lightblue;'>Prompt: " + promptInput.value + "</span><br/><br/>";
            this.controller = new AbortController();
            const signal = this.controller.signal;
            try {
                debugger;

                $.ajax(this.API_URL, {
                    method: 'POST',
                    data: JSON.stringify({
                        message: window.message,
                    }),
                    success: function(res) {
                        debugger;
                    },
                    error: function(e) {
                        debugger;
                    },
                });

                // const response = await fetch(this.API_URL, {
                //     method: "POST",
                //     headers: {
                //         "Content-Type": "application/json",
                //         // Authorization: `Bearer ${this.API_KEY}`,
                //     },
                //     body: JSON.stringify({
                //         message: window.message,
                //     }),
                //     signal, // Attach the abort signal
                // });
                // promptInput.value = "";
                // if (response.ok) {
                //     const reader = response.body?.pipeThrough(new TextDecoderStream()).getReader();
                //     if (!reader) return;
                //     // eslint-disable-next-line no-constant-condition
                //     while (true) {
                //         const {value, done} = await reader.read();
                //         if (done) break; // Exit the loop if reading is complete
                //         let dataDone = false;
                //         const arr = value.split('\n'); // Split streamed data into lines
                //         arr.forEach((data) => {
                //             if (data.length === 0 || data.startsWith(':')) return; // Ignore empty and comment lines
                //             if (data === 'data: [DONE]') {
                //                 dataDone = true;
                //                 return;
                //             }
                //             const json = JSON.parse(data.substring(6)); // Parse each JSON data line
                //             if (json.choices && json.choices[0] && json.choices[0].delta && json.choices[0].delta.content) {
                //                 var content = json.choices[0].delta.content;
                //                 if (typeof content !== 'undefined' && content !== null) {
                //                     resultText.innerHTML += content;
                //                     apiResponse += content;
                //                 }
                //             }
                //         });
                //         if (dataDone) break;
                //     }
                // } else {
                //     console.error('API request failed with status:', response.status);
                //     resultText.innerHTML += 'Failed to fetch data.';
                // }
                // window.message = apiResponse;
                // let regex = /```(\w+)?\n?(.*?)```/gs;
                // resultText.innerHTML = resultText.innerHTML.replace(regex, (match, lang, code) => {
                //     const languageClass = lang ? ` class="language-${lang}"` : '';
                //     return `<pre><code${languageClass}>${code}</code></pre>`;
                // });
                // resultText.innerHTML += "<br/><span style='color: gray;'>[End of Response]</span><br/><br/>";
                // apiResponse = "";
            } catch (error) {
                debugger;
                if (signal.aborted) {
                    resultText.innerText = "Request aborted.";
                } else {
                    console.error("Error:", error);
                    resultText.innerText = "Error occurred while generating.";
                }
            } finally {
                queryBtn.disabled = false;
                stopBtn.disabled = true;
                this.controller = null;
            }
        },
        stop() {
            if (this.controller) {
                this.controller.abort();
                this.controller = null;
            }
        },
        clearInput() {
            document.getElementById("promptInput").value = "";
            document.getElementById("resultText").innerText = "How can I help you today?";
        },
  }
};
</script>