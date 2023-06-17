<script>
import { Link } from "svelte-routing";
import { onMount } from 'svelte';
import Icon from './components/Icon.svelte'

export let pdfs = [];

$ : if(pdfs.length) {
  pdfs = pdfs.sort(function (a, b) {
    if (a.title < b.title) {
      return -1;
    }
    if (a.title > b.title) {
      return 1;
    }
    return 0;
  });
}

</script>

<div class="sidebar">
    <ul class="whitepaper-list">
    {#each pdfs as pdf}
        <li class="whitepaper flex">
          <Icon class="mr-2 mt-1" icon={pdf.provider.toLowerCase()} />
          <Link class="a a__subtle pdf-link" to="/detail/{pdf.id}">{pdf.title}</Link>
        </li>
    {/each}
    </ul>
  </div>

<style lang="scss">

    .sidebar {
      max-width: 40rem;
      width: 100%;
      border-left: 1px solid var(--light-border-color);
    }

    .whitepaper-list {
      border-bottom: 1px solid var(--light-border-color);
      background-color: var(--card-bg);
      height: 100%;
      overflow: scroll;
    }

    .whitepaper {
      padding: var(--unit3) var(--unit4);
      color: var(--light-text-color);
      border-top: 1px solid var(--light-border-color);
    }

    @media only screen and (max-width: 1024px) {
      .sidebar {
        display: none;
      }
    }

</style>