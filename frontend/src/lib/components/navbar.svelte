<script lang="ts">
	import { resetGptEditing } from '$lib/stores/gptEditing';
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
		{#if isLoggedIn && user !== null}
			<a class="link" href="/create" on:click={resetGptEditing}>New GPT</a>
			<a class="link" href="/logout">Log Out of {$user && $user.name}</a>
		{:else}
			<a class="link" href="/login">Register/Login</a>
		{/if}
	</div>
</div>

<style>
	.links {
		display: flex;
		justify-content: space-between;
		padding: 0.5rem;
		background-color: #b8f2d5;
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
