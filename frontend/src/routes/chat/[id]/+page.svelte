<script lang="ts">
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import { fetchPublicGpts, fetchUserGpts, allGpts } from '$lib/stores/gpts';
	import Threads from './threads.svelte';
	import { page } from '$app/stores';
	import Chat from './chat.svelte';

	export let data: PageData;
	let threadId = $page.url.searchParams.get('threadId');
	const gptId = data.props.id;
	let gpt = $allGpts.find((gpt) => gpt.id === gptId);

	$: if ($page.url.searchParams.get('threadId')) {
		threadId = $page.url.searchParams.get('threadId');
	}

	onMount(async () => {
		if (!gpt) {
			await fetchPublicGpts();
			await fetchUserGpts();
			gpt = $allGpts.find((gpt) => gpt.id === gptId);
		}
	});
</script>

<div class="content">
	<Threads {gptId} />
	<main>
		{#if gptId && threadId}
			<!-- <h1>Chatting with {gpt?.name}</h1> -->
			<Chat {gptId} {threadId} preMessage={() => {}} />
		{:else}
			<h1>Select a GPT and a thread to chat</h1>
		{/if}
	</main>
</div>

<style>
	.content {
		display: flex;
		flex-direction: row;
	}

	main {
		box-sizing: border-box;
		padding: 2rem;
		width: 100%;
	}
</style>
