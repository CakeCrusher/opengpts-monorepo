<script>
	import { galleryGpts } from './stores';
	import GptCard from './gpt-card.svelte';
	import { onMount } from 'svelte';
	import { fetchApi } from '$lib/fetcher';

	onMount(() => {
		fetchApi('gpt', 'GET').then((res) => {
			galleryGpts.set(res);
		});
	});
</script>

<div class="gallery">
	{#each $galleryGpts as gpt}
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
