<script>
    import { onMount, afterUpdate } from 'svelte';
    import seedrandom from 'seedrandom';
    import { makeNoise2D } from 'open-simplex-noise';

    export let id = ""; // put your id here
    let seed;
    let noise2D;
    let svgElement;

    const generateColor = (value) => `hsl(${(value + 1) * 360}, 50%, 50%)`;

    $ : id, generate()

    function generate() {
      if(svgElement) {
        seed = seedrandom(id);
        noise2D = makeNoise2D(seed());
        render();
      }
    }

    onMount(() => {
      generate();
    });

    afterUpdate(() => {
      render();
    });

    const render = () => {
      const bgVal = noise2D(0, 0);
      const circle1Val = noise2D(seed(), seed());
      const circle2Val = noise2D(seed(), seed());
      const circle1Pos = { x: seed() * svgElement.clientWidth, y: seed() * svgElement.clientHeight };
      const circle2Pos = { x: seed() * svgElement.clientWidth, y: seed() * svgElement.clientHeight };

      svgElement.style.backgroundColor = generateColor(bgVal);
      svgElement.querySelector("#circle1").setAttribute("fill", generateColor(circle1Val));
      svgElement.querySelector("#circle2").setAttribute("fill", generateColor(circle2Val));
      svgElement.querySelector("#circle1").setAttribute("cx", circle1Pos.x);
      svgElement.querySelector("#circle1").setAttribute("cy", circle1Pos.y);
      svgElement.querySelector("#circle2").setAttribute("cx", circle2Pos.x);
      svgElement.querySelector("#circle2").setAttribute("cy", circle2Pos.y);
    };
  </script>

  <div class="bg-gradient-container">
    <svg bind:this={svgElement} style="width: 100%; height: 25rem;" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
      <defs>
        <filter id="blur" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur in="SourceGraphic" stdDeviation="50" />
        </filter>
      </defs>
      <circle id="circle1" r="50%" filter="url(#blur)" />
      <circle id="circle2" r="50%" filter="url(#blur)" style="mix-blend-mode: screen;" />
    </svg>
    <img class="texture" src="../texture.png">
  </div>

  <style lang="scss">

    .bg-gradient-container {
      position: relative;
      width: 100%;
      //height: calc(100vw / (40 / 9));
      overflow: hidden;
    }

    .texture {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      mix-blend-mode: overlay;
      object-fit: cover;
    }

  </style>
