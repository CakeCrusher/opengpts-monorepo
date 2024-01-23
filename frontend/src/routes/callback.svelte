<script lang="ts">
	import { onMount } from 'svelte';
	import { fetchApi } from '$lib/fetcher';
	import { user } from '$lib/stores/user';
	import { goto } from '$app/navigation';

	onMount(async () => {
		// Extract the code from the URL query parameters
		const urlParams = new URLSearchParams(window.location.search);
		const code = urlParams.get('code');

		if (code) {
			// Send the code to the backend
			const response = await fetchApi('auth/google', 'GET', { code });

			if (response.access_token) {
				// Store the access token and user details
				localStorage.setItem('token', response.access_token);
				user.set(response.user);

				// Redirect the user to the home page
				goto('/');
			} else {
				// Handle error
				console.error('Failed to authenticate user');
			}
		} else {
			// Handle error
			console.error('No code in URL query parameters');
		}
	});
</script>