<script lang="ts">
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import { gpts } from '$lib/stores/gpts';
	import { createThreadMessage } from '$lib/stores/threads';
	import { fetchPublicGpts } from '$lib/stores/gpts';
	import Threads from './threads.svelte';
	import Messages from './messages.svelte';
	import { selectedThreadId } from './stores';
	import { page } from '$app/stores';
	import type { Gpt } from '../../../types/gpt';

	export let data: PageData;
	const threadId = $page.url.searchParams.get('threadId');
	let gpt: Gpt | undefined = $gpts.public.find((gpt) => gpt.id === data.props.id);
	let inputMessage: string = '';

	async function sendMessage() {
		if (!gpt) {
			return;
		}

		if (!$selectedThreadId) {
			alert('Select a thread first!');
			return;
		}
		await createThreadMessage(data.props.id, $selectedThreadId, inputMessage);
	}

	onMount(async () => {
		if (!gpt) {
			const fetchedGpts = await fetchPublicGpts();
			gpt = fetchedGpts.find((gpt) => gpt.id === data.props.id);
		}
		if (threadId) {
			$selectedThreadId = threadId;
		}
	});
</script>

<div class="content">
	<Threads gptId={gpt?.id} />
	<main>
		<Messages />
		<form class="message-box" on:submit={sendMessage}>
			<input type="text" placeholder="Message Assistant..." bind:value={inputMessage} />
		</form>
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

	.message-box {
		width: 100%;
	}
</style>
