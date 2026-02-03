from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import os


def generate_mom_pdf(
    output_path: str,
    meeting_title: str,
    transcript: str,
    summary: str,
    action_items: list,
    impact_points: list
) -> str:
    """
    Generate MOM (Minutes of Meeting) PDF

    Parameters:
    - output_path: path to save pdf
    - meeting_title: title of meeting
    - transcript: full transcript text
    - summary: meeting summary
    - action_items: list of action items
    - impact_points: list of dicts with 'sentence' and 'score'
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="TitleStyle",
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=20
    ))

    styles.add(ParagraphStyle(
        name="HeaderStyle",
        fontSize=14,
        spaceBefore=16,
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name="BodyStyle",
        fontSize=10,
        spaceAfter=8
    ))

    content = []

    # ---------------- TITLE ----------------
    content.append(Paragraph("Minutes of Meeting (MOM)", styles["TitleStyle"]))
    content.append(Paragraph(meeting_title, styles["HeaderStyle"]))
    content.append(
        Paragraph(
            f"Date: {datetime.now().strftime('%d %B %Y, %H:%M')}",
            styles["BodyStyle"]
        )
    )
    content.append(Spacer(1, 12))

    # ---------------- SUMMARY ----------------
    content.append(Paragraph("Meeting Summary", styles["HeaderStyle"]))
    content.append(Paragraph(summary, styles["BodyStyle"]))

    # ---------------- KEY INSIGHTS ----------------
    if impact_points:
        content.append(Paragraph("Key Insights", styles["HeaderStyle"]))
        insights_list = [
            ListItem(
                Paragraph(
                    f"<b>Score {item['score']}:</b> {item['sentence']}",
                    styles["BodyStyle"]
                )
            )
            for item in impact_points
        ]
        content.append(ListFlowable(insights_list, bulletType="bullet"))

    # ---------------- ACTION ITEMS ----------------
    if action_items:
        content.append(Paragraph("Action Items", styles["HeaderStyle"]))
        action_list = [
            ListItem(Paragraph(item, styles["BodyStyle"]))
            for item in action_items
        ]
        content.append(ListFlowable(action_list, bulletType="bullet"))

    # ---------------- TRANSCRIPT ----------------
    content.append(Paragraph("Full Transcript", styles["HeaderStyle"]))
    for para in transcript.split("\n"):
        if para.strip():
            content.append(Paragraph(para, styles["BodyStyle"]))

    # ---------------- BUILD PDF ----------------
    doc.build(content)

    return output_path
