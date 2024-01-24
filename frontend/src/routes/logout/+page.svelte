<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { user } from '$lib/stores/user';

	onMount(async () => {
		localStorage.removeItem('token');
		user.set(null);
		goto('/');
	});
</script>
