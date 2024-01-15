<script lang="ts">
	import { user } from '$lib/stores/user';
	import { onDestroy } from 'svelte';

	let isLoggedIn = false;

	const unsubscribe = user.subscribe((value) => (isLoggedIn = value !== null));

	onDestroy(unsubscribe);
</script>

<div class="links">
	<div class="left">
		<a class="link" href="/">Home</a>
	</div>
	<div class="right">
		{#if isLoggedIn}
			<a class="link" href="/create">New GPT</a>
		{:else}
			<a class="link" href="/login">Register/Login</a>
		{/if}
	</div>
</div>

<style>
	.links {
		display: flex;
		justify-content: space-between;
	}

	.link {
		display: inline-block;
		text-align: center;
		font-size: 1.25rem;
		color: #000;
		text-decoration: none;
		padding: 0.5rem 1rem;
		border-radius: 0.5rem;
	}

	.link:hover {
		background-color: #ddd;
	}
</style>
