<script lang="ts">
	import { createThread, fetchMessages, fetchThreads, threads } from '$lib/stores/threads';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	export let gptId: string;
	let threadTitle: string = '';
	let selectedThreadId: string = '';

	async function setThread(threadId: string) {
		if (!gptId) {
			return;
		}

		selectedThreadId = threadId;

		// add url parameter threadId
		goto(`/chat/${gptId}?threadId=${threadId}`);
		await fetchMessages(gptId, threadId);
	}

	async function handleCreateThread() {
		if (!gptId) {
			return;
		}

		selectedThreadId = await createThread(gptId, threadTitle);

		goto(`/chat/${gptId}?threadId=${selectedThreadId}`);
	}

	let gptThreads = $threads.filter((thread) => thread.metadata.gpt_id === gptId).reverse();

	$: {
		if ($threads) {
			gptThreads = $threads.filter((thread) => thread.metadata.gpt_id === gptId).reverse();
		}
	}

	onMount(async () => {
		await fetchThreads(); // TODO: inefficient
	});
</script>

<div class="threads">
	{#if gptId}
		<input bind:value={threadTitle} type="text" placeholder="Thread Title" />
		<button class="create-thread" on:click={handleCreateThread}>Create Thread</button>
	{/if}
	<div class="thread-selectors">
		{#each gptThreads as thread}
			<button
				class="thread-selector"
				class:selected={thread.id === selectedThreadId}
				on:click={() => setThread(thread.id)}>{thread.metadata.title}</button
			>
		{/each}
	</div>
</div>

<style>
	.threads {
		box-sizing: border-box;
		width: 12rem;
		height: calc(100vh - 3.58rem);
		background-color: #222;
		padding: 1rem;
	}

	.create-thread {
		background-color: black;
		color: white;
		width: 100%;
	}

	.thread-selectors {
		margin-top: 0.5rem;
	}

	.thread-selector {
		margin-top: 0.5rem;
		background-color: black;
		color: white;
		width: 100%;
	}

	.selected {
		background-color: #444;
	}
</style>
