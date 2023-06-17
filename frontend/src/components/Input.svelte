<script>
    import Icon from './Icon.svelte';

    export let value = '';
    export let name = '';
    export let icon = null;
    export let disabled = false;
    export let invalid = false;
    export let large = false;
    export let dataTestid = '';
    export let style = null;
    export let placeholder = null;
    export { klass as class };

    let inputElement = null;
    let klass = '';

    export function focus() {
		inputElement.focus();
	}
</script>

<div class="input-field {klass}">
    {#if icon}
        <span class="search-icon">
            <Icon icon="{icon}" size={large ? 16 : 14} color="var(--light-text-color)" />
        </span>
    {/if}
    {#if !disabled}
        <input
            type="text"
            bind:value
            bind:this={inputElement}
            class:disabled
            class:invalid
            class:large
            class:icon
            data-testid={dataTestid}
            {name}
            {style}
            {placeholder}
            on:focus
            on:blur
            on:input
            on:change
            on:keypress
            on:keydown
            on:keyup
            on:paste
        >
    {/if}
    {#if disabled}
        <input
            type="text"
            bind:value
            bind:this={inputElement}
            disabled
            class:disabled
            class:invalid
            class:large
            class:icon
            {name}
            {style}
            {placeholder}
            on:focus
            on:blur
            on:input
            on:change
            on:keypress
            on:keydown
            on:keyup
        >
    {/if}
</div>

<style lang="scss">

    .input-field {
        position: relative;
        display: flex;
        align-items: center;
    }

    .search-icon {
        display: flex;
        position: absolute;
        left: 1rem;
        color: var(--light-text-color);
    }

    .icon {
        padding-left: var(--unit5);
    }

    .large {
        padding: var(--large-field-padding);
        font-size: var(--font-size-regular);
    }

    .large.icon {
        padding: 1.2rem 1.6rem 1.2rem var(--unit5);
    }

</style>