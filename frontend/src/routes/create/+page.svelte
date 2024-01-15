<h1>Create a GPT</h1>
<form action="">
	<div>
		<label class="label--block" for="email">Your Email</label>
		<input id="email" type="text" placeholder="Email" />
	</div>
	<h2>GPT Details</h2>
	<div class="input--mb">
		<label class="label--block" for="name">Name</label>
		<input id="name" type="text" placeholder="Name" />
	</div>
	<div class="input--mb">
		<label class="label--block" for="description">Description</label>
		<textarea id="description" cols="30" rows="10"></textarea>
	</div>
	<div class="input--mb">
		<label class="label--block" for="instructions">Instructions</label>
		<textarea id="instructions" cols="30" rows="10"></textarea>
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
			<label for="code-interpreter">Code Interpreter</label>
			<input id="code-interpreter" type="checkbox" />
		</div>
		<div class="input--mb">
			<label for="retrieval">Web Browsing</label>
			<input id="retrieval" type="checkbox" />
		</div>
		<div>
			<label class="label--block" for="function-calling">Actions</label>
			<button>New Action</button>
		</div>
	</div>
	<div>
		<h3>Knowledge</h3>
		<div>
			<label for="files">Select files:</label>
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
	.label--block {
		display: block;
		padding-bottom: 0.5rem;
	}

	.input--mb {
		margin-bottom: 1rem;
	}

	input[type='text'],
	textarea {
		box-sizing: border-box;
		width: 100%;
		padding: 0.5rem;
		border-radius: 0.5rem;
		border: 1px solid #ccc;
		font-size: 1rem;
	}
</style>
