<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { user } from '$lib/stores/user';
	import { gpts } from '$lib/stores/gpts';

	onMount(async () => {
		localStorage.removeItem('token');
		user.set(null);
		gpts.update((gpts) => ({ ...gpts, user: [] }));
		goto('/');
	});
</script>
