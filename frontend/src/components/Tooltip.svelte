<script>
    let klass = '';
    export { klass as class };
    export let style = '';
    export let id = '';
</script>

<div {id} class="tooltip {klass}" {style} on:mouseleave>
    <slot />
</div>

<style lang="scss">

.tooltip {
    position: absolute;
    background-color: var(--body-text-color);
    color: var(--body-background-color);
    padding: var(--large-padding);
    border-radius: var(--border-radius-small);
    font-family: var(--font-family-sans);
    font-weight: var(--font-weight-regular);
    bottom: 2rem;
    max-width: 25rem;
    width: max-content;
    z-index: var(--tooltip-z-index);

    &:after {
        content: "";
        position: absolute;
        color: var(--body-background-color);
        border: 1rem solid var(--body-text-color);
    }

    &.invert {
        background-color: var(--body-background-color);
        color: var(--body-text-color);

        &:after {
            color: var(--body-text-color);
            border: 1rem solid var(--body-background-color);
        }
    }
}


.small {
    font-size: var(--font-size-small);
    padding: var(--small-padding);
}

.top {
    transform: translateX(-50%);
    left: 50%;

    &:after {
        bottom: 0;
        margin-bottom: -1.5rem;
        left: 50%;
        transform: translateX(-50%);
        border-color: var(--body-text-color) transparent transparent transparent;
    }
}

.bottom {
    transform: translateX(-50%);
    left: 50%;

    &:after {
        top: 0;
        margin-top: -1.5rem;
        left: 50%;
        transform: translateX(-50%);
        border-color: transparent transparent var(--body-text-color) transparent;
    }
}

.right {

    &:after {
        top: 50%;
        margin-left: -1.5rem;
        left: 0;
        transform: translateY(-50%);
        border-color: transparent var(--body-text-color) transparent transparent;
    }
}

.left {
    left: 32rem;

    &:after {
        top: 50%;
        margin-left: -1.5rem;
        left: 0;
        transform: translateY(-50%);
        border-color: transparent var(--body-text-color) transparent transparent;
    }
}
</style>