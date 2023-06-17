<script>
  import { Router, Route, Link } from "svelte-routing";
  import { onMount } from 'svelte'
  import Index from "./Index.svelte";
  import Detail from "./Detail.svelte";
  import WhitepaperList from "./WhitepaperList.svelte";

  let pdfs = [];

  onMount(async () => {
    const pdf_res = await fetch("/api/index");
    if(!pdfs.length) {
      pdfs = await pdf_res.json();
    }
  });

  // const systemTheme = (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  // document.documentElement.setAttribute('data-theme', systemTheme);

</script>

<div class="wrapper">
<Router>
    <Route path="/" let:params>
      <Index {params} {pdfs} />
    </Route>
    <Route path="/detail/:id" let:params>
      <Index {params} {pdfs} />
    </Route>
    <WhitepaperList {pdfs}></WhitepaperList>
</Router>
</div>

<style lang="scss">

.wrapper {
  margin: 0 auto;
  height: 100vh;
  display: flex;
}

</style>
