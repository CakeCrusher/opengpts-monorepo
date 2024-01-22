<script lang="ts">
	import { createThread, fetchMessages, fetchThreads, threads } from '$lib/stores/threads';
	import { onMount } from 'svelte';
	import { selectedThreadId } from './stores';

	export let gptId: string | undefined;
	let threadTitle: string = '';

	async function setThread(threadId: string) {
		if (!gptId) {
			return;
		}

		$selectedThreadId = threadId;
		await fetchMessages(gptId, threadId);
	}

	onMount(async () => {
		if ($threads.length === 0) {
			await fetchThreads();
		}
	});
</script>

<div class="threads">
	{#if gptId}
		<input bind:value={threadTitle} type="text" placeholder="Thread Title" />
		<button class="create-thread" on:click={async () => await createThread(gptId, threadTitle)}
			>Create Thread</button
		>
	{/if}
	<div class="thread-selectors">
		{#each $threads as thread}
			<button
				class="thread-selector"
				class:selected={thread.id === $selectedThreadId}
				on:click={async () => setThread(thread.id)}>{thread.metadata.title}</button
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
