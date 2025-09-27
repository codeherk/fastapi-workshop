from typing import Optional

from .schemas import TaskCreate
from .storage import Storage

# --- NEW: imports ---
from typing import Optional
import os

try:
    from transformers import pipeline
    import torch
except Exception:
    # Let the app still run if transformers/torch aren't installed
    pipeline = None
    torch = None

class Service:
    def __init__(self):
        super().__init__()
        # TODO: add config as class arg and reference when init Storage
        sqlite_file_name = "database.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        connect_args = {"check_same_thread": False}
        self.storage = Storage(sqlite_url, connect_args=connect_args)

        # --- NEW: optional, lazy-loaded local HF pipeline ---
        self._text_gen = None
        self._hf_model_id = os.getenv("HF_LOCAL_MODEL_ID", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self._max_new_tokens = int(os.getenv("HF_MAX_NEW_TOKENS", "220"))

        return


    def create_task_with_ai_response(self, data: TaskCreate):
        # 1) Create the task as usual (DB write happens inside storage)
        created_task = self.storage.create_task(data)

        # 2) Generate a local model follow-up suggestion based on the title
        model_response = self.generate_model_response(getattr(data, "title", ""))

        # 3) Return both, but DO NOT persist model_response
        #    Shape this however your API layer expects. Common pattern:
        return {
            "task": created_task,  # your ORM/Pydantic object
            "model_response": model_response  # str | None (not stored in DB)
        }



#Cool stuff below: local text generation for follow-up message

    #Small helper to initialize a local text-generation pipeline on first use
    def ensure_text_gen(self):
        if self._text_gen is not None:
            return
        if pipeline is None:
            # transformers/torch not installed; leave as None so we gracefully skip generation
            return
        # device_map="auto" will use GPU if available, CPU otherwise
        dtype = torch.float16 if torch and torch.cuda.is_available() else torch.float32
        self._text_gen = pipeline(
            "text-generation",
            model=self._hf_model_id,  # swap to any local model you’ve downloaded / cached
            device_map="auto",
            torch_dtype=dtype,
        )

    #Build a clear prompt to get a short, ready to send message
    def build_followup_prompt(self, title: str) -> str:
        return (
            "You are a helpful assistant. Using the task title provide a helpful response to assist with completing the task"
            "e.g if the title is 'Buy groceries', a good response would be 'Don't forget to check for discounts and make a list of essentials.'"
            "e.g if the title is to send an email/message, provide a short, polite, message that can be sent as is"
            f"Task Title: \"{title}\""
        )

    #Generate text locally; safe to fail without breaking task creation ---
    def generate_model_response(self, title: str) -> Optional[str]:
        self.ensure_text_gen()
        if self._text_gen is None:
            return None  # transformers not available / model not loaded
        prompt = self.build_followup_prompt(title)
        try:
            out = self._text_gen(
                prompt,
                max_new_tokens=self._max_new_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                eos_token_id=None,  # let model decide; many chat models stop naturally
            )
            # Some models echo the prompt—trim it if present.
            text = out[0]["generated_text"]
            if text.startswith(prompt):
                text = text[len(prompt):].lstrip()
            # simple post-process: keep only the first paragraph
            return text.strip().split("\n\n")[0].strip()
        except Exception:
            # Don’t break the main flow if generation fails
            return None