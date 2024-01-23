<script lang="ts">
	import { goto } from '$app/navigation';
	import { fetchApi } from '$lib/fetcher';
	import { user } from '$lib/stores/user';

	async function submit(e: Event) {
		e.preventDefault();
		try {
			const response = await fetchApi('login/google', 'GET');
			if (response.url) {
				window.location.href = response.url;
			} else {
				// Handle error: No URL in response
				console.error('No URL in response from backend');
			}
		} catch (error) {
			// Handle error: Failed to make request to backend
			console.error('Failed to make request to backend', error);
		}
	}
</script>

<div class="page">
	<h1>Register or Log In</h1>
	<form on:submit|preventDefault={(e) => submit(e)}>
		<label class="label--block" for="email">Email</label>
		<input type="text" name="email" id="email" placeholder="Email" />
		<input class="submit" type="submit" value="Submit" />
	</form>
</div>

<style>
	.page {
		max-width: 400px;
		margin: 0 auto;
	}

	.submit {
		margin-top: 1rem;
	}
</style>
