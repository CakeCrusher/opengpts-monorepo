<script lang="ts">
	import { onMount } from 'svelte';
	import { PUBLIC_BUSINESS_LAYER_URL } from '$env/static/public';

	onMount(async () => {
		window.location.href = `${PUBLIC_BUSINESS_LAYER_URL}/login/google`;
	});
</script>
