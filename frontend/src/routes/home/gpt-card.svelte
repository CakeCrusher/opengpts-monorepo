<script lang="ts">
	import type { Gpt } from './types';

	export let gpt: Gpt;
</script>

<div class="card">
	<!-- <img class="card-image" src={gpt.imageUrl} alt="" /> -->
	<div class="card-content">
		<h3 class="name">{gpt.name}</h3>
		<p class="description">{gpt.description}</p>
		<p class="author">{gpt.metadata.user_name}</p>
	</div>
</div>

<style>
	.card {
		display: flex;
		gap: 1rem;
		border-radius: 0.5rem;
		padding: 1rem;
		box-shadow:
			0 0 0 1px rgba(0, 0, 0, 0.1),
			0 2px 4px rgba(0, 0, 0, 0.1);
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
