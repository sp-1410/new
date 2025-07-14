from transformers import T5Tokenizer, T5ForConditionalGeneration
import gradio as gr
from fpdf import FPDF

# Load model and tokenizer
print("Loading model...")
tok = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")
print("Model loaded successfully!")

# Store flashcards globally
cards = []

def generate_notes(notes):
    global cards
    cards = []
    for s in notes.split("."):
        s = s.strip()
        if len(s) < 10:
            continue
        ids = tok.encode("generate question: " + s, return_tensors="pt", truncation=True)
        out = model.generate(ids, max_length=64, num_beams=4, early_stopping=True)
        q = tok.decode(out[0], skip_special_tokens=True)
        cards.append((q, s))
    return f"✅ Generated {len(cards)} flashcards." if cards else "⚠️ No flashcards created."

def show_card(idx):
    if not cards:
        return "⚠️ No cards yet. Click Generate.", 0
    idx = max(0, min(idx, len(cards)-1))
    q, a = cards[idx]
    return f"Q: {q}\n\nA: {a}", idx

def next_card(idx): return show_card(idx + 1)
def prev_card(idx): return show_card(idx - 1)

def save_pdf():
    if not cards:
        return "⚠️ Nothing to save."
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "AI Flashcards", ln=True, align="C")
    for i, (q, a) in enumerate(cards, 1):
        pdf.ln(5)
        pdf.multi_cell(0, 8, f"{i}. Q: {q}\nA: {a}")
    pdf.output("flashcards.pdf")
    return "✅ Saved as flashcards.pdf"

# Build Gradio interface
# Build Gradio interface
with gr.Blocks() as app:
    gr.Markdown("# 🧠 AI Flashcard Generator")
    notes_box = gr.Textbox(lines=10, label="Paste notes")
    gen_btn = gr.Button("Generate")
    status = gr.Textbox(interactive=False, label="Status")
    card_view = gr.Textbox(lines=4, interactive=False, label="Flashcard")
    idx_state = gr.State(0)

    with gr.Row():
        prev_btn = gr.Button("⬅️ Previous")
        next_btn = gr.Button("Next ➡️")
        pdf_btn = gr.Button("📄 Save to PDF")

    gen_btn.click(generate_notes, notes_box, status).then(
        fn=show_card, inputs=idx_state, outputs=[card_view, idx_state]
    )
    next_btn.click(next_card, idx_state, [card_view, idx_state])
    prev_btn.click(prev_card, idx_state, [card_view, idx_state])
    pdf_btn.click(save_pdf, outputs=status)

print("Launching app on browser...")
app.launch(share=True)
