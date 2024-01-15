<script lang="ts">
	import { fetchApi } from '$lib/fetcher';
	import { user } from '$lib/stores/user';
	import { onDestroy } from 'svelte';

	let email: string | undefined;
	let name: string;
	let description: string;
	let instructions: string;
	let model: string;
	let usesCodeInterpreter: boolean;
	let usesWebBrowsing: boolean;
	let visibility: string;

	const unsubscribe = user.subscribe((value) => (email = value?.email));

	onDestroy(unsubscribe);

	function submit() {
		fetchApi('gpt', 'POST', {
			name,
			description,
			instructions,
			model,
			usesCodeInterpreter,
			usesWebBrowsing,
			visibility,
			email
		});
	}
</script>

<h1>Create a GPT</h1>
<form on:submit={submit}>
	<h2>GPT Details</h2>
	<div class="input--mb">
		<label class="label--block" for="name">Name</label>
		<input id="name" type="text" placeholder="Name" bind:value={name} />
	</div>
	<div class="input--mb">
		<label class="label--block" for="description">Description</label>
		<textarea
			id="description"
			cols="30"
			rows="10"
			placeholder="Description"
			bind:value={description}
		></textarea>
	</div>
	<div class="input--mb">
		<label class="label--block" for="instructions">Instructions</label>
		<textarea
			id="instructions"
			cols="30"
			rows="10"
			placeholder="Instructions"
			bind:value={instructions}
		></textarea>
	</div>
	<div>
		<label class="label--block" for="model">Model</label>
		<select id="model" bind:value={model}>
			<option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
		</select>
	</div>
	<div>
		<h3>Tools</h3>
		<div>
			<input id="code-interpreter" type="checkbox" bind:checked={usesCodeInterpreter} />
			<label for="code-interpreter">Code Interpreter</label>
		</div>
		<div class="input--mb">
			<input id="retrieval" type="checkbox" bind:checked={usesWebBrowsing} />
			<label for="retrieval">Web Browsing</label>
		</div>
		<div>
			<label class="label--block" for="function-calling">Actions</label>
			<button>New Action</button>
		</div>
	</div>
	<div>
		<h3>Knowledge</h3>
		<div>
			<label for="files">Upload files:</label>
			<input id="files" type="file" multiple />
		</div>
	</div>
	<div class="input--mb">
		<h3>Visibility</h3>
		<label for="visibility">Visibility</label>
		<select id="visibility" bind:value={visibility}>
			<option value="public">Public</option>
			<option value="private">Private</option>
		</select>
	</div>
	<input type="submit" value="Create" />
</form>

<style>
	h2 {
		margin-bottom: 1rem;
	}

	h3 {
		margin-bottom: 0.5rem;
	}
</style>
