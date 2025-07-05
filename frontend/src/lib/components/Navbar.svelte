<script>
  import { isAuthenticated, token } from '$lib/stores/auth';
  import { goto } from '$app/navigation';

  function logout() {
    document.cookie = 'token=; Max-Age=0; path=/';
    token.set('');
    isAuthenticated.set(false);
    goto('/login');
  }
</script>

<nav class="bg-white border-b border-gray-200 shadow-sm px-6 py-3 flex items-center justify-between sticky top-0 z-50">
  <div class="flex items-center space-x-8">
    <a href="/" class="text-xl font-semibold text-indigo-600 tracking-wide">IssueTracker</a>
    {#if $isAuthenticated}
      <a href="/issues" class="text-gray-700 hover:text-indigo-600 text-sm font-medium">Issues</a>
      <a href="/dashboard" class="text-gray-700 hover:text-indigo-600 text-sm font-medium">Dashboard</a>
    {/if}
  </div>
  <div>
    {#if $isAuthenticated}
      <button
        on:click={logout}
        class="bg-red-500 hover:bg-red-600 text-white text-sm font-medium px-4 py-1.5 rounded-md shadow-sm"
      >
        Logout
      </button>
    {:else}
      <a href="/login" class="text-sm text-gray-600 hover:text-indigo-600 font-medium mr-4">Login</a>
      <a href="/register" class="text-sm text-white bg-indigo-600 hover:bg-indigo-700 font-medium px-4 py-1.5 rounded-md shadow">Register</a>
    {/if}
  </div>
</nav>
