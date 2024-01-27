<script lang="ts">
	import { onMount } from 'svelte';
	import { gpts, fetchPublicGpts, fetchUserGpts } from '$lib/stores/gpts';
	import { user } from '$lib/stores/user';
	import GptCard from './gpt-card.svelte';
	import type { Gpt, GptStaging } from '../../types/gpt';
	import { gptSearchQuery } from '$lib/stores/gptSearchQuery';

	const queryFilter = (gpts: Gpt[]) => {
		return gpts.filter((gpt) => {
			if (
				gpt.name.toLowerCase().includes($gptSearchQuery.toLowerCase()) ||
				gpt.description?.toLowerCase().includes($gptSearchQuery.toLowerCase())
			) {
				return true;
			}
			return false;
		});
	};

	let userGptsToShow = $gpts.user;
	let publicGptsToShow = $gpts.public;

	$: {
		if ($gptSearchQuery) {
			const newUserGptsToShow = queryFilter($gpts.user);
			userGptsToShow = newUserGptsToShow as GptStaging[];
			publicGptsToShow = queryFilter($gpts.public);
		}
	}

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
			{#each userGptsToShow as gpt}
				<GptCard {gpt} />
			{/each}
		</div>
	{:else}
		<p>Log in to see your GPTs</p>
	{/if}
	<hr />
	<h3>Public GPTs</h3>
	<div class="gallery">
		{#each publicGptsToShow as gpt}
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
