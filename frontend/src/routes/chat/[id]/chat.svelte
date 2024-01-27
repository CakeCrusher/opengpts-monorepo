<script lang="ts">
	import { allGpts, gpts } from '$lib/stores/gpts';
	import { createThreadMessage } from '$lib/stores/threads';
	import Messages from './messages.svelte';
	import type { Gpt } from '../../../types/gpt';

	export let gptId: string;
	export let threadId: string;
	export let preMessage: () => void;
	// get the gpt_id that was passed as a parameter

	$: {
		if ($allGpts) {
			console.log('allGpts', $allGpts);
		}
	}

	let gpt: Gpt | undefined = $allGpts.find((gpt) => gpt.id === gptId);
	let inputMessage: string = '';

	console.log("gpt", gpt, "threadId", threadId)

	async function sendMessage() {
		await preMessage();
		if (!gpt) {
			alert('Must be using a valid gpt.');
			return;
		}

		if (!threadId) {
			alert('Select a thread first!');
			return;
		}
		await createThreadMessage(gptId, threadId, inputMessage);
	}
</script>

<Messages {threadId} />
<form class="message-box" on:submit={sendMessage}>
	<input
		class="message-input"
		disabled={!(gpt && threadId)}
		type="text"
		placeholder="Message Assistant..."
		bind:value={inputMessage}
	/>
</form>

<style>
	.message-box {
		width: 100%;
		margin: 0;
	}
	.message-input {
		margin: 0;
	}
</style>
