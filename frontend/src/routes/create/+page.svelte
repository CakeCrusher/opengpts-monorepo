<script lang="ts">
	import { user } from '$lib/stores/user';
	import { gptEditing, publishGpt, removeFile, saveGpt, uploadFile } from '$lib/stores/gptEditing';
	import { Model, ToolTypes, Visibility, type ToolAction } from '../../types/gpt';
	import Chat from '../chat/[id]/chat.svelte';
	import { createThread } from '$lib/stores/threads';

	// const unsubscribe = user.subscribe((value) => (user_name = value?.name));

	// onDestroy(unsubscribe);

	// function submit() {
	// 	let tools = [];

	// 	if (usesCodeInterpreter) {
	// 		tools.push({ type: 'code-interpreter' });
	// 	}
	// 	if (usesWebBrowsing) {
	// 		tools.push({ type: 'retrieval' });
	// 	}

	// }

	let selectedFiles: FileList | null = null;
	let fileUploadLoading: boolean = false;

	function clearInput() {
		const input = document.getElementById('files') as HTMLInputElement;
		if (input) {
			input.value = ''; // Clear the input
		}
	}

	const submitFile = async () => {
		if (!selectedFiles || selectedFiles.length === 0) return;
		const file = selectedFiles[0];

		fileUploadLoading = true;

		try {
			await uploadFile(file);
			clearInput();
		} catch (error) {
			console.error('File upload error: ', error);
		}

		fileUploadLoading = false;
	};

	function addNewAction() {
		gptEditing.update((current) => {
			const newAction: ToolAction = {
				type: ToolTypes.ACTION,
				data: ''
			};
			return {
				...current,
				tools: [...current.tools, newAction]
			};
		});
	}

	function removeTool(index: number) {
		gptEditing.update((current) => {
			let toolsCopy = [...current.tools];
			toolsCopy.splice(index, 1);
			return { ...current, tools: toolsCopy };
		});
	}

	let codeInterpreterEnabled: boolean = false;

	$: {
		if (codeInterpreterEnabled) {
			gptEditing.update((value) => ({
				...value,
				tools: [...value.tools, { type: ToolTypes.CODE_INTERPRETER }]
			}));
		} else {
			gptEditing.update((value) => ({
				...value,
				tools: value.tools.filter((tool) => tool.type !== ToolTypes.CODE_INTERPRETER)
			}));
		}
	}

	let retrievalEnabled: boolean = false;

	$: {
		if (retrievalEnabled) {
			gptEditing.update((value) => ({
				...value,
				tools: [...value.tools, { type: ToolTypes.RETRIEVAL }]
			}));
		} else {
			gptEditing.update((value) => ({
				...value,
				tools: value.tools.filter((tool) => tool.type !== ToolTypes.RETRIEVAL)
			}));
		}
	}

	$: {
		if ($gptEditing.file_ids.length > 0) {
			gptEditing.update((value) => ({
				...value,
				tools: [...value.tools, { type: ToolTypes.RETRIEVAL }]
			}));
		} else {
			gptEditing.update((value) => ({
				...value,
				tools: value.tools.filter((tool) => tool.type !== ToolTypes.RETRIEVAL)
			}));
		}
	}

	$: {
		if ($gptEditing) {
			console.log('$gptEditing', $gptEditing);
		}
	}

	let threadId: string = '';

	const modelValidation = () => {
		if ($gptEditing.model === Model.GPT_3_5_TURBO) {
			if ($gptEditing.file_ids.length > 0) {
				throw new Error('GPT-3.5 Turbo does not support knowledge files');
			}
		}
		return true;
	};

	const onSave = async () => {
		try {
			modelValidation();
		} catch (error: any) {
			alert(error.message);
			return;
		}

		console.log('$gptEditing', $gptEditing);

		await saveGpt();

		const threadTitle = 'gpt_testing-' + new Date().toLocaleString();
		threadId = await createThread($gptEditing.id, threadTitle);
	};

	let gptEditingTag = '';
	$: {
		if ($gptEditing.id) {
			gptEditingTag = ' for ' + $gptEditing.id.slice(0, 8) + '...';
		} else {
			gptEditingTag = '';
		}
	}

	$: {
		if ($gptEditing) {
			threadId = '';
		}
	}
</script>

{#if $user}
	<div class="wrapper">
		<div class="content">
			<form class="gpt_fields">
				<h2>GPT Details {gptEditingTag}</h2>
				<div class="input--mb">
					<label class="label--block" for="name">Name</label>
					<input id="name" type="text" placeholder="Name" bind:value={$gptEditing.name} />
				</div>
				<div class="input--mb">
					<label class="label--block" for="description">Description</label>
					<textarea
						id="description"
						cols="30"
						rows="10"
						placeholder="Description"
						bind:value={$gptEditing.description}
					></textarea>
				</div>
				<div class="input--mb">
					<label class="label--block" for="instructions">Instructions</label>
					<textarea
						id="instructions"
						cols="30"
						rows="10"
						placeholder="Instructions"
						bind:value={$gptEditing.instructions}
					></textarea>
				</div>
				<div>
					<label class="label--block" for="model">Model</label>
					<select id="model" bind:value={$gptEditing.model}>
						<option value="gpt-3.5-turbo">{Model.GPT_3_5_TURBO}</option>
						<option value="gpt-4-turbo-preview">{Model.GPT_4_TURBO_PREVIEW}</option>
					</select>
				</div>
				<div>
					<h3>Tools</h3>
					<div>
						<input id="code-interpreter" type="checkbox" bind:checked={codeInterpreterEnabled} />
						<label for="code-interpreter">Code Interpreter</label>
					</div>

					<!-- <div class="input--mb">
				<input id="retrieval" type="checkbox" bind:checked={usesWebBrowsing} />
				<label for="retrieval">Web Browsing</label>
			</div> -->
					<div>
						<label class="label--block" for="function-calling">Actions</label>
						{#each $gptEditing.tools as tool, index}
							{#if tool.type === ToolTypes.ACTION}
								<textarea rows="3" bind:value={tool.data} placeholder="Enter action data here..."
								></textarea>
								<button type="button" on:click={() => removeTool(index)}>Remove</button>
							{/if}
						{/each}
						<button type="button" on:click={addNewAction}>New Action</button>
					</div>
				</div>
				<div>
					<h3>Knowledge</h3>
					<div>
						{#each $gptEditing.file_ids as file_id}
							<div class="fileContainer">
								<span>{file_id}</span>
								<button on:click={() => removeFile(file_id)}> Remove </button>
							</div>
						{/each}
						<label for="files">Upload files:</label>
						<input
							id="files"
							type="file"
							disabled={fileUploadLoading}
							bind:files={selectedFiles}
							on:change={submitFile}
						/>
					</div>
				</div>
				<div class="input--mb">
					<h3>Visibility</h3>
					<label for="visibility">Visibility</label>
					<select id="visibility" bind:value={$gptEditing.metadata.visibility}>
						<option value="private">{Visibility.PRIVATE}</option>
						<option value="public">{Visibility.PUBLIC}</option>
					</select>
				</div>
				<div class="save-publish-buttons">
					<button on:click={onSave}>Save</button>
					<button on:click={publishGpt}>Publish</button>
				</div>
			</form>
			<div class="chat">
				{#if $gptEditing.id && threadId}
					<Chat gptId={$gptEditing.id} {threadId} preMessage={() => {}} />
				{:else}
					<h2>Make sure to save your GPT before using</h2>
				{/if}
			</div>
		</div>
	</div>
{:else}
	<h3>Must be logged in</h3>
{/if}

<style>
	.wrapper {
		display: flex;
		flex-direction: column;
		height: calc(100vh - 2rem); /* Adjust the height to be 100vh - 2rem */
		overflow: hidden; /* Prevent the wrapper from scrolling */
	}

	.content {
		display: flex;
		gap: 1rem;
		overflow: hidden; /* Prevent the content area from scrolling */
	}

	.gpt_fields,
	.chat {
		position: relative;
		height: 100%;
		flex: 1;
		overflow-y: auto; /* Allow each section to scroll independently */
		margin-bottom: 1rem; /* Optional: add some space at the bottom */
		margin: 0;
	}

	.content {
		display: flex;
		gap: 1rem;
		overflow: hidden; /* Prevent the content area from scrolling */
	}

	.chat {
		display: flex;
		flex-direction: column;
	}
	h2 {
		margin-bottom: 1rem;
	}

	h3 {
		margin-bottom: 0.5rem;
	}

	.content {
		display: flex;
		gap: 1rem;
	}
	.content > * {
		flex: 1 1 50%;
	}

	.save-publish-buttons {
		position: sticky;
		top: 1rem;
		right: 1rem;
		display: flex;
		gap: 1rem;
		z-index: 1;
	}
</style>
