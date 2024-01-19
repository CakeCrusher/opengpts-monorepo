<script lang="ts">
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import { fetchApi } from '$lib/fetcher';
	import type { Gpt } from '../../home/types';
	import { galleryGpts } from '../../home/stores';
	import { threads } from '$lib/stores/threads';

	export let data: PageData;
	const gpt: Gpt | undefined = $galleryGpts.find((gpt) => gpt.id === data.props.id);
	let inputMessage: string = '';

	function sendMessage() {
		fetchApi(`gpt/${data.props.id}/thread`, 'POST').then((res) => {
			threads.update((threads) => [...threads, res]);

			fetchApi(`gpt/${data.props.id}/thread/${res.id}/messages`, 'POST', {
				content: inputMessage
			}).then((res) => {
				console.log(res);
			});
		});
	}

	onMount(() => {
		if (!gpt) {
			fetchApi(`gpt`, 'GET').then((res) => {
				galleryGpts.update((gpts) => [...gpts, res]);
			});
		}
	});
</script>

<main>
	<h1>Chat</h1>
</main>
<form class="message-box" on:submit={sendMessage}>
	<input type="text" placeholder="Message Assistant..." bind:value={inputMessage} />
</form>

<style>
	main {
		max-width: 800px;
		margin: 0 auto;
		padding: 2rem;
	}

	.message-box {
		left: 50%;
		transform: translateX(-50%);
		position: fixed;
		bottom: 1rem;
		width: 100%;
		max-width: 800px;
	}
</style>
