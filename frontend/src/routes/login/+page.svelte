// TODO: PUBLIC_BUSINESS_LAYER_URL should not be hard coded. Should be pulled from envirnment variables.
<script lang="ts">
	import { onMount } from 'svelte';
	import { PUBLIC_BUSINESS_LAYER_URL } from '../../lib/fetcher';

	onMount(async () => {
		window.location.href = `${PUBLIC_BUSINESS_LAYER_URL}/login/google`;
	});
</script>
