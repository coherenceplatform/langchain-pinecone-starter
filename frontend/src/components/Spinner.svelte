<script>

    export let size = 16;
    export let color = 'currentColor';
    export let style = '';
    let klass = '';
    export { klass as class };
</script>

<div class="spinner {klass}" style="color: {color}; width: {size/10}rem; height: {size/10}rem; {style}">
    <svg width={size/2} height={size/2} viewBox="0 0 33 33" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M16.226 0h.548C18.164 8.291 24.709 14.835 33 16.226v.548C24.709 18.164 18.165 24.709 16.774 33h-.548C14.836 24.709 8.291 18.165 0 16.774v-.548C8.291 14.836 14.835 8.291 16.226 0Z" fill="currentColor"/></svg>
    <svg width={size/2} height={size/2} style="margin-left: {size/2}px;" viewBox="0 0 33 33" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M16.226 0h.548C18.164 8.291 24.709 14.835 33 16.226v.548C24.709 18.164 18.165 24.709 16.774 33h-.548C14.836 24.709 8.291 18.165 0 16.774v-.548C8.291 14.836 14.835 8.291 16.226 0Z" fill="currentColor"/></svg>
    <svg width={size/2} height={size/2} style="margin-left: {size/2}px; margin-top: {size/2}px;" viewBox="0 0 33 33" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M16.226 0h.548C18.164 8.291 24.709 14.835 33 16.226v.548C24.709 18.164 18.165 24.709 16.774 33h-.548C14.836 24.709 8.291 18.165 0 16.774v-.548C8.291 14.836 14.835 8.291 16.226 0Z" fill="currentColor"/></svg>
    <svg width={size/2} height={size/2} style="margin-top: {size/2}px;" viewBox="0 0 33 33" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M16.226 0h.548C18.164 8.291 24.709 14.835 33 16.226v.548C24.709 18.164 18.165 24.709 16.774 33h-.548C14.836 24.709 8.291 18.165 0 16.774v-.548C8.291 14.836 14.835 8.291 16.226 0Z" fill="currentColor"/></svg>
</div>

<style lang="scss">

    .spinner {
        display: flex;
        position: relative;

        svg {
            position: absolute;
            display: inline-block;
            animation: twinkle 0.5s cubic-bezier(0,0,0,1) infinite;
        }

        svg:nth-child(4) {
            animation-delay: 0s;
        }
        svg:nth-child(3) {
            animation-delay: -0.125s;
        }
        svg:nth-child(2) {
            animation-delay: -0.25s;
        }
        svg:nth-child(1) {
            animation-delay: -0.375s;
        }
    }

    @keyframes twinkle {
        0% {
            transform: scale(0);
        } 50% {
            transform: scale(1);
        } 100% {
            transform: scale(0);
        }
    }
</style>