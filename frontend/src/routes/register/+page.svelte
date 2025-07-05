<script>
  import { goto } from '$app/navigation';
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
</script>

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
  <p class="mt-4 text-sm">
    Already have an account? <a href="/login" class="text-blue-500">Login</a>
  </p>
</main>

