import os
import openai
openai.organization = "org-ml2rVfxmOg8B1S2tlQqQOLVe"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()