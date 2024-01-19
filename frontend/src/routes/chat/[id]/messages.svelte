<script lang="ts">
	import { threads } from '$lib/stores/threads';
	import Message from './message.svelte';
	import { selectedThreadId } from './stores';
</script>

<div class="messages">
	{#each $threads.find((thread) => thread.id === $selectedThreadId)?.threadMessages || [] as message}
		<Message {message} />
	{/each}
</div>

<style>
	.messages {
		height: calc(100% - 1rem);
	}
</style>
