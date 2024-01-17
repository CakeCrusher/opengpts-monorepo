import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Optional
from models.thread import (
    RunStepsResponse,
    ThreadMessage,
)

load_dotenv()

openai_client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def get_run_steps_and_messages(
    openai_client: OpenAI,
    thread_id: str,
    run_id: str,
    step_callback: Optional[callable] = None,
) -> RunStepsResponse:
    run_steps = openai_client.beta.threads.runs.steps.list(
        thread_id=thread_id,
        run_id=run_id,
    )
    messages: Dict[str, ThreadMessage] = {}
    run_steps_list = []

    # Iterate over the data in run_steps
    for step in run_steps:
        step_callback(step) if step_callback else None
        if step.type == 'message_creation':
            # Retrieve the message
            message = openai_client.beta.threads.messages.retrieve(
                thread_id=step.thread_id,
                message_id=step.step_details.message_creation.message_id,
            )
            # Map the message to the message_id in the hash map
            messages[
                step.step_details.message_creation.message_id
            ] = message.model_dump()
            # Pydandtic does not recognize the ThreadMessage object,
            # so it must be serialized

        run_steps_list.append(step)

    return RunStepsResponse(
        messages=messages,
        run_steps=run_steps_list,
    )
