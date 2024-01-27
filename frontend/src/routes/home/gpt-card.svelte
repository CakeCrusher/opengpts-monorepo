<script lang="ts">
	import { gptEditing } from '$lib/stores/gptEditing';
	import { user } from '$lib/stores/user';
	import type { Gpt, GptStaging } from '../../types/gpt';

	export let gpt: Gpt;
	const gptIsStaging = gpt.metadata.is_staging;
	const setGptEditing = () => {
		if (gpt.metadata.is_staging) {
			gptEditing.set(gpt as GptStaging);
		}
	};

	let hrefTo: string;
	let onClick: () => void;

	if (gptIsStaging) {
		hrefTo = `/create`;
		onClick = setGptEditing;
	} else {
		hrefTo = `/chat/${gpt.id}`;
		onClick = () => {};
	}

	if (user) {
		hrefTo = `/`;
		onClick = () => {
			alert('You must be logged in to chat with a GPT.');
		};
	}
</script>

<a class="card" href={hrefTo} on:click={onClick}>
	<!-- <img class="card-image" src={gpt.imageUrl} alt="" /> -->
	<div class="card-content">
		<h3 class="name">{gpt.name}</h3>
		<p class="description">{gpt.description}</p>
		<p class="author">{gpt.metadata.user_name}</p>
	</div>
</a>

<style>
	.card {
		display: flex;
		gap: 1rem;
		border-radius: 0.5rem;
		padding: 1rem;
		box-shadow:
			0 0 0 1px rgba(0, 0, 0, 0.1),
			0 2px 4px rgba(0, 0, 0, 0.1);
		text-decoration: none;
		color: inherit;
	}

	.card:hover {
		box-shadow:
			0 0 0 1px rgba(0, 0, 0, 0.1),
			0 4px 8px rgba(0, 0, 0, 0.1);
		margin-top: -0.5rem;
	}

	/* .card-image {
		border-radius: 0.5rem;
	} */

	.name {
		margin-top: 0;
	}

	.description {
		margin-bottom: 0;
	}

	.author {
		color: #666;
	}
</style>
