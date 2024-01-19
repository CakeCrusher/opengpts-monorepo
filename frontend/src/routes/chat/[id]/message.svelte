<script lang="ts">
	import type { ThreadMessage } from '$lib/stores/threads';

	export let message: ThreadMessage;
</script>

{#if message}
	<div class="header">You</div>
	{#each message.content as item}
		{#if item.type === 'text'}
			{item.text.value}
		{/if}
	{/each}
{/if}

<style>
	.header {
		font-weight: bold;
	}
</style>
