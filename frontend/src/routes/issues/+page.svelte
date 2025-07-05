<script>
  import { isAuthenticated, token } from '$lib/stores/auth';
  import { onMount } from 'svelte';
  import { get } from 'svelte/store';
  import Navbar from '$lib/components/Navbar.svelte';

  let issues = [];
  let showModal = false;
  let confirmDeleteModal = false;
  let newIssue = { title: '', description: '', severity: 'LOW', file: null };
  let editingIssueId = null;
  let issueToDelete = null;

  function openModal(issue = null) {
    editingIssueId = issue?.id || null;
    newIssue = {
      title: issue?.title || '',
      description: issue?.description || '',
      severity: issue?.severity || 'LOW',
      file: null,
    };
    showModal = true;
  }

  function handleFile(e) {
    newIssue.file = e.target.files[0];
  }

  async function fetchIssues() {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/issues/getall`, {
        headers: { Authorization: `Bearer ${get(token)}` }
      });
      if (res.ok) {
        issues = await res.json();
      } else {
        console.error('Failed to fetch issues');
      }
    } catch (err) {
      console.error('Error:', err);
    }
  }

  async function submitIssue() {
    const isEditing = Boolean(editingIssueId);
    let res;

    if (isEditing) {
      // Assume file update not supported on PUT; use JSON
      res = await fetch(`${import.meta.env.VITE_API_URL}/issues/${editingIssueId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${get(token)}`,
        },
        body: JSON.stringify({
          title: newIssue.title,
          description: newIssue.description,
          severity: newIssue.severity,
        }),
      });
    } else {
      // Use FormData for POST with file
      const form = new FormData();
      form.append('title', newIssue.title);
      form.append('description', newIssue.description);
      form.append('severity', newIssue.severity);
      if (newIssue.file) form.append('file', newIssue.file);

      res = await fetch(`${import.meta.env.VITE_API_URL}/issues/create`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${get(token)}`,
        },
        body: form,
      });
    }

    if (res.ok) {
      showModal = false;
      await fetchIssues();
    } else {
      try {
        const err = await res.json();
        alert(err.detail || 'Failed to save issue');
      } catch (e) {
        alert('Error saving issue');
      }
    }
  }


  async function deleteIssue() {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/issues/${issueToDelete}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${get(token)}` },
      });

      if (res.ok) {
        confirmDeleteModal = false;
        await fetchIssues();
      } else {
        const err = await res.json();
        alert(err.detail || 'Failed to delete issue');
      }
    } catch (err) {
      console.error('Issue delete failed:', err);
      alert('Error deleting issue');
    }
  }

  onMount(() => {
    if (get(isAuthenticated)) fetchIssues();
  });
</script>

<Navbar />

<main class="bg-gray-50 min-h-screen px-6 py-10 border-t border-gray-200">
  <div class="flex justify-between items-center mb-4">
    <h1 class="text-2xl font-bold text-gray-700">Your Issues</h1>
    <button type="button" on:click={() => openModal()} class="bg-indigo-600 text-white px-4 py-2 rounded shadow">
      + Create Issue
    </button>
  </div>

  {#if issues.length > 0}
    <ul class="space-y-4">
      {#each issues as issue}
        <li class="flex justify-between items-start border p-4 rounded shadow bg-white">
          <div>
            <p class="font-semibold text-lg">{issue.title}</p>
            <p class="text-sm text-gray-600">{issue.description}</p>
          </div>
          <div class="flex space-x-3">
            <button type="button" on:click={() => openModal(issue)} title="Edit" class="text-blue-500 hover:text-blue-700 text-lg">
              📝
            </button>
            <button type="button" on:click={() => { confirmDeleteModal = true; issueToDelete = issue.id }} title="Delete" class="text-red-500 hover:text-red-700 text-lg">
              🗑️
            </button>
          </div>
        </li>
      {/each}
    </ul>
  {:else}
    <p class="text-gray-600">No issues found.</p>
  {/if}

  {#if showModal}
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded shadow w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">{editingIssueId ? 'Edit' : 'Create'} Issue</h2>
        <input type="text" bind:value={newIssue.title} placeholder="Title" class="w-full p-2 border rounded mb-2" />
        <textarea bind:value={newIssue.description} placeholder="Description" class="w-full p-2 border rounded mb-2"></textarea>
        <select bind:value={newIssue.severity} class="w-full p-2 border rounded mb-2">
          <option value="LOW">Low</option>
          <option value="MEDIUM">Medium</option>
          <option value="HIGH">High</option>
        </select>
        <input type="file" on:change={handleFile} class="w-full mb-4" />
        <div class="flex justify-end space-x-2">
          <button type="button" on:click={() => showModal = false} class="text-gray-600 hover:underline">Cancel</button>
          <button type="button" on:click={submitIssue} class="bg-green-600 text-white px-4 py-2 rounded shadow">Save</button>
        </div>
      </div>
    </div>
  {/if}

  {#if confirmDeleteModal}
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded shadow w-full max-w-sm text-center">
        <p class="text-gray-800 text-lg mb-4">Are you sure you want to delete this issue?</p>
        <div class="flex justify-center gap-4">
          <button type="button" on:click={() => confirmDeleteModal = false} class="text-gray-600 hover:underline">Cancel</button>
          <button type="button" on:click={deleteIssue} class="bg-red-600 text-white px-4 py-2 rounded shadow">Delete</button>
        </div>
      </div>
    </div>
  {/if}
</main>

<style lang="postcss">
  @reference "tailwindcss";
  :global(html) {
    background-color: theme('colors.gray.100');
  }
</style>
