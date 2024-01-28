<script lang="ts">
	import { onMount } from 'svelte';
	import { PUBLIC_GPT_TO_ASSISTANT_API } from '$env/static/public';

	onMount(async () => {
		window.location.href = `${PUBLIC_GPT_TO_ASSISTANT_API}/login/google`;
	});
</script>
