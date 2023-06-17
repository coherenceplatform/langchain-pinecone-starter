<script>
  import Input from './components/Input.svelte';
  import Detail from './Detail.svelte';
  import Textarea from './components/Textarea.svelte';
  import Button from './components/Button.svelte';
  import Spinner from './components/Spinner.svelte';
  import SpinnerLogo from './components/SpinnerLogo.svelte';
  import BackgroundHeader from './components/BackgroundHeader.svelte';
  import { Link, useLocation, navigate } from "svelte-routing";
  import { onMount } from "svelte";
  import { messageTextStore, messagesStore, sendChatMessage, deleteChatHistory } from "./lib/Chat.svelte";

  // use params.id to get the id from the URL
  export let params = null;
  export let pdfs = [];

  let message_text = '';
  let messages = [];
  let loading = false;
  let holdingShift = false;
  let placeholderMessage = '';
  let aiTypingIndicator;

  messageTextStore.subscribe(value => message_text = value);
  messagesStore.subscribe(value => messages = value);

  $ : if(messages.length) {
    console.log(messages)
  }

  const examples = [
    'How can I add CORS to CloudFront?',
    'How many AWS accounts should I have?',
    'How can I use GKE Autopilot to deploy my containers securely?'
  ]

  function getPDFSourceObjects(arr) {
    return arr.map(n => pdfs.find(o => o.id === n));
  }


  function sendExampleMessage(example) {
    messageTextStore.set(example);
    placeholderMessage = example;
    scrollToIndicator();
    loading = true;

    sendChatMessage().then(resp => {
      loading = false;
      setTimeout(() => {
        [...document.querySelectorAll('.line')].at(-1).scrollIntoView({ behavior: "smooth"});
      }, 16);
    })
  }

  function scrollToIndicator() {
    setTimeout(() => {
      document.querySelector('.typing-indicator').scrollIntoView({ behavior: "smooth"});
    }, 16);
  }

  function submitMessage () {
    console.log(message_text);
    placeholderMessage = message_text;
    messageTextStore.set(message_text);
    scrollToIndicator();
    loading = true;
    sendChatMessage().then(resp => {
      loading = false;
      setTimeout(() => {
        [...document.querySelectorAll('.line')].at(-1).scrollIntoView({ behavior: "smooth"});
      }, 16);
    })
  };

  function handleKeyPress(e) {
    if(e.key === 'Enter' && !holdingShift) {
      e.preventDefault();
      submitMessage();
    }
  }

  function handleNewChat() {
    deleteChatHistory().then(resp => {
      if(params && params.id) {
        navigate("/", { replace: true })
      }
    });
  }

  onMount(async () => {

      // const pdf_res = await fetch("/api/index");
      // if(!pdfs.length) {
      //   pdfs = await pdf_res.json();
      // }

      window.addEventListener('keydown', e => {
        if(e.key === 'Shift') {
          holdingShift = true;
        }
      });

      window.addEventListener('keyup', e => {
        if(e.key === 'Shift') {
          holdingShift = false;
        }
      });
  });
  </script>

  <div class="main-container w-100 flex {params ? 'main-container__locked' : ''}">
    <div class="chat-wrapper w-100">

      {#if params && params.id}
        <Detail {params}/>
      {/if}
      <div class="chat-scroll-container">
        <div class="chat-container w-100">
          {#if messages.length || loading}
              <ul class="messages">
              {#each messages as message}
                  <li class="line">
                    <div class="message font-size-large {message.role === 'human' ? 'message__user' : 'message__ai'}">
                      <span>{message.content.replace(/(\d+\.\s)/g, "\n$1")}</span>
                      {#if message.sources && message.sources.length}
                          <div class="sources mt-4">
                            {#each getPDFSourceObjects(message.sources) as source, _index}
                              {#if source}
                                <Link class="block small light-text-color mr-2" to="/detail/{source.id}">
                                  <span style="vertical-align: super; font-size: 1rem">{_index + 1}</span>
                                  {source.title}
                                </Link>
                              {/if}
                            {/each}
                          </div>
                      {/if}
                    </div>
                  </li>
              {/each}
              {#if !loading}
                <div class="line">
                  <div on:click={handleNewChat} class="message font-size-large message__newchat">Start a new chat</div>
                </div>
              {/if}
              {#if loading}
                  <li class="line">
                    <div class="message font-size-large message__user">{placeholderMessage}</div>
                  </li>
                  <div class="line" bind:this={aiTypingIndicator}>
                    <div class="message message__ai font-size-large typing-indicator"><Spinner color="var(--light-text-color)" size={24} /></div>
                  </div>
              {/if}
            </ul>
          {:else}
            <div class="example-list mt-auto">
              <div class="welcome-text mb-5">
                <div class="video-container">
                  <video style="filter: brightness(0.9)" width="100%" autoplay loop muted>
                      <source src="https://storage.googleapis.com/cbabf43da74-6b6f518d7a0e-public-assets/videos/vid-3.mp4" type="video/mp4">
                  </video>
                </div>
                <div class="welcome-text-inner">
                  <h1 class="h2 mt-3 mb-1">Whitepaper IDX</h1>
                  <h2 class="light-text-color mb-3 font-size-large">Chat with a catalog of hundreds of cloud architecture white papers and easily discover industry-leading insights and best practices. For more about the project, check out the <a class="a body-text-color" target="_blank" href="http://www.withcoherence.com/post/announcing-the-cloud-whitepaper-index">article</a> on the <a class="a body-text-color" target="_blank" href="http://www.withcoherence.com">Coherence</a> blog.</h2>
                </div>
              </div>
              {#each examples as example}
                <div class="line">
                  <div on:click={() => sendExampleMessage(example)} class="message font-size-large message__example">{example}</div>
                </div>
              {/each}
            </div>
          {/if}
        </div>
        <div class="input-container w-100">
          <Textarea placeholder="Type a message..." large disabled={loading} class="w-100" bind:value={message_text} on:keypress="{e => handleKeyPress(e)}" />
          <button class="send-button {message_text.length ? 'send-button__active' : ''}" on:click={submitMessage}>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M227.32,28.68a16,16,0,0,0-15.66-4.08l-.15,0L19.57,82.84a16,16,0,0,0-2.42,29.84l85.62,40.55,40.55,85.62A15.86,15.86,0,0,0,157.74,248q.69,0,1.38-.06a15.88,15.88,0,0,0,14-11.51l58.2-191.94c0-.05,0-.1,0-.15A16,16,0,0,0,227.32,28.68ZM157.83,231.85l-.05.14L118.42,148.9l47.24-47.25a8,8,0,0,0-11.31-11.31L107.1,137.58,24,98.22l.14,0L216,40Z"></path></svg>
          </button>
        </div>
      </div>
    </div>

  </div>

  <style lang="scss">



    .sidebar-header {
      padding: var(--unit4);
    }

    .main-container {
      margin: 0 auto;
      height: inherit;

      &.main-container__locked {
        overflow: hidden;
      }
    }

    .logo {
      position: absolute;
      top: 4rem;
      left: 4rem;
    }

    .new-chat {
      position: absolute;
      top: 4rem;
      right: 4rem;
    }

    .chat-wrapper {
      position: relative;
      margin: 0 auto;
    }

    .chat-scroll-container {
      height: calc(100vh);
      padding: 4rem 0 14rem 0;
      overflow: auto;
      background-color: var(--card-bg);

      &::after {
        content: "";
        position: absolute;
        width: 100%;
        bottom: 0;
        height: 12rem;
        background: linear-gradient(transparent, var(--card-bg) 90%);
        z-index: 0;
      }
    }

    .example-list {
      //margin-top: calc(100vh - 65rem);
    }

    .chat-container, .input-container {
      max-width: 70rem;
      margin: 0 auto;
    }

    .input-container {
      position: fixed;
      left: 0;
      right: 40rem;
      width: auto;
      margin: 0 auto;
      bottom: 5rem;
      z-index: 1;
    }

    .messages {
      list-style: none;
      padding: 0;
    }

    .message {
      display: inline-block;
      padding: var(--unit3);
      border-radius: var(--border-radius-small);
      transition: background-color 0.2s ease;

      &.message__user {
        background-color: var(--primary);
      }

      &.message__ai {
        white-space: break-spaces;
        background-color: var(--body-background-accent);
        border: 1px solid var(--light-border-color);
        padding: var(--unit3);
      }

      &.message__example {
        background-color: var(--body-background-accent);
        cursor: pointer;

        &:hover {
          background-color: var(--primary);
        }
      }

      &.message__newchat {
        background-color: transparent;
        border: 1px solid var(--field-border-color);
        cursor: pointer;
        transition: border 0.2s ease, background-color 0.2s ease;

        &:hover {
          border: 1px solid var(--primary);
          background-color: var(--primary);
        }
      }

    }

    .line + .line {
      margin-top: var(--unit3);
    }


    .send-button {
      position: absolute;
      right: 0;
      top: 0;
      padding: 1.2rem;
      border-radius: var(--border-radius-small);
      cursor: pointer;
      margin-top: 0.7rem;
      margin-right: 0.7rem;
      transition: background-color 0.2s ease;

      &.send-button__active {
        background-color: var(--primary);

        &:hover {
          background-color: var(--primary-hover);
        }
      }

      &:hover {
        background-color: var(--body-background-accent);
      }
    }

    .welcome-text {
      background-color: var(--body-background-accent);
      border-radius: 1rem;
      padding-top: 1.5rem;
    }

    // .video-container {
    //   position: relative;
    //   padding: 0 1.5rem;

    //   &:before, &:after {
    //     content: '';
    //     position: absolute;
    //     height: 100%;
    //     width: 3rem;
    //   }

    //   &::before {
    //     left: 1.5rem;
    //     background: linear-gradient(to right, var(--body-background-accent), transparent);
    //   }

    //   &::after {
    //     right: 1.5rem;
    //     background: linear-gradient(to left, var(--body-background-accent), transparent);
    //   }
    // }

    .welcome-text-inner {
      padding: 2rem;
    }

    @media only screen and (max-width: 1024px) {


      .input-container {
        right: 1.5rem;
        left: 1.5rem;
        bottom: 2rem;
      }

      .chat-scroll-container {
        padding: 2rem 1.5rem 14rem 1.5rem;
      }
    }

  </style>