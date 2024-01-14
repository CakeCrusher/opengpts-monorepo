<script>
	import SearchBar from './search-bar.svelte';
	import GptGallery from './gpt-gallery.svelte';
</script>

<main class="main">
	<h1 class="gpts-header">GPTs</h1>
	<div class="search-bar">
		<SearchBar />
	</div>
	<GptGallery />
</main>

<style>
	.main {
		max-width: 1000px;
		margin: 0 auto;
	}

	.gpts-header {
		text-align: center;
		font-size: 2.5rem;
		margin-bottom: 0;
	}

	.search-bar {
		margin: 1rem 0;
	}
</style>
