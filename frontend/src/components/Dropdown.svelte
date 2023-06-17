<script>
    import { createEventDispatcher } from 'svelte';
    import Icon from './Icon.svelte';

    const dispatch = createEventDispatcher();

    export let options;
    export let value;
    export let name = '';
    export let large = false;
    export let disabled = false;
    export let style = '';
    export let label = '';
    export let id = '';
    export let caret = 'downCaretBold';
    export let appSelector = false;
    let klass = '';
    export { klass as class };

    let open = false;
    let hovered = false;
    let optionFocused = false;
    let inputElement;
    let dropdownValue;

    $: selected = options.find(n => n.value === value);

    function handleInput(event) {
      open = false;
      hovered = false;
      inputElement.value = event.value;
      value = event.value;
      dispatch('change', event.value);
    }

    function handleValueBlur() {
      requestAnimationFrame(() => {
        open = optionFocused || hovered;
      });
    }

  </script>

  <div class="dropdown {klass}" {style}>
    {#if label}
      <div class="dropdown-label" class:large>{@html label}</div>
    {/if}
    <button type="button" {id} {disabled} class:large class="dropdown-button dropdown-value" on:click={() => {open = !open; dropdownValue.focus()}}  on:blur={handleValueBlur} bind:this={dropdownValue}>
      <span class="label-text mr-4" {style}>
        <slot />
        {#if selected && selected.icon}
          <Icon class="mr-1" icon={selected.icon} />
        {/if}
        { selected ? selected.label : 'Choose one' }
      </span>
      <Icon icon="{caret}" size={appSelector ? 21 : 16} color="var(--gray)"/>
      <input {name} bind:value bind:this={inputElement} class="dropdown-value-input">
    </button>
    {#if open}
    <div class="dropdown-options" style="top: {large ? '5.7rem' : '4rem'}" on:mouseenter={() => hovered = true} on:mouseleave={() => hovered = false} on:click={() => {dropdownValue.focus()}}>
      {#each options as option}
        {#if option.divided}
          <div class="dropdown-divider"></div>
        {/if}
        <button type="button" class:large class="dropdown-button dropdown-option flex align-center"
          on:click={handleInput(option)}
          on:focus={() => {optionFocused = true}}
          on:blur={() => {optionFocused = false; handleValueBlur()}}
          class:dropdown-option__selected="{value && value === option.value}"
        >
          {#if option.icon}
            <Icon class="mr-1" icon={option.icon} />
          {/if}
          { option.label }
      </button>
      {/each}
    </div>
    {/if}
  </div>

  <style lang="scss">

    .dropdown {
      position: relative;
      display: flex;
      text-align: left;
      min-width: 15rem;
    }
    .dropdown-value {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
    }

    .dropdown-button {
      &[disabled] {
          opacity: 0.6;
          background-color: var(--body-background-accent);
          pointer-events: none;
      }
    }

    .dropdown-label {
      border-top-left-radius: 0.5rem;
      border-bottom-left-radius: 0.5rem;
      background-color: var(--dropdown-menu-bg);
      box-shadow: inset var(--field-border);
      color: var(--light-text-color);

      & + .dropdown-button {
        margin-left: -0.1rem;
        border-top-left-radius: 0;
        border-bottom-left-radius: 0;
      }
    }

    .large {
        padding: var(--large-field-padding);
        font-size: var(--font-size-regular);
    }

    .label-text {
      text-align: left;
    }

    .dropdown-value-input {
      visibility: hidden;
      position: absolute;
      pointer-events: none;
    }

    .dropdown-options {
      position: absolute;
      z-index: var(--dropdown-z-index);
      width: -webkit-fill-available;
      padding: var(--unit2);
      border-radius: 0.5rem;
      background-color: var(--dropdown-menu-bg);
      animation: popin var(--base-transition) forwards;
      box-shadow: var(--medium-shadow);
    }

    @keyframes popin {
      from {
        opacity: 0;
        transform: translateY(0.5rem) scale(0.95);
      } to {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
    }

    .dropdown-option {
      position: relative;
      display: flex;
      width: 100%;
      box-shadow: none;
      text-align: left;
      z-index: 1;

      &:focus {
        z-index: 2;
      }
    }

    .dropdown-option:hover {
      background-color: var(--light-border-color)
    }

    .dropdown-option.dropdown-option__selected {
      background-color: var(--primary);
      color: white;
    }
  </style>
