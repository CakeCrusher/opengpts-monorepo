<script>
	import { onMount } from 'svelte';
	import { gpts, fetchGpts } from '$lib/stores/gpts';
	import GptCard from './gpt-card.svelte';

	onMount(() => {
		fetchGpts();
	});
</script>

<div class="gallery">
	{#each $gpts as gpt}
		<GptCard {gpt} />
	{/each}
</div>

<style>
	.gallery {
		display: grid;
		grid-template-columns: repeat(2, minmax(300px, 1fr));
		gap: 1rem;
	}
</style>
