from pathlib import Path

from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "CI-CD-Benchmark-Optimisation-Report.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

INK = colors.HexColor("#10231D")
MUTED = colors.HexColor("#536A61")
PANEL = colors.HexColor("#EFF5F2")
LINE = colors.HexColor("#C7D7D0")
ACCENT = colors.HexColor("#1B8B5A")
ACCENT_LIGHT = colors.HexColor("#9EF0C6")
ORANGE = colors.HexColor("#E98A32")
WHITE = colors.white

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=28,
        textColor=WHITE,
        alignment=TA_LEFT,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#DCEAE4"),
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17,
        textColor=INK,
        spaceBefore=8,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyCompact",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=INK,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=7.2,
        leading=9.5,
        textColor=MUTED,
    )
)
styles.add(
    ParagraphStyle(
        name="MetricValue",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=20,
        textColor=INK,
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="MetricLabel",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9,
        textColor=MUTED,
    )
)
styles.add(
    ParagraphStyle(
        name="LinkSmall",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=7.2,
        leading=9.5,
        textColor=ACCENT,
    )
)
styles.add(
    ParagraphStyle(
        name="TableHeader",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=7.2,
        leading=9.5,
        textColor=WHITE,
    )
)


def p(text, style="BodyCompact"):
    return Paragraph(text, styles[style])


def metric_card(value, label, note=""):
    rows = [[p(value, "MetricValue")], [p(label, "MetricLabel")]]
    if note:
        rows.append([p(note, "Small")])
    table = Table(rows, colWidths=[40 * mm], rowHeights=None)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PANEL),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, 0), 7),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
            ]
        )
    )
    return table


def duration_chart():
    drawing = Drawing(170 * mm, 37 * mm)
    drawing.add(String(0, 94, "Workflow duration (seconds)", fontName="Helvetica-Bold", fontSize=8, fillColor=INK))
    max_value = 120
    left = 40 * mm
    width = 112 * mm
    labels = [
        ("Mean baseline", 108, ORANGE, 76),
        ("Mean optimised", 93.6, ACCENT, 58),
        ("p95 baseline", 117, colors.HexColor("#F2B777"), 36),
        ("p95 optimised", 99, ACCENT_LIGHT, 18),
    ]
    for label, value, color, y in labels:
        drawing.add(String(0, y + 3, label, fontName="Helvetica", fontSize=7.5, fillColor=MUTED))
        drawing.add(Rect(left, y, width, 9, fillColor=colors.HexColor("#E5ECE8"), strokeColor=None))
        drawing.add(Rect(left, y, width * value / max_value, 9, fillColor=color, strokeColor=None))
        drawing.add(String(left + width + 5, y + 2, f"{value:g}s", fontName="Helvetica-Bold", fontSize=7.5, fillColor=INK))
    return drawing


def header_block():
    table = Table(
        [
            [p("CI/CD Benchmark &amp; Optimisation Report", "ReportTitle")],
            [p("GitHub Actions to GitHub Pages | Pipeline Observatory | 30 September 2026", "ReportSubtitle")],
        ],
        colWidths=[180 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), INK),
                ("LEFTPADDING", (0, 0), (-1, -1), 13),
                ("RIGHTPADDING", (0, 0), (-1, -1), 13),
                ("TOPPADDING", (0, 0), (-1, 0), 13),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 12),
            ]
        )
    )
    return table


def result_table():
    data = [
        [p("Metric", "TableHeader"), p("Baseline", "TableHeader"), p("Optimised", "TableHeader"), p("Change", "TableHeader")],
        [p("Average total", "Small"), p("108.0 s", "Small"), p("93.6 s", "Small"), p("<b>-13.3%</b>", "Small")],
        [p("p95 total", "Small"), p("117 s", "Small"), p("99 s", "Small"), p("<b>-15.4%</b>", "Small")],
        [p("Build", "Small"), p("1.4 s / 2 builds", "Small"), p("1.2 s / 1 build", "Small"), p("1 build removed", "Small")],
        [p("Test", "Small"), p("1.2 s", "Small"), p("1.2 s", "Small"), p("0%", "Small")],
        [p("Scan", "Small"), p("68.6 s", "Small"), p("65.4 s", "Small"), p("-4.7%", "Small")],
        [p("Deployment job", "Small"), p("19.0 s", "Small"), p("9.4 s", "Small"), p("<b>-50.5%</b>", "Small")],
        [p("Failure rate", "Small"), p("0/5", "Small"), p("0/5", "Small"), p("No regression", "Small")],
    ]
    table = Table(data, colWidths=[48 * mm, 39 * mm, 39 * mm, 42 * mm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), INK),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("BACKGROUND", (0, 1), (-1, -1), WHITE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PANEL]),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def link(label, url):
    return p(f'<link href="{url}" color="#1B8B5A"><u>{label}</u></link>', "LinkSmall")


def multi_links(items):
    fragments = [f'<link href="{url}" color="#1B8B5A"><u>{label}</u></link>' for label, url in items]
    return p(" / ".join(fragments), "LinkSmall")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.4)
    canvas.line(15 * mm, 11 * mm, 195 * mm, 11 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(15 * mm, 7 * mm, "CI/CD Benchmark & Optimisation Report")
    canvas.drawRightString(195 * mm, 7 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=15 * mm,
    leftMargin=15 * mm,
    topMargin=12 * mm,
    bottomMargin=15 * mm,
    title="CI/CD Benchmark & Optimisation Report",
    author="Pipeline Observatory benchmark",
)

story = [header_block(), Spacer(1, 7 * mm)]

story.append(
    Table(
        [[
            metric_card("-13.3%", "Mean duration", "108.0s to 93.6s"),
            metric_card("-15.4%", "p95 duration", "117s to 99s"),
            metric_card("0%", "Failure rate", "10/10 passed"),
            metric_card("-84.3%", "Rollback time", "108s proxy to 17s"),
        ]],
        colWidths=[42.5 * mm] * 4,
        style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 2)],
    )
)
story += [Spacer(1, 4 * mm), p("Objective and method", "Section")]
story.append(
    p(
        "A real Vite website was built, tested, security-scanned and deployed to GitHub Pages. "
        "Two matched samples used five sequential workflow_dispatch runs on the same application, lockfile and ubuntu-latest runner label. "
        "Total duration is GitHub's workflow startedAt-to-updatedAt interval; p95 uses nearest rank. Step timestamps have one-second resolution."
    )
)
story.append(duration_chart())
story.append(p("Optimisations implemented", "Section"))

changes = [
    [p("1", "MetricValue"), p("<b>Dependency caching</b><br/>setup-node restores npm cache keyed by package-lock.json.", "Small")],
    [p("2", "MetricValue"), p("<b>Parallel quality gates</b><br/>Lint/tests, CodeQL/dependency scans and build execute concurrently.", "Small")],
    [p("3", "MetricValue"), p("<b>Build once and reuse</b><br/>The tested dist artifact is deployed directly and retained for 30-day rollback.", "Small")],
]
change_table = Table(changes, colWidths=[13 * mm, 155 * mm])
change_table.setStyle(
    TableStyle(
        [
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [PANEL, WHITE]),
            ("BOX", (0, 0), (-1, -1), 0.5, LINE),
            ("INNERGRID", (0, 0), (-1, -1), 0.3, LINE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
    )
)
story.append(change_table)
story.append(Spacer(1, 4 * mm))
story.append(p("Measured results", "Section"))
story.append(result_table())

story.append(PageBreak())
story.append(p("Interpretation", "Section"))
story.append(
    p(
        "Average delivery time fell by 14.4 seconds (13.3%) and p95 fell by 18 seconds (15.4%). "
        "The deployment job improved most because it no longer repeats checkout, dependency installation or compilation. "
        "CodeQL remained the critical path, so the total reduction is smaller than the 50.5% deployment-job improvement."
    )
)
story.append(
    p(
        "All ten measured runs passed, so failure rate remained 0%; an improvement could not be demonstrated without manufacturing failures. "
        "The automatic post-merge run (111 seconds) warmed the cache and is disclosed but excluded from the matched five-run sample. "
        "Aggregate npm ci time did not decrease because three parallel jobs each install dependencies; for this small project, runner variability dominates."
    )
)

rollback_box = Table(
    [[
        p("<b>Rollback validation</b><br/><br/>Baseline recovery required rebuilding a historical commit through the full 108-second pipeline proxy. "
          "The new workflow redeployed the retained immutable artifact in <b>17 seconds</b> and the live-site smoke test passed. "
          "This is an <b>84.3% recovery-time reduction</b> and avoids dependency drift during recovery.", "BodyCompact")
    ]],
    colWidths=[168 * mm],
)
rollback_box.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#DFF7E9")),
            ("BOX", (0, 0), (-1, -1), 1, ACCENT),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]
    )
)
story += [Spacer(1, 4 * mm), rollback_box, Spacer(1, 4 * mm)]

story.append(p("Evidence and traceability", "Section"))
evidence_rows = [
    [p("Change", "Small"), link("Baseline commit 95f5222", "https://github.com/s9cspawn/cicd-optimisation-demo/commit/95f52226fa664d289b9209a589a36f302d1d564f"), link("Optimisation PR #1", "https://github.com/s9cspawn/cicd-optimisation-demo/pull/1")],
    [p("Baseline runs", "Small"), multi_links([("1", "https://github.com/s9cspawn/cicd-optimisation-demo/actions/runs/36697503043"), ("2", "https://github.com/s9cspawn/cicd-optimisation-demo/actions/runs/36698081105"), ("3", "https://github.com/s9cspawn/cicd-optimisation-demo/actions/runs/36698351025")]), multi_links([("4", "https://github.com/s9cspawn/cicd-optimisation-demo/actions/runs/36698677932"), ("5", "https://github.com/s9cspawn/cicd-optimisation-demo/actions/runs/36698905269")])],
    [p("Optimised runs", "Small"), multi_links([("1", "https://github.com/s9cspawn/cicd-optimisation-demo/actions/runs/36702435710"), ("2", "https://github.com/s9cspawn/cicd-optimisation-demo/actions/runs/36702876074"), ("3", "https://github.com/s9cspawn/cicd-optimisation-demo/actions/runs/36703118636")]), multi_links([("4", "https://github.com/s9cspawn/cicd-optimisation-demo/actions/runs/36703327609"), ("5", "https://github.com/s9cspawn/cicd-optimisation-demo/actions/runs/36703560098")])],
    [p("Rollback", "Small"), link("Run 36704893909", "https://github.com/s9cspawn/cicd-optimisation-demo/actions/runs/36704893909"), link("Rollback workflow", "https://github.com/s9cspawn/cicd-optimisation-demo/blob/main/.github/workflows/rollback.yml")],
    [p("Exports", "Small"), link("Baseline CSV/JSON", "https://github.com/s9cspawn/cicd-optimisation-demo/tree/main/evidence"), link("Optimised CSV/JSON", "https://github.com/s9cspawn/cicd-optimisation-demo/tree/main/evidence")],
    [p("Deployment", "Small"), link("Live GitHub Pages site", "https://s9cspawn.github.io/cicd-optimisation-demo/"), link("Repository", "https://github.com/s9cspawn/cicd-optimisation-demo")],
]
evidence_table = Table(evidence_rows, colWidths=[32 * mm, 68 * mm, 68 * mm])
evidence_table.setStyle(
    TableStyle(
        [
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [PANEL, WHITE]),
            ("GRID", (0, 0), (-1, -1), 0.4, LINE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story.append(evidence_table)

story += [Spacer(1, 5 * mm), p("Conclusion", "Section")]
story.append(
    p(
        "The optimised workflow achieved repeatable mean and p95 reductions without removing any test or security gate. "
        "Artifact reuse delivered the clearest stage improvement and transformed rollback from a full rebuild into a fast, verified redeployment."
    )
)
story.append(
    p(
        "Limitations: n=5 per phase; GitHub-hosted runner demand varies; one-second timestamps obscure subsecond changes; "
        "the 108-second baseline rollback value is a full-pipeline proxy rather than a separately repeated rollback sample.",
        "Small",
    )
)

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT)
