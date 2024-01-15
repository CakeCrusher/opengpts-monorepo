<script lang="ts">
	import { goto } from '$app/navigation';
	import { fetchApi } from '$lib/fetcher';
	import { user } from '$lib/stores/user';

	function submit(e: Event) {
		const email = e.target?.email.value;
		fetchApi('users', 'POST', { email }).then((response) => {
			user.set(response);
			goto('/');
		});
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
