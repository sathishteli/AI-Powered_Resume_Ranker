"""
Professional PDF HR report generator.

Creates a formatted PDF report from resume ranking results.
"""

from datetime import datetime
from html import escape
from io import BytesIO
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


def generate_pdf_report(
    results: list[dict[str, Any]],
    job_description: str,
) -> BytesIO:
    """
    Generate a professional HR evaluation PDF report.

    Parameters
    ----------
    results : list[dict]
        Ranked candidate results.

    job_description : str
        Job description used for ranking.

    Returns
    -------
    BytesIO
        PDF document stored in memory.
    """

    output = BytesIO()

    document = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="AI-Powered Resume Ranker - HR Report",
        author="AI-Powered Resume Ranker",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        leading=14,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=8,
    )

    candidate_heading_style = ParagraphStyle(
        "CandidateHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        spaceBefore=8,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        spaceAfter=5,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11,
    )

    insight_style = ParagraphStyle(
        "Insight",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=12,
        leftIndent=8,
        firstLineIndent=-8,
        spaceAfter=4,
    )

    story = []

    # ==================================================
    # TITLE
    # ==================================================

    story.append(
        Paragraph(
            "AI-POWERED RESUME RANKER",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "HR Candidate Evaluation Report",
            subtitle_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated:</b> "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            body_style,
        )
    )

    story.append(
        Spacer(1, 6)
    )

    # ==================================================
    # JOB DESCRIPTION
    # ==================================================

    story.append(
        Paragraph(
            "Job Description",
            heading_style,
        )
    )

    job_description_html = (
        escape(job_description.strip())
        .replace("\n", "<br/>")
    )

    story.append(
        Paragraph(
            job_description_html,
            small_style,
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # ==================================================
    # SUMMARY
    # ==================================================

    story.append(
        Paragraph(
            "Ranking Summary",
            heading_style,
        )
    )

    candidate_count = len(results)

    if results:

        average_score = sum(
            candidate["overall_score"]
            for candidate in results
        ) / candidate_count

    else:

        average_score = 0.0

    summary_data = [
        [
            "Candidates Evaluated",
            str(candidate_count),
        ],
        [
            "Average Overall Score",
            f"{average_score:.2f}%",
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            65 * mm,
            45 * mm,
        ],
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#eeeeee"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "Helvetica",
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    story.append(summary_table)

    story.append(
        Spacer(1, 12)
    )

    # ==================================================
    # RANKING TABLE
    # ==================================================

    story.append(
        Paragraph(
            "Candidate Ranking",
            heading_style,
        )
    )

    ranking_data = [
        [
            "Rank",
            "Candidate",
            "Skill Match",
            "Text Similarity",
            "Overall",
            "Recommendation",
        ]
    ]

    for candidate in results:

        ranking_data.append(
            [
                f"#{candidate['rank']}",
                candidate["candidate_name"],
                f"{candidate['skill_match_score']:.2f}%",
                f"{candidate['text_similarity_score']:.2f}%",
                f"{candidate['overall_score']:.2f}%",
                candidate.get(
                    "recommendation",
                    "N/A",
                ),
            ]
        )

    ranking_table = Table(
        ranking_data,
        colWidths=[
            12 * mm,
            35 * mm,
            27 * mm,
            32 * mm,
            22 * mm,
            38 * mm,
        ],
        repeatRows=1,
    )

    ranking_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#333333"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (0, -1),
                    "CENTER",
                ),
                (
                    "ALIGN",
                    (2, 1),
                    (4, -1),
                    "CENTER",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    story.append(ranking_table)

    # ==================================================
    # DETAILED CANDIDATE REPORTS
    # ==================================================

    for candidate in results:

        story.append(
            PageBreak()
        )

        story.append(
            Paragraph(
                f"Rank #{candidate['rank']}: "
                f"{escape(str(candidate['candidate_name']))}",
                candidate_heading_style,
            )
        )

        story.append(
            Paragraph(
                f"<b>Resume:</b> "
                f"{escape(str(candidate.get('resume_file', 'N/A')))}",
                body_style,
            )
        )

        story.append(
            Paragraph(
                f"<b>Recommendation:</b> "
                f"{escape(str(candidate.get('recommendation', 'N/A')))}",
                body_style,
            )
        )

        story.append(
            Spacer(1, 6)
        )

        # ------------------------------------------
        # Score table
        # ------------------------------------------

        score_data = [
            [
                "Metric",
                "Score",
                "Weight",
                "Contribution",
            ],
            [
                "Skill Match",
                f"{candidate['skill_match_score']:.2f}%",
                f"{candidate.get('skill_weight', 0.70) * 100:.0f}%",
                f"{candidate.get('skill_contribution', 0):.2f}",
            ],
            [
                "Text Similarity",
                f"{candidate['text_similarity_score']:.2f}%",
                f"{candidate.get('text_weight', 0.30) * 100:.0f}%",
                f"{candidate.get('text_contribution', 0):.2f}",
            ],
            [
                "Overall Score",
                f"{candidate['overall_score']:.2f}%",
                "-",
                "-",
            ],
        ]

        score_table = Table(
            score_data,
            colWidths=[
                42 * mm,
                35 * mm,
                30 * mm,
                35 * mm,
            ],
        )

        score_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#333333"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "FONTNAME",
                        (0, -1),
                        (-1, -1),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "ALIGN",
                        (1, 1),
                        (-1, -1),
                        "CENTER",
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        story.append(score_table)

        # ------------------------------------------
        # Candidate insights
        # ------------------------------------------

        story.append(
            Paragraph(
                "Why This Candidate?",
                heading_style,
            )
        )

        candidate_insights = candidate.get(
            "candidate_insights",
            [],
        )

        if candidate_insights:

            for insight in candidate_insights:

                story.append(
                    Paragraph(
                        f"• {escape(str(insight))}",
                        insight_style,
                    )
                )

        else:

            story.append(
                Paragraph(
                    "No additional insights available.",
                    small_style,
                )
            )

        # ------------------------------------------
        # Matched skills
        # ------------------------------------------

        story.append(
            Paragraph(
                "Matched Skills",
                heading_style,
            )
        )

        matched_skills = candidate.get(
            "matched_skills",
            [],
        )

        if matched_skills:

            matched_text = ", ".join(
                escape(str(skill))
                for skill in matched_skills
            )

            story.append(
                Paragraph(
                    matched_text,
                    small_style,
                )
            )

        else:

            story.append(
                Paragraph(
                    "None",
                    small_style,
                )
            )

        # ------------------------------------------
        # Missing skills
        # ------------------------------------------

        story.append(
            Paragraph(
                "Missing Skills",
                heading_style,
            )
        )

        missing_skills = candidate.get(
            "missing_skills",
            [],
        )

        if missing_skills:

            missing_text = ", ".join(
                escape(str(skill))
                for skill in missing_skills
            )

            story.append(
                Paragraph(
                    missing_text,
                    small_style,
                )
            )

        else:

            story.append(
                Paragraph(
                    "None",
                    small_style,
                )
            )

    # ==================================================
    # BUILD PDF
    # ==================================================

    document.build(story)

    output.seek(0)

    return output