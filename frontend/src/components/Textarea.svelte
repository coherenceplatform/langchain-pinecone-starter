<script>
    import Icon from './Icon.svelte';
    import { onMount } from 'svelte';
    export { klass as class };
    export let value = '';
    export let name = '';
    export let search = null;
    export let disabled = false;
    export let subtle = false;
    export let invalid = false;
    export let large = false;
    export let pre = false;
    export let rows = 1;
    export let style = null;
    export let placeholder = null;
    export let inputElement = null;

    let klass = '';
    let unitHeight = large ? 34 : 20;

    function handleHeight() {
        rows = 1;
        requestAnimationFrame(() => {
            if(inputElement.value.length > 1) {
                rows = Math.floor((inputElement.scrollHeight - unitHeight)/unitHeight) + 1;
            }
        });
    }

    onMount(() => {
        rows = Math.floor(inputElement.scrollHeight/unitHeight);
    });

</script>

<div class="input-field {klass}" {style}>
    {#if search}
        <span class="search-icon">
            <Icon icon="search" />
        </span>
    {/if}
    <textarea
        type="text"
        class="textarea"
        bind:value
        bind:this={inputElement}
        class:disabled
        class:invalid
        class:large
        class:search
        class:subtle
        class:pre
        {name}
        {style}
        {rows}
        {placeholder}
        on:focus
        on:blur
        on:input
        on:change
        on:keypress
        on:keydown={handleHeight}
        on:keyup
    ></textarea>
</div>

<style lang="scss">

    .textarea {
        display: block;
        resize: none;
        width: 100%;

        &.subtle {
            background-color: transparent;
            border: none;
            box-shadow: none;
            padding: 0.5rem;

            &:focus {
                box-shadow: var(--field-border-focus);
            }
        }
    }

    .input-field {
        position: relative;
    }

    .search-icon {
        position: absolute;
        top: 0.8rem;
        left: 1rem;
        line-height: normal;
    }

    .search {
        padding-left: var(--unit5);
    }

    .large {
        padding: 1.8rem 2rem;
        border-radius: var(--border-radius-medium);
        font-size: var(--font-size-large);
    }

    .pre {
        white-space: pre;
        font-size: var(--font-size-small);
        font-family: var(--font-family-mono);
        background-color: var(--body-background-accent);
    }

</style>