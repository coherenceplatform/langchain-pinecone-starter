<script>
    export let size = 50;
    export let color = 'currentColor';
    export let mashing = false;
</script>

<div class="animated-logo" class:mashing>
    <svg width="{size}" height="{size}" viewBox="0 0 780 780" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path fill="{color}" d="M124 264h536v4H124z" />
      <path fill="{color}" d="M268 120h248v4H268z" />
      <path fill="{color}" d="M120 512V268h4v244z" />
      <path fill="{color}" d="M656 512V268h4v244z" />
      <path fill="{color}" d="M268 656h248v4H268z" />
      <path fill="{color}" d="M264 656V120h4v536z" />
      <path fill="{color}" d="M388 660V120h4v540z" />
      <path fill="{color}" d="M120 512h537v4H120z" />
      <path fill="{color}" d="M120 388h540v4H120z" />
      <path fill="{color}" d="M512 664V124h4v540z" />
      <path class="aa animate" fill-rule="evenodd" clip-rule="evenodd" d="M511.976 536h4.048C526.309 597.305 574.695 645.691 636 655.976v4.048C574.695 670.309 526.309 718.695 516.024 780h-4.048C501.691 718.695 453.305 670.309 392 660.024v-4.048C453.305 645.691 501.691 597.305 511.976 536Z" fill="{color}" />
      <path class="b animate" fill-rule="evenodd" clip-rule="evenodd" d="M119.976 392h4.048C134.309 453.305 182.695 501.691 244 511.976v4.048C182.695 526.309 134.309 574.695 124.024 636h-4.048C109.691 574.695 61.306 526.309 0 516.024v-4.048C61.305 501.691 109.691 453.305 119.976 392Z" fill="{color}" />
      <path class="c animate" fill-rule="evenodd" clip-rule="evenodd" d="M655.976 144h4.048C670.309 205.305 718.695 253.691 780 263.976v4.048C718.695 278.309 670.309 326.695 660.024 388h-4.048C645.691 326.695 597.305 278.309 536 268.024v-4.048C597.305 253.691 645.691 205.305 655.976 144Z" fill="{color}" />
      <path class="d animate" fill-rule="evenodd" clip-rule="evenodd" d="M263.976 0h4.048C278.309 61.305 326.695 109.691 388 119.976v4.048C326.695 134.309 278.309 182.695 268.024 244h-4.048C253.691 182.695 205.305 134.309 144 124.024v-4.048C205.305 109.691 253.691 61.305 263.976 0Z" fill="{color}" />
      <path class="e animate" fill-rule="evenodd" clip-rule="evenodd" d="M512.749 46.69h2.499c6.349 37.843 36.217 67.711 74.059 74.06v2.498c-37.842 6.349-67.71 36.217-74.059 74.06h-2.499c-6.349-37.843-36.216-67.711-74.059-74.06v-2.498c37.843-6.349 67.71-36.217 74.059-74.06Z" fill="{color}" />
      <path class="f animate" fill-rule="evenodd" clip-rule="evenodd" d="M120.749 190.69h2.499c6.349 37.843 36.217 67.711 74.059 74.06v2.498c-37.842 6.349-67.71 36.217-74.059 74.06h-2.499c-6.349-37.843-36.216-67.711-74.059-74.06v-2.498c37.843-6.349 67.71-36.217 74.059-74.06Z" fill="{color}" />
      <path class="g animate" fill-rule="evenodd" clip-rule="evenodd" d="M656.749 438.69h2.499c6.349 37.843 36.217 67.711 74.059 74.06v2.498c-37.842 6.349-67.71 36.217-74.059 74.06h-2.499c-6.349-37.843-36.216-67.711-74.059-74.06v-2.498c37.843-6.349 67.71-36.217 74.059-74.06Z" fill="{color}" />
      <path class="h animate" fill-rule="evenodd" clip-rule="evenodd" d="M264.75 582.69h2.499c6.348 37.843 36.216 67.71 74.059 74.059v2.499c-37.843 6.349-67.711 36.217-74.059 74.059h-2.499c-6.349-37.842-36.217-67.71-74.06-74.059v-2.499c37.843-6.349 67.711-36.216 74.06-74.059Z" fill="{color}" />
    </svg>
</div>

<style lang="scss">

.animate {
  animation: twinkle 0.8s cubic-bezier(0, 0, 0, 1) infinite;
  transform-origin: 66% 90%;
}

.animated-logo {
  transition: transform var(--base-transition);
  will-change: transform;

  &.mashing {
    transform: scale(0.75);
  }
}

.aa {
  transform-origin: 66% 85%;
  animation-delay: -0.025s;
}
.b {
  transform-origin: 15% 66%;
  animation-delay: -0.05s;
}
.c {
  transform-origin: 85% 34%;
  animation-delay: -0.075s;
}
.d {
  transform-origin: 34% 15%;
  animation-delay: -0.1s;
}
.e {
  transform-origin: 66% 15%;
  animation-delay: -0.5s;
}
.f {
  transform-origin: 16% 34%;
  animation-delay: -0.525s;
}
.g {
  transform-origin: 85% 66%;
  animation-delay: -0.55s;
}
.h {
  transform-origin: 34% 85%;
  animation-delay: -0.575s;
}

@keyframes twinkle {
  0% {
    transform: scale(0.25);
  }
  50% {
    transform: scale(1);
  }
  100% {
    transform: scale(0.25);
  }
}
@keyframes twinklelonger {
  0% {
    transform: scale(0.25);
  }
  25% {
    transform: scale(1);
  }
  75% {
    transform: scale(1);
  }
  100% {
    transform: scale(0.25);
  }
}

</style>