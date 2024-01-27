<script>
	import { gptSearchQuery } from '$lib/stores/gptSearchQuery';
</script>

<div class="search-bar-container">
	<i class="search-icon ph ph-magnifying-glass"></i>
	<input type="text" class="search-bar" placeholder="Search GPTs" bind:value={$gptSearchQuery} />
</div>

<style>
	.search-bar-container {
		display: flex;
		align-items: center;
	}

	.search-icon {
		position: absolute;
		padding-left: 0.75rem;
	}

	.search-bar {
		box-sizing: border-box;
		width: 100%;
		padding: 0.75rem;
		padding-left: 2.25rem;
		border-radius: 0.5rem;
		border: 1px solid #ccc;
		font-size: 1rem;
	}
</style>
