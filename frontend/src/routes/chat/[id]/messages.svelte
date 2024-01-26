<script lang="ts">
	import { threads } from '$lib/stores/threads';
	import Message from './message.svelte';
	export let threadId: string;
</script>

<div class="messages">
	{#each [...($threads.find((thread) => thread.id === threadId)?.threadMessages || [])].reverse() as message}
		<Message {message} />
	{/each}
</div>

<style>
	.messages {
		height: calc(100% - 1rem);
	}
</style>
