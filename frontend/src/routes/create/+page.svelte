<h1>Create a GPT</h1>
<form action="">
	<div>
		<label class="label--block" for="email">Your Email</label>
		<input id="email" type="email" placeholder="Email" />
	</div>
	<h2>GPT Details</h2>
	<div class="input--mb">
		<label class="label--block" for="name">Name</label>
		<input id="name" type="text" placeholder="Name" />
	</div>
	<div class="input--mb">
		<label class="label--block" for="description">Description</label>
		<textarea id="description" cols="30" rows="10" placeholder="Description"></textarea>
	</div>
	<div class="input--mb">
		<label class="label--block" for="instructions">Instructions</label>
		<textarea id="instructions" cols="30" rows="10" placeholder="Instructions"></textarea>
	</div>
	<div>
		<label class="label--block" for="model">Model</label>
		<select id="model">
			<option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
		</select>
	</div>
	<div>
		<h3>Tools</h3>
		<div>
			<input id="code-interpreter" type="checkbox" />
			<label for="code-interpreter">Code Interpreter</label>
		</div>
		<div class="input--mb">
			<input id="retrieval" type="checkbox" />
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
	<div>
		<h3>Visibility</h3>
		<label for="visibility">Visibility</label>
		<select id="visibility">
			<option value="public">Public</option>
			<option value="private">Private</option>
		</select>
	</div>
</form>

<style>
	h2 {
		margin-bottom: 1rem;
	}

	h3 {
		margin-bottom: 0.5rem;
	}
</style>
