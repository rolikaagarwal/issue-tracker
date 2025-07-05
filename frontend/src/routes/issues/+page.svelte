<script>
  import { isAuthenticated, token } from "$lib/stores/auth";
  import { onMount } from "svelte";
  import { get } from "svelte/store";
  import Navbar from "$lib/components/Navbar.svelte";

  const BASE_URL = import.meta.env.VITE_API_URL;

  let issues = [];
  let showModal = false;
  let confirmDeleteModal = false;
  let editingIssueId = null;
  let issueToDelete = null;

  let newIssue = {
    title: "",
    description: "",
    severity: "LOW",
    status: "OPEN",
    role: "",
    file: null,
    attachment: null,
  };

  function openModal(issue = null) {
    editingIssueId = issue?.id || null;
    newIssue = {
      title: issue?.title || "",
      description: issue?.description || "",
      severity: issue?.severity || "LOW",
      status: issue?.status || "OPEN",
      role: issue?.role || "",
      file: null,
      attachment: issue?.attachment || null,
    };
    showModal = true;
  }

  function handleFile(e) {
    newIssue.file = e.target.files[0];
  }

  async function fetchIssues() {
    try {
      const res = await fetch(`${BASE_URL}/issues/getall`, {
        headers: { Authorization: `Bearer ${get(token)}` },
      });
      if (res.ok) {
        issues = await res.json();
      } else {
        console.error("Failed to fetch issues");
      }
    } catch (err) {
      console.error("Error:", err);
    }
  }

  async function submitIssue() {
    const isEditing = Boolean(editingIssueId);
    let res;

    if (isEditing) {
      res = await fetch(`${BASE_URL}/issues/${editingIssueId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${get(token)}`,
        },
        body: JSON.stringify({
          title: newIssue.title,
          description: newIssue.description,
          severity: newIssue.severity,
          status: newIssue.status,
        }),
      });
    } else {
      const form = new FormData();
      form.append("title", newIssue.title);
      form.append("description", newIssue.description);
      form.append("severity", newIssue.severity);
      if (newIssue.file) form.append("file", newIssue.file);

      res = await fetch(`${BASE_URL}/issues/create`, {
        method: "POST",
        headers: { Authorization: `Bearer ${get(token)}` },
        body: form,
      });
    }

    if (res.ok) {
      showModal = false;
      await fetchIssues();
    } else {
      const err = await res.json().catch(() => ({}));
      alert(err.detail || "Failed to save issue");
    }
  }

  async function deleteIssue() {
    try {
      const res = await fetch(`${BASE_URL}/issues/${issueToDelete}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${get(token)}` },
      });

      if (res.ok) {
        confirmDeleteModal = false;
        await fetchIssues();
      } else {
        const err = await res.json().catch(() => ({}));
        alert(err.detail || "Failed to delete issue");
      }
    } catch (err) {
      console.error("Issue delete failed:", err);
      alert("Error deleting issue");
    }
  }

  onMount(() => {
    if (get(isAuthenticated)) fetchIssues();
  });
</script>

<Navbar />

<main class="bg-gray-50 min-h-screen px-6 py-10 border-t border-gray-200">
  <!-- Header + Create button -->
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-3xl font-bold text-gray-800">Your Issues</h1>
    <button
      on:click={() => openModal()}
      class="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded-lg shadow"
    >+ Create Issue</button>
  </div>

  <!-- Issues List -->
  {#if issues.length}
    <ul class="space-y-4">
      {#each issues as issue}
        <li class="flex items-center justify-between p-6 bg-white rounded-xl shadow hover:shadow-lg transition-shadow">
          <!-- Left: Title & Description -->
          <div class="flex-1">
            <p class="text-lg font-semibold text-gray-900">{issue.title}</p>
            <p class="mt-1 text-sm text-gray-600">{issue.description}</p>
          </div>

          <!-- Right: Actions + Badges -->
          <div class="flex flex-col items-center">
            <!-- Action Icons -->
            <div class="flex space-x-4 text-xl">
              <button
                on:click={() => openModal(issue)}
                title="Edit"
                class="text-blue-500 hover:text-blue-700 transition-colors"
              >📝</button>
              <button
                on:click={() => { confirmDeleteModal = true; issueToDelete = issue.id }}
                title="Delete"
                class="text-red-500 hover:text-red-700 transition-colors"
              >🗑️</button>
            </div>
            <!-- Badges below icons -->
            <div class="flex space-x-2 mt-2">
              <span
                class="px-3 py-1 text-xs font-medium rounded-full"
                class:bg-green-100={issue.severity === 'LOW'}
                class:text-green-800={issue.severity === 'LOW'}
                class:bg-yellow-100={issue.severity === 'MEDIUM'}
                class:text-yellow-800={issue.severity === 'MEDIUM'}
                class:bg-red-100={issue.severity === 'HIGH'}
                class:text-red-800={issue.severity === 'HIGH'}
              >
                {issue.severity}
              </span>
              <span
                class="px-3 py-1 text-xs font-medium rounded-full"
                class:bg-blue-100={issue.status === 'OPEN'}
                class:text-blue-800={issue.status === 'OPEN'}
                class:bg-orange-100={issue.status === 'IN_PROGRESS'}
                class:text-orange-800={issue.status === 'IN_PROGRESS'}
                class:bg-green-100={issue.status === 'RESOLVED'}
                class:text-green-800={issue.status === 'RESOLVED'}
                class:bg-gray-100={issue.status === 'CLOSED'}
                class:text-gray-800={issue.status === 'CLOSED'}
              >
                {issue.status.replace('_', ' ')}
              </span>
            </div>
          </div>
        </li>
      {/each}
    </ul>
  {:else}
    <p class="text-gray-600 italic">No issues found.</p>
  {/if}

  <!-- Create/Edit Modal -->
  {#if showModal}
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded shadow w-full max-w-md max-h-[90vh] overflow-auto p-6">
        <h2 class="text-xl font-bold mb-4">{editingIssueId ? "Edit" : "Create"} Issue</h2>
        <input type="text" bind:value={newIssue.title} placeholder="Title" class="w-full p-2 border rounded mb-2" />
        <textarea bind:value={newIssue.description} placeholder="Description" class="w-full p-2 border rounded mb-2"></textarea>
        <select bind:value={newIssue.severity} class="w-full p-2 border rounded mb-2">
          <option value="LOW">Low</option>
          <option value="MEDIUM">Medium</option>
          <option value="HIGH">High</option>
        </select>
        {#if newIssue.role === "MAINTAINER" || newIssue.role === "ADMIN"}
          <select bind:value={newIssue.status} class="w-full p-2 border rounded mb-4">
            <option value="OPEN">Open</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="RESOLVED">Resolved</option>
            <option value="CLOSED">Closed</option>
          </select>
        {:else}
          <!-- <p class="mb-4"><span class="font-medium">Status:</span> {newIssue.status}</p> -->
        {/if}
        {#if newIssue.attachment}
          <div class="mb-4">
            <p class="text-sm text-gray-700">Attached: {newIssue.attachment.filename}</p>
            {#if newIssue.attachment.filename.toLowerCase().endsWith(".pdf")}
              <div class="h-64 overflow-auto border rounded mb-2">
                <iframe src={`${BASE_URL}${newIssue.attachment.url}`} class="w-full h-full" title="PDF Preview"></iframe>
              </div>
            {:else}
              <img src={`${BASE_URL}${newIssue.attachment.url}`} alt={newIssue.attachment.filename} class="w-full max-h-64 object-contain border rounded mb-2" />
            {/if}
            <a href={`${BASE_URL}${newIssue.attachment.url}`} target="_blank" download={newIssue.attachment.filename} class="text-blue-500 underline text-sm">Download</a>
          </div>
        {/if}
        <input type="file" on:change={handleFile} class="w-full mb-4" />
        <div class="flex justify-end space-x-2">
          <button on:click={() => (showModal = false)} class="text-gray-600 hover:underline">Cancel</button>
          <button on:click={submitIssue} class="bg-green-600 text-white px-4 py-2 rounded shadow">Save</button>
        </div>
      </div>
    </div>
  {/if}

  <!-- Delete Confirmation Modal -->
  {#if confirmDeleteModal}
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded shadow w-full max-w-md max-h-[90vh] overflow-auto p-6">
        <p class="text-gray-800 text-lg mb-4">Are you sure you want to delete this issue?</p>
        <div class="flex justify-center gap-4">
          <button on:click={() => (confirmDeleteModal = false)} class="text-gray-600 hover:underline">Cancel</button>
          <button on:click={deleteIssue} class="bg-red-600 text-white px-4 py-2 rounded shadow">Delete</button>
        </div>
      </div>
    </div>
  {/if}
</main>

<style lang="postcss">
  @reference "tailwindcss";
  :global(html) { background-color: theme("colors.gray.100"); }
</style>
