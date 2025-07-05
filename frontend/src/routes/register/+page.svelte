<script>
  import { token, isAuthenticated } from '$lib/stores/auth';
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  import { onMount } from 'svelte';

  let email = '';
  let password = '';
  let error = '';
  let success = '';

  async function handleRegister() {
    error = '';
    success = '';
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (res.ok) {
        success = 'Registration successful! Redirecting to login...';
        setTimeout(() => goto('/login'), 1500);
      } else {
        error = data.detail || JSON.stringify(data);
      }
    } catch (e) {
      error = e.message;
    }
  }

  async function handleGoogleCredential(credential) {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/google-login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_token: credential })
      });

      if (!res.ok) {
        const err = await res.json();
        alert(err.detail || 'Google login failed');
        return;
      }

      const data = await res.json();
      document.cookie = `token=${data.access_token}; path=/; max-age=${7 * 24 * 60 * 60}`;
      token.set(data.access_token);
      isAuthenticated.set(true);
      goto('/');
    } catch (err) {
      console.error('Google login failed:', err);
      alert('Google login failed');
    }
  }

  onMount(() => {
    if (browser && window.google) {
      window.google.accounts.id.initialize({
        client_id: `${import.meta.env.VITE_GOOGLE_CLIENT_ID}`,
        callback: (response) => {
          handleGoogleCredential(response.credential);
        },
      });

      window.google.accounts.id.renderButton(
        document.getElementById("google-signin"),
        { theme: "outline", size: "large", width: "100%" }
      );
    }
  });
</script>

<svelte:head>
  <script src="https://accounts.google.com/gsi/client" async defer></script>
</svelte:head>

<main class="max-w-md mx-auto mt-8 p-4">
  <h1 class="text-2xl font-bold mb-4">Register</h1>
  {#if error}<p class="text-red-600 mb-2">{error}</p>{/if}
  {#if success}<p class="text-green-600 mb-2">{success}</p>{/if}
  <form on:submit|preventDefault={handleRegister} class="space-y-4">
    <input
      type="email"
      bind:value={email}
      placeholder="Email"
      required
      class="w-full p-2 border rounded"
    />
    <input
      type="password"
      bind:value={password}
      placeholder="Password"
      required
      class="w-full p-2 border rounded"
    />
    <button
      type="submit"
      class="w-full bg-blue-600 text-white p-2 rounded"
    >
      Register
    </button>
  </form>

  <div class="text-center my-4 text-gray-500">or</div>
  <div id="google-signin" class="w-full flex justify-center"></div>

  <p class="mt-4 text-sm">
    Already have an account? <a href="/login" class="text-blue-500">Login</a>
  </p>
</main>
