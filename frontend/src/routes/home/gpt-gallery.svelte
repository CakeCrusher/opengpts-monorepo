<script>
	import { onMount, afterUpdate } from 'svelte';
	import { gpts, fetchPublicGpts, fetchUserGpts } from '$lib/stores/gpts';
	import { user } from '$lib/stores/user';
	import GptCard from './gpt-card.svelte';

	onMount(() => {
		fetchPublicGpts();
		if ($user) {
			fetchUserGpts();
		}
	});
</script>

<div class="container">
	<h3>My GPTs</h3>
	{#if $user}
		<div class="gallery">
			{#each $gpts.user as gpt}
				<GptCard {gpt} />
			{/each}
		</div>
	{:else}
		<p>Log in to see your GPTs</p>
	{/if}
	<hr>
	<h3>Public GPTs</h3>
	<div class="gallery">
		{#each $gpts.public as gpt}
			<GptCard {gpt} />
		{/each}
	</div>
</div>

<style>
	.container {
		padding: 1rem;
	}
	.gallery {
		display: grid;
		grid-template-columns: repeat(2, minmax(300px, 1fr));
		gap: 1rem;
	}
</style>
