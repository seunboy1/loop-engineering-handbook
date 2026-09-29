#!/usr/bin/env python3
"""
Generate a 10-slide LinkedIn carousel PDF for the Loop Engineering Handbook.
Output: docs/images/loop-engineering-carousel.pdf
Run:    python3 scripts/generate-carousel.py
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import os

# ── Palette ────────────────────────────────────────────────────────────────
BG       = HexColor("#0f1a14")   # near-black green
CARD     = HexColor("#1b2a20")   # card surface
ACCENT   = HexColor("#57e389")   # bright green
WHITE    = HexColor("#f7f7f3")   # off-white
MUTED    = HexColor("#7a9988")   # muted text
CODE_BG  = HexColor("#111f17")   # code block bg
CODE_FG  = HexColor("#a3e4b0")   # code text

# ── Page size: square 1080×1080 pt (LinkedIn-optimal) ──────────────────────
W = H = 1080

OUT = "docs/images/loop-engineering-carousel.pdf"
os.makedirs("docs/images", exist_ok=True)

# ── Helpers ────────────────────────────────────────────────────────────────
def make_canvas(path):
    c = canvas.Canvas(path, pagesize=(W, H))
    return c

def bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def tag(c, text, x, y):
    """Small pill label."""
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 11)
    tw = c.stringWidth(text, "Helvetica-Bold", 11)
    pad = 10
    c.roundRect(x, y - 4, tw + pad*2, 22, 6, fill=1, stroke=0)
    c.setFillColor(BG)
    c.drawString(x + pad, y + 4, text)

def headline(c, text, y, size=52, color=WHITE):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", size)
    c.drawString(60, y, text)

def headline_green(c, text, y, size=52):
    headline(c, text, y, size, ACCENT)

def body(c, text, y, size=22, color=WHITE, x=60, width=960):
    """Word-wrapped body text."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    c.setFillColor(color)
    c.setFont("Helvetica", size)
    words = text.split()
    line = ""
    line_y = y
    for word in words:
        test = (line + " " + word).strip()
        if stringWidth(test, "Helvetica", size) > width:
            c.drawString(x, line_y, line)
            line_y -= size * 1.45
            line = word
        else:
            line = test
    if line:
        c.drawString(x, line_y, line)
    return line_y - size * 1.45

def rule(c, y):
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2)
    c.line(60, y, W - 60, y)

def slide_number(c, n, total=10):
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 16)
    c.drawRightString(W - 60, 36, f"{n} / {total}")

def footer_bar(c, text):
    c.setFillColor(CARD)
    c.rect(0, 0, W, 62, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(60, 20, text)

def code_block(c, lines, y, font_size=18):
    """Draw a code block and return the bottom y."""
    line_h = font_size * 1.6
    block_h = len(lines) * line_h + 28
    c.setFillColor(CODE_BG)
    c.roundRect(60, y - block_h + 14, W - 120, block_h, 10, fill=1, stroke=0)
    c.setFillColor(CODE_FG)
    c.setFont("Courier-Bold", font_size)
    ty = y - 8
    for line in lines:
        c.drawString(82, ty, line)
        ty -= line_h
    return ty - 10

def bullet(c, items, y, size=21, indent=60, gap=14):
    """Dot-bulleted list; returns final y."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    for item in items:
        c.setFillColor(ACCENT)
        c.circle(indent + 8, y + 7, 5, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica", size)
        # wrap
        words = item.split()
        line = ""
        lx = indent + 24
        lw = W - lx - 60
        line_y = y
        for word in words:
            test = (line + " " + word).strip()
            if stringWidth(test, "Helvetica", size) > lw:
                c.drawString(lx, line_y, line)
                line_y -= size * 1.4
                line = word
            else:
                line = test
        if line:
            c.drawString(lx, line_y, line)
        y = line_y - size * 1.4 - gap
    return y

def numbered_item(c, n, title, desc, y, title_size=22, desc_size=19):
    """Numbered card row."""
    # circle
    c.setFillColor(ACCENT)
    c.circle(84, y + 6, 18, fill=1, stroke=0)
    c.setFillColor(BG)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(84, y, str(n))
    # title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", title_size)
    c.drawString(114, y + 6, title)
    # desc
    c.setFillColor(MUTED)
    c.setFont("Helvetica", desc_size)
    c.drawString(114, y - 18, desc)
    return y - 58

# ═══════════════════════════════════════════════════════════════════════════
# SLIDES
# ═══════════════════════════════════════════════════════════════════════════
c = canvas.Canvas(OUT, pagesize=(W, H))

# ── SLIDE 1 : Cover ────────────────────────────────────────────────────────
bg(c)
tag(c, "AGENT ENGINEERING", 60, 920)
c.setFillColor(WHITE);  c.setFont("Helvetica-Bold", 68); c.drawString(60, 820, "Stop Prompting")
c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 68); c.drawString(60, 740, "Agents.")
c.setFillColor(WHITE);  c.setFont("Helvetica-Bold", 68); c.drawString(60, 660, "Start Designing")
c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 68); c.drawString(60, 580, "Loops.")
rule(c, 530)
body(c, "Most developers use coding agents like a faster search box. There is a better way.", 480, size=23, color=MUTED)
body(c, "10 slides  •  Practical system design  •  Real guardrails", 360, size=19, color=MUTED)
slide_number(c, 1)
footer_bar(c, "github.com/seunboy1/loop-engineering-handbook")
c.showPage()

# ── SLIDE 2 : The core shift ───────────────────────────────────────────────
bg(c)
tag(c, "THE CORE SHIFT", 60, 960)
headline(c, "A prompt gives you", 880)
headline_green(c, "an answer.", 810)
headline(c, "A loop gives you", 730)
headline_green(c, "a workflow.", 660)
rule(c, 620)
body(c, "When you prompt an agent you ask: what should it do?", 576, size=23)
body(c, "When you design a loop you ask:", 530, size=23)
y = bullet(c, [
    "Where do tasks come from?",
    "Which decisions are safe to delegate?",
    "What proves the result is correct?",
    "Who makes the irreversible decision?",
], 478, size=21)
slide_number(c, 2)
footer_bar(c, "Loop Engineering Handbook  •  2 of 10")
c.showPage()

# ── SLIDE 3 : What a loop actually looks like ──────────────────────────────
bg(c)
tag(c, "ANATOMY OF A LOOP", 60, 960)
headline(c, "Five moves.", 880)
headline_green(c, "Every loop.", 810)
rule(c, 770)
y = numbered_item(c, 1, "Wake",        "on a schedule or event",                     720)
y = numbered_item(c, 2, "Read state",  "from a visible control plane",               y)
y = numbered_item(c, 3, "Choose",      "one bounded, policy-allowed action",         y)
y = numbered_item(c, 4, "Change",      "the world: update a ticket or open a PR",    y)
y = numbered_item(c, 5, "Record",      "evidence and stop. Repeat later.",           y)
rule(c, y - 10)
body(c, "The loop is easy. Designing the boundaries around it is the real engineering.", y - 54, size=21, color=MUTED)
slide_number(c, 3)
footer_bar(c, "Loop Engineering Handbook  •  3 of 10")
c.showPage()

# ── SLIDE 4 : Control plane ────────────────────────────────────────────────
bg(c)
tag(c, "CONTROL PLANE", 60, 960)
headline(c, "Visible state beats", 880)
headline_green(c, "agent memory.", 810)
rule(c, 770)
body(c, "GitHub Issues works as a control plane because it already has:", 728, size=23)
y = bullet(c, [
    "Durable tickets and acceptance criteria",
    "Labels that act as a small policy language",
    "Comments that form an audit trail",
    "Links from issues to branches and pull requests",
    "Human permissions and override controls",
], 676, size=21)
rule(c, y - 10)
body(c, "Agents read from it before acting. They write evidence back after.", y - 60, size=21, color=MUTED)
body(c, "A human can reroute work by changing a label. No hunting for hidden prompts.", y - 100, size=21, color=MUTED)
slide_number(c, 4)
footer_bar(c, "Loop Engineering Handbook  •  4 of 10")
c.showPage()

# ── SLIDE 5 : Label taxonomy ───────────────────────────────────────────────
bg(c)
tag(c, "LABEL TAXONOMY", 60, 960)
headline(c, "Labels are your", 880)
headline_green(c, "policy language.", 810)
rule(c, 770)

# three columns
col = [(60, "RISK", ["risk:low", "risk:medium", "risk:high"]),
       (380, "TYPE",  ["type:bug", "type:docs", "type:test", "type:feature", "type:refactor"]),
       (700, "ROUTING", ["agent-ready", "needs-human", "blocked"])]

for cx, title, items in col:
    c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 20); c.drawString(cx, 730, title)
    ty = 690
    for item in items:
        c.setFillColor(CARD)
        tw = c.stringWidth(item, "Courier-Bold", 16) + 20
        c.roundRect(cx, ty - 6, tw, 26, 6, fill=1, stroke=0)
        c.setFillColor(CODE_FG); c.setFont("Courier-Bold", 16); c.drawString(cx + 10, ty + 4, item)
        ty -= 44

rule(c, 390)
y = code_block(c, [
    "gh issue list --search \\",
    "  'is:open label:agent-ready label:risk:low \\",
    "   -label:needs-human' --limit 1",
], 370, font_size=16)
body(c, "The worker queue is a transparent, deterministic query.", y - 20, size=20, color=MUTED)
slide_number(c, 5)
footer_bar(c, "Loop Engineering Handbook  •  5 of 10")
c.showPage()

# ── SLIDE 6 : Two loops ────────────────────────────────────────────────────
bg(c)
tag(c, "ARCHITECTURE", 60, 960)
headline(c, "Two loops.", 880)
headline_green(c, "Different jobs.", 810)
rule(c, 770)

# Manager box
c.setFillColor(CARD); c.roundRect(60, 530, 440, 220, 14, fill=1, stroke=0)
c.setStrokeColor(ACCENT); c.setLineWidth(2); c.roundRect(60, 530, 440, 220, 14, fill=0, stroke=1)
c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 22); c.drawString(84, 724, "LOOP 1  —  MANAGER")
c.setFillColor(WHITE); c.setFont("Helvetica", 19)
for i, txt in enumerate(["Reads open issues", "Applies risk + routing labels", "Never touches code"]):
    c.drawString(84, 686 - i*36, "•  " + txt)
c.setFillColor(MUTED); c.setFont("Helvetica", 16); c.drawString(84, 548, "permissions: issues:write  contents:read")

# Worker box
c.setFillColor(CARD); c.roundRect(560, 530, 460, 220, 14, fill=1, stroke=0)
c.setStrokeColor(ACCENT); c.setLineWidth(2); c.roundRect(560, 530, 460, 220, 14, fill=0, stroke=1)
c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 22); c.drawString(584, 724, "LOOP 2  —  WORKER")
c.setFillColor(WHITE); c.setFont("Helvetica", 19)
for i, txt in enumerate(["Reads safe queue only", "Writes code + tests, opens PR", "Never merges or deploys"]):
    c.drawString(584, 686 - i*36, "•  " + txt)
c.setFillColor(MUTED); c.setFont("Helvetica", 16); c.drawString(584, 548, "permissions: contents:write  pulls:write")

rule(c, 510)
body(c, "The manager earns the worker. Neither earns the merge button.", 468, size=21, color=MUTED)
slide_number(c, 6)
footer_bar(c, "Loop Engineering Handbook  •  6 of 10")
c.showPage()

# ── SLIDE 7 : Inner workflow ───────────────────────────────────────────────
bg(c)
tag(c, "WORKER INNER LOOP", 60, 960)
headline(c, "Input: one ticket.", 880)
headline_green(c, "Output: one PR.", 810)
rule(c, 770)
steps = [
    ("1", "Verify clean tree",   "abort if dirty"),
    ("2", "Claim the issue",     "add agent-running label"),
    ("3", "Implement + test",    "smallest complete change"),
    ("4", "Fresh agent review",  "new context, no shared bias"),
    ("5", "Fix findings",        "rerun checks once"),
    ("6", "Open PR with evidence", "exact commands, outputs, risks"),
]
y = 730
for num, title, desc in steps:
    c.setFillColor(ACCENT); c.circle(84, y+6, 16, fill=1, stroke=0)
    c.setFillColor(BG); c.setFont("Helvetica-Bold", 16); c.drawCentredString(84, y+1, num)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 20); c.drawString(112, y+8, title)
    c.setFillColor(MUTED); c.setFont("Helvetica", 17); c.drawString(112, y-12, desc)
    y -= 52
rule(c, y - 8)
body(c, "The coordinator writes the worker prompt. The worker writes the review prompt.", y - 54, size=20, color=MUTED)
slide_number(c, 7)
footer_bar(c, "Loop Engineering Handbook  •  7 of 10")
c.showPage()

# ── SLIDE 8 : Guardrails ───────────────────────────────────────────────────
bg(c)
tag(c, "GUARDRAILS", 60, 960)
headline(c, "Prompts are not", 880)
headline_green(c, "permissions.", 810)
rule(c, 770)
body(c, '"Never deploy" is a useful instruction. It is not a security control.', 730, size=22)
body(c, "Real guardrails sit at multiple layers:", 684, size=22)
items = [
    "Selection — reject any issue missing required labels",
    "Quantity  — cap at 1 ticket until metrics hold, then 3 max",
    "Environment — abort on dirty working tree",
    "Permissions — least-privilege token, branch protection enforced",
    "Stop conditions — escalate on ambiguity, scope creep, or repeated failure",
]
y = bullet(c, items, 638, size=20)
rule(c, y - 10)
body(c, "A branch protection rule beats a sentence in a prompt every time.", y - 56, size=20, color=MUTED)
slide_number(c, 8)
footer_bar(c, "Loop Engineering Handbook  •  8 of 10")
c.showPage()

# ── SLIDE 9 : Metrics ─────────────────────────────────────────────────────
bg(c)
tag(c, "EVALUATION", 60, 960)
headline(c, "You cannot increase", 880)
headline_green(c, "trust without metrics.", 810)
rule(c, 770)
rows = [
    ("First-pass merge rate",  "PRs merged with no requested changes"),
    ("Rework rate",            "PRs substantially rewritten by a human"),
    ("Escalation precision",   "Agent asks for help at the right time"),
    ("Cost per merged PR",     "Tokens + CI spend per useful output"),
    ("Policy violations",      "Any prohibited action attempted — target: 0"),
]
y = 726
for metric, desc in rows:
    c.setFillColor(CARD); c.roundRect(60, y - 18, W - 120, 48, 8, fill=1, stroke=0)
    c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 19); c.drawString(80, y + 8, metric)
    c.setFillColor(MUTED);  c.setFont("Helvetica", 17);     c.drawString(80, y - 10, desc)
    y -= 64
rule(c, y - 8)
body(c, "A weekly scorecard beats a story about one impressive pull request.", y - 54, size=20, color=MUTED)
slide_number(c, 9)
footer_bar(c, "Loop Engineering Handbook  •  9 of 10")
c.showPage()

# ── SLIDE 10 : CTA ────────────────────────────────────────────────────────
bg(c)
tag(c, "GET STARTED", 60, 960)
headline(c, "Build one small loop", 880)
headline_green(c, "this week.", 810)
rule(c, 770)
steps2 = [
    "Create one clear issue with explicit acceptance criteria",
    "Apply risk:low and agent-ready labels",
    "Run the manager loop in dry-run mode first",
    "Allow one documentation or test PR before anything bigger",
    "Measure first-pass merge rate before expanding scope",
]
y = bullet(c, steps2, 724, size=21)
rule(c, y - 14)

# repo box
c.setFillColor(CARD); c.roundRect(60, 120, W - 120, 90, 12, fill=1, stroke=0)
c.setStrokeColor(ACCENT); c.setLineWidth(1.5); c.roundRect(60, 120, W - 120, 90, 12, fill=0, stroke=1)
c.setFillColor(ACCENT);  c.setFont("Helvetica-Bold", 20); c.drawString(90, 188, "Full handbook, scripts, and workflows:")
c.setFillColor(WHITE);   c.setFont("Courier-Bold", 20);  c.drawString(90, 152, "github.com/seunboy1/loop-engineering-handbook")

slide_number(c, 10)
footer_bar(c, "Follow for more  •  @seunboy1")
c.showPage()

c.save()
print(f"Carousel saved: {OUT}")
