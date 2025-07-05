<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  import { token } from '$lib/stores/auth';
  import { get } from 'svelte/store';
  import Navbar from '$lib/components/Navbar.svelte';

  let canvas;
  let chart;

  async function fetchSeverityStats() {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/dashboard/issue_severity_counts`, {
      headers: { Authorization: `Bearer ${get(token)}` },
    });
    if (!res.ok) return;

    const data = await res.json();

    const labels = ['LOW', 'MEDIUM', 'HIGH'];
    const counts = labels.map(label => data[label] || 0);

    if (chart) chart.destroy(); 

    chart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Open Issues by Severity',
          data: counts,
          backgroundColor: ['#4ade80', '#facc15', '#f87171'], 
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          title: {
            display: true,
            text: 'Open Issues by Severity',
            font: { size: 18 }
          }
        }
      }
    });
  }

  onMount(fetchSeverityStats);
</script>
<Navbar />
<main class="p-6">
  <h2 class="text-xl font-bold mb-4 text-gray-700">Dashboard</h2>
  <canvas bind:this={canvas} class="max-w-2xl mx-auto" ></canvas>
</main>
