<h1>Create a GPT</h1>
<form action="">
	<div>
		<label for="email">Your Email</label>
		<input id="email" type="text" placeholder="Email" />
	</div>
	<h2>GPT Details</h2>
	<div>
		<label for="name">Name</label>
		<input id="name" type="text" placeholder="Name" />
	</div>
	<div>
		<label for="description">Description</label>
		<input id="description" type="text" placeholder="Description" />
	</div>
	<div>
		<label for="instructions">Instructions</label>
		<input id="instructions" type="text" placeholder="Instructions" />
	</div>
	<div>
		<label for="model">Model</label>
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
		<div>
			<label for="retrieval">Web Browsing</label>
			<input id="retrieval" type="checkbox" />
		</div>
		<div>
			<label for="function-calling">Function Calling</label>
			<button>New Function</button>
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
