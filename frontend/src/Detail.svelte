<script>
  import Button from './components/Button.svelte';
  import Spinner from './components/Spinner.svelte';
  import Icon from './components/Icon.svelte';
  import BackgroundHeader from './components/BackgroundHeader.svelte';
  import { messageTextStore, messagesStore, sendChatMessage, deleteChatHistory } from "./lib/Chat.svelte";
  import { Link, navigate } from "svelte-routing";
  import { onMount, onDestroy } from "svelte";

let message_text = '';
let messages = [];

messageTextStore.subscribe(value => message_text = value);
messagesStore.subscribe(value => messages = value);

// use params.id to get the id from the URL
export let params;

let pdf = null;

$ : params, fetchPDF()

async function fetchPDF() {
  pdf = null
  const res = await fetch("/api/detail/" + params.id);
  pdf = await res.json();
}

function handleClose() {
  navigate("/", { replace: true });
}

</script>
<div class="close-overlay" on:click={handleClose}></div>
<div class="detail-container">
  <BackgroundHeader id={params.id} />
  <div class="control-bar flex justify-between">
    <div class="close">
      <Link to="/" class="a a__subtle pdf-nav">
        <span class="pdf-nav border-right  ">✕</span>
      </Link>
    </div>
    <div class="flex">
      {#if pdf}
        <a href="{pdf.source_url}" target="_blank" class="a pdf-link">Check out the full PDF ↗</a>
      {/if}
    </div>
  </div>
  {#if !pdf}
    <Spinner size={50} />
  {:else}
    {#if pdf}
      <div class="content-container">
        <div class="provider">
          {#if pdf.provider === 'AWS'}
            <Icon icon={pdf.provider.toLowerCase()} /> Amazon Web Services
          {:else if pdf.provider === 'GCP'}
            <Icon icon={pdf.provider.toLowerCase()} /> Google Cloud Provider
          {/if}
        </div>
        <h1 class="h1 header mt-1">{pdf.title}</h1>
        <p class="font-size-large mt-4">{pdf.description}</p>
        {#if pdf.keywords}
          <h3 class="h6 light-text-color mt-6 mb-0">Topics</h3>
          <div class="keyword-container mt-4">
            {#each pdf.keywords as keyword}
              <div class="keyword">{keyword.trim()}</div>
            {/each}
          </div>
        {/if}
      </div>
    {/if}
  {/if}
</div>

<style lang="scss">

  .detail-container {
    position: absolute;
    right: 0rem;
    background-color: var(--card-bg);
    height: 100%;
    overflow: auto;
    z-index: 2;
    box-shadow: -3rem 0 6rem 3rem rgba(0,0,0,0.25);
    animation: enter 0.3s cubic-bezier(0,0,0,1) forwards;
  }

  @keyframes enter {
    0% {
      transform: translateX(10rem);
      opacity: 0;
    } 100% {
      transform: translateX(0rem);
      opacity: 1;
    }
  }

  .keyword {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    font-size: var(--font-size-smaller);
    background-color: var(--body-background-accent);
    margin: 0.4rem;
  }

  .content-container {
    position: relative;
    z-index: 1;
    max-width: 82rem;
    width: 100%;
    margin-right: auto;
    padding-left: 8rem;
    padding-right: 8rem;
    padding-bottom: 8rem;
    padding-top: 4rem;
    //margin-top: -16rem;
    background-color: var(--card-bg);
    animation: enter2 0.3s ease forwards;
  }

  @keyframes enter2 {
    0% {
      opacity: 0;
    } 100% {
      opacity: 1;
    }
  }

  .provider {
    display: inline-block;
    padding: var(--small-padding);
    border-radius: 4rem;
    background-color: var(--body-background-accent);
    font-size: 1.4rem;
    color: var(--light-text-color);
  }

  .keyword-container {
    margin-left: -0.4rem;
  }

  .control-bar {
    border-bottom: 1px solid var(--field-border-color);
    max-width: 66rem;
    margin: 0 auto;
  }

  .pdf-nav {
    display: inline-block;
    padding: 1.5rem;
    width: 5rem;
    height: 5rem;
    text-align: center;
    color: var(--light-text-color);

    &.border-right {
      border-right: 1px solid var(--field-border-color);
    }

    &.border-left {
      border-left: 1px solid var(--field-border-color);
    }
  }

  .pdf-link {
    border-left: 1px solid var(--field-border-color);
    height: 5rem;
    color: var(--body-text-color);
    padding: 1.3rem 1.3rem 1.3rem 2rem;
  }

  .close-overlay {
    position: absolute;
    width: 100%;
    height: 100%;
    right: 40rem;
    background-color: rgba(0,0,0,0.4);
    z-index: 2;
  }

  @media only screen and (max-width: 1024px) {
    .content-container {
      padding-left: 1.5rem;
      padding-right: 1.5rem;
      padding-bottom: 1.5rem;
      padding-top: 3rem;
    }
  }

</style>