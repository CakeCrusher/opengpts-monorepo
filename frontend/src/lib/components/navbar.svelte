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
			<a class="link google-button" href="/login"><i class="ph ph-google-logo"></i>Sign In</a>
		{/if}
	</div>
</div>

<style>
	.links {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.5rem;
		height: 2rem;
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

	.google-button {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		background-color: white;
		padding: 0.25rem 0.75rem;
		padding-right: 0.85rem;
	}
</style>
