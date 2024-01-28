<script>
	import Navbar from '$lib/components/navbar.svelte';
	import { onMount } from 'svelte';
	import './global.css';
	import { fetchApi } from '$lib/fetcher';
	import { goto } from '$app/navigation';
	import { user } from '$lib/stores/user';
	import { fetchUserGpts } from '$lib/stores/gpts';



	
	onMount(async () => {
		let token = localStorage.getItem('token');

		const urlParams = new URLSearchParams(window.location.search);
		const urlToken = urlParams.get('token');

		if (urlToken) {
			token = urlToken;
			urlParams.delete('token');
			window.history.replaceState({}, '', `${window.location.pathname}?${urlParams}`);
		}
		if (token) {
			localStorage.setItem('token', token);
			const response = await fetchApi('login', 'GET');

			if (response.email) {
				// Store the access token and user details
				user.set(response);

				// run dependent state updates
				fetchUserGpts();

				// Redirect the user to the home page
				goto('/');
			} else {
				localStorage.removeItem('token');
				// Handle error
				console.error('Failed to authenticate user');
			}
		}
	});
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
	<link
		href="https://fonts.googleapis.com/css2?family=Mulish:ital,wght@0,200..1000;1,200..1000&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<Navbar />
<slot />
