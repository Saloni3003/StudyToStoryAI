import re
import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM


# ============================================================
# MODEL CONFIGURATION
# ============================================================

MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"


# ============================================================
# DEVICE SELECTION
# ============================================================

if torch.backends.mps.is_available():
    DEVICE = "mps"
elif torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    print(f"Loading Qwen model on: {DEVICE}")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype=torch.float16 if DEVICE in ["mps", "cuda"] else torch.float32
    )

    model = model.to(DEVICE)

    return tokenizer, model


# ============================================================
# PREPARE SOURCE MATERIAL
# ============================================================

def prepare_source(text, max_chars=12000):

    text = text.strip()

    if not text:
        return ""

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    # Keep the source within a reasonable size
    return text[:max_chars]


# ============================================================
# CLEAN GENERATED STORY
# ============================================================

def clean_storyboard(story):

    # Remove markdown formatting
    story = story.replace("**", "")

    # Remove unwanted code fences
    story = story.replace("```text", "")
    story = story.replace("```", "")

    story = story.strip()

    return story


# ============================================================
# GENERATE EDUCATIONAL STORYBOARD
# ============================================================

def generate_story(source_text):

    source_text = prepare_source(source_text)

    if not source_text:
        return "ERROR: No study material was provided."

    tokenizer, model = load_model()

    # --------------------------------------------------------
    # IMPORTANT:
    # The source material is the ONLY factual source.
    # --------------------------------------------------------

    prompt = f"""
You are an educational video storyboard writer.

Your task is to transform the PROVIDED STUDY MATERIAL into
a simple and engaging educational explanation.

STRICT SOURCE-GROUNDING RULE:

The study material below is the ONLY source of factual
information.

You MUST NOT add facts, features, examples, applications,
technical terms, components, advantages, disadvantages,
processes, or concepts that are not explicitly stated or
clearly implied by the study material.

Do NOT use your general knowledge about the topic.

If the study material contains only one or two concepts,
explain those concepts from different educational angles
instead of introducing new concepts.

You may use a simple analogy ONLY when the analogy does not
introduce a new factual claim.

For example, if the source says that Hadoop stores and
processes large datasets across multiple computers, you may
use a simple analogy of distributing books among several
shelves.

However, you MUST NOT introduce concepts such as:
HDFS, MapReduce, NameNode, DataNode, fault tolerance,
scalability, cluster management, workload balancing,
parallel processing, structured data, unstructured data,
or any other Hadoop feature unless it appears in the source.

============================================================
EDUCATIONAL STORY REQUIREMENTS
============================================================

Create EXACTLY 6 scenes.

The purpose is to TEACH the content, not simply list facts.

The explanation should progress naturally:

Scene 1:
Introduce the main topic using only the source.

Scene 2:
Explain the first important idea from the source.

Scene 3:
Explain another part of the same source material.

Scene 4:
Give a simple source-grounded explanation or analogy.

Scene 5:
Connect the ideas already present in the source.

Scene 6:
Give a concise summary of ONLY what was learned.

IMPORTANT:

If the source is very short, do NOT invent additional
technical information just to make six scenes.

Instead, break the existing information into smaller
educational steps and use simple analogies.

============================================================
NARRATION REQUIREMENTS
============================================================

Each narration should contain approximately 2–3 natural
sentences.

The narration should sound like a human educational
explainer speaking to a student.

Avoid:
- unnecessary repetition
- exaggerated claims
- unsupported facts
- marketing language
- advanced concepts not present in the source

Keep the language simple and clear.

============================================================
VISUAL REQUIREMENTS
============================================================

The visual must directly represent the narration.

Use realistic educational visuals such as:

- students
- computers
- data
- documents
- simple computer networks
- books or boxes as analogies
- laboratory environments

Do NOT put technical text, labels, equations, logos,
or long written explanations inside AI-generated images.

============================================================
OUTPUT FORMAT
============================================================

Return EXACTLY this format:

TITLE:
<short educational title>

SCENE 1:
Narration: <2–3 sentences>
Visual: <visual description>
Animation: <simple animation>
Technical Concept: <concept directly supported by source>
Transition: fade

SCENE 2:
Narration: <2–3 sentences>
Visual: <visual description>
Animation: <simple animation>
Technical Concept: <concept directly supported by source>
Transition: fade

SCENE 3:
Narration: <2–3 sentences>
Visual: <visual description>
Animation: <simple animation>
Technical Concept: <concept directly supported by source>
Transition: fade

SCENE 4:
Narration: <2–3 sentences>
Visual: <visual description>
Animation: <simple animation>
Technical Concept: <concept directly supported by source>
Transition: fade

SCENE 5:
Narration: <2–3 sentences>
Visual: <visual description>
Animation: <simple animation>
Technical Concept: <concept directly supported by source>
Transition: fade

SCENE 6:
Narration: <2–3 sentences>
Visual: <visual description>
Animation: <simple animation>
Technical Concept: <concept directly supported by source>
Transition: fade

============================================================
STUDY MATERIAL
============================================================

{source_text}

============================================================

Now generate the EXACTLY 6-scene educational storyboard.
Remember: do NOT add factual information that is absent
from the study material.
"""

    messages = [
        {
            "role": "system",
            "content": (
                "You are a precise educational storyboard "
                "generator. Follow the requested format exactly "
                "and never add unsupported facts."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

        # ========================================================
    # TOKENIZE
    # ========================================================

    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        return_tensors="pt",
        add_generation_prompt=True
    )

    input_ids = inputs["input_ids"].to(DEVICE)
    attention_mask = inputs["attention_mask"].to(DEVICE)

    # ========================================================
    # GENERATE
    # ========================================================

    with torch.no_grad():

        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=1600,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
    )

    # ========================================================
    # DECODE
    # ========================================================

    generated_tokens = outputs[0][input_ids.shape[-1]:]

    story = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
)

    story = clean_storyboard(story)

    return story