<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(async () => {
		localStorage.removeItem('token');
		goto('/');
	});
</script>
