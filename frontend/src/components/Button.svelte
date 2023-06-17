<script>
    import Icon from './Icon.svelte';
    import Spinner from './Spinner.svelte';

    let klass = '';
    export { klass as class };
    export let type = 'button';
    export let large = false;
    export let href = '';
    export let target = '';
    export let loading = false;
    export let id = '';
    export let disabled = loading || false;
    export let icon = undefined;
    export let style = null;

</script>

{#if href}
<a
    {style}
    {type}
    {href}
    {target}
    {id}
    class:disabled
    class="button-link {klass}"
    class:large
    on:click
    on:mouseenter
    on:mouseleave
>
    {#if icon}
        <Icon size="{large ? 19 : 16}" icon={icon} />
        <div style="width: 1rem"></div>
    {:else if loading}
        <Spinner size="{large ? 19 : 16}" />
        <div style="width: 0.5rem"></div>
    {/if}
    <slot />
</a>
{:else}
<button
    {style}
    {type}
    {disabled}
    {id}
    class="button {klass}"
    class:large
    on:click
    on:mouseenter
    on:mouseleave
>
    {#if icon}
        <Icon size="{large ? 19 : 16}" icon={icon} />
        <div style="width: 1rem"></div>
    {:else if loading}
        <Spinner size="{large ? 19 : 16}" />
        <div style="width: 0.5rem"></div>
    {/if}
    <slot />
</button>
{/if}


<style lang="scss">

    .button {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: var(--small-padding);
        border-radius: var(--field-border-radius);
        white-space: nowrap;
        transition: background-color var(--base-transition), transform var(--base-transition), box-shadow var(--base-transition);

        &:focus {
            box-shadow: var(--field-border-focus);
        }

        &.link {
            padding: 0;
        }

        &[disabled] {
            opacity: 0.6;
            pointer-events: none;
        }
    }

    .neutral {
        background-color: var(--body-text-color);
        color: var(--body-background-color);
    }

    .primary {
        color: var(--white);
        background-color: var(--primary);
        box-shadow: var(--field-border-none);

        &:hover {
            background-color: var(--primary-hover);
        }

        &:active {
            background-color: var(--primary);
        }
    }

    .secondary {
        color: var(--body-text-color);
        background-color: var(--card-bg);
        box-shadow: inset var(--field-border);

        &:hover {
            background-color: var(--neutral-bg);
        }

        &:active {
            background-color: var(--body-background-color);
        }
    }

    .secondary__dangerous {
        color: var(--danger);
    }

    .danger {
        color: var(--white);
        background-color: var(--danger);
        box-shadow: var(--field-border-none);

        &:hover {
            background-color: var(--danger-hover);
        }

        &:active {
            background-color: var(--danger);
        }
    }

    .large {
        border-radius: var(--border-radius-small);
        font-size: var(--font-size-regular);
        padding: var(--large-padding);

        &.link {
            padding: 0;
        }
    }

    .icon {
        padding: 0.4rem;

        &.icon__large {
            padding: 1rem;
            color: var(--light-text-color);

            &:hover {
                background-color: var(--body-background-accent);
            }
        }

        &:focus {
            box-shadow: inset var(--field-border-focus);
        }

        &:hover {
            background-color: var(--card-bg);
        }
    }

    .button-link {
        display: inline-flex;
        color: var(--body-text-color);
        justify-content: center;
        align-items: center;
        padding: 1.05rem;
        font-weight: var(--font-weight-medium);
        font-size: var(--font-size-small);
        line-height: var( --font-size-small);
        transition: background-color var(--base-transition), transform var(--base-transition), box-shadow var(--base-transition);

        &.primary {
            color: var(--white);
        }

        &.neutral {
            background-color: var(--body-text-color);
            color: var(--body-background-color);
        }

        &:hover {
            text-decoration: none;
        }

        &:focus {
            box-shadow: var(--field-border-focus);
        }

        &.large {
            padding: var(--unit3);
            line-height: var( --font-size-regular);
            font-size: var(--font-size-regular);
        }
    }

</style>