<script>
  import { token, isAuthenticated } from '$lib/stores/auth';
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';

  let username = '';
  let password = '';

  // Restore token from cookie (browser only)
  if (browser && !($isAuthenticated)) {
    const match = document.cookie.match(/(^| )token=([^;]+)/);
    const cookieToken = match ? match[2] : '';
    if (cookieToken) {
      token.set(cookieToken);
      isAuthenticated.set(true);
      goto('/');
    }
  }

  async function login() {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ username, password })
      });

      if (!res.ok) {
        const err = await res.json();
        alert(err.detail?.[0]?.msg || 'Login failed');
        return;
      }

      const data = await res.json();
      document.cookie = `token=${data.access_token}; path=/; max-age=${7 * 24 * 60 * 60}`;
      token.set(data.access_token);
      isAuthenticated.set(true);
      goto('/');
    } catch (err) {
      console.error('Login failed:', err);
      alert('Login failed');
    }
  }
</script>

<main class="min-h-screen flex items-center justify-center bg-gray-100">
  <div class="bg-white p-6 rounded shadow w-full max-w-md">
    <h2 class="text-xl font-bold mb-4">Login</h2>
    <input type="text" bind:value={username} placeholder="Username" class="border p-2 rounded w-full mb-2" />
    <input type="password" bind:value={password} placeholder="Password" class="border p-2 rounded w-full mb-4" />
    <button on:click={login} class="bg-indigo-600 text-white px-4 py-2 rounded shadow w-full">Login</button>
  </div>
</main>
<style lang="postcss">
  @reference "tailwindcss";
  :global(html) {
    background-color: theme(--color-gray-100);
  }
</style>
