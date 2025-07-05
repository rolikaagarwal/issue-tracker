<script>
  import { onMount } from 'svelte';
  import { isAuthenticated } from '$lib/stores/auth';
  import { goto } from '$app/navigation';
  import { get } from 'svelte/store';

  onMount(() => {
    if (get(isAuthenticated)) {
      goto('/issues');
    } else {
      goto('/login');
    }
  });
</script>

<style lang="postcss">
  @reference "tailwindcss";

  :global(html) {
    background-color: theme(--color-gray-100);
  }
</style>
