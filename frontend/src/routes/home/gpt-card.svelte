<script lang="ts">
	import type { Gpt } from './types';

	export let gpt: Gpt;
</script>

<a class="card" href={`/chat/${gpt.id}`}>
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

	.card-image {
		border-radius: 0.5rem;
	}

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
