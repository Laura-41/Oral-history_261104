#!/usr/bin/env python3
"""Manually reviewed person-level biography overlay for the six workflow-demo documents.

The document-level EventNode and NEXT chains remain untouched.  A LifeEpisode may
later cite more than one EventNode when the same life experience is retold in
multiple interviews.
"""

from __future__ import annotations


SUBJECTS = {
    "PER-CHF": {
        "person_name": "陈海峰",
        "documents": ["CHF-V1-01", "CHF-V2-01", "CHF-V3-01"],
        "episodes": [
            ("CHF-L01", "CHF-V1-E01", "PERSONAL_EXPERIENCE"),
            ("CHF-L02", "CHF-V1-E03", "PERSONAL_EXPERIENCE"),
            ("CHF-L03", "CHF-V1-E02", "PERSONAL_EXPERIENCE"),
            ("CHF-L04", "CHF-V1-E04", "PERSONAL_EXPERIENCE"),
            ("CHF-L05", "CHF-V1-E05", "PERSONAL_EXPERIENCE"),
            ("CHF-L06", "CHF-V1-E06", "PERSONAL_EXPERIENCE"),
            ("CHF-L07", "CHF-V1-E07", "PERSONAL_EXPERIENCE"),
            ("CHF-L08", "CHF-V2-E01", "PERSONAL_EXPERIENCE"),
            ("CHF-L09", "CHF-V2-E02", "PERSONAL_EXPERIENCE"),
            ("CHF-L10", "CHF-V2-E03", "PERSONAL_EXPERIENCE"),
            ("CHF-L11", "CHF-V2-E04", "PERSONAL_EXPERIENCE"),
            ("CHF-L12", "CHF-V2-E05", "PERSONAL_EXPERIENCE"),
            ("CHF-L13", "CHF-V2-E06", "PERSONAL_EXPERIENCE"),
        ],
        # These are events narrated by Chen Haifeng, but the present evidence
        # supports collective history rather than a direct personal life episode.
        "narrated_context": [
            "CHF-V3-E01", "CHF-V3-E02", "CHF-V3-E03", "CHF-V3-E04", "CHF-V3-E05"
        ],
    },
    "PER-CRT": {
        "person_name": "陈锐霆",
        "documents": ["CRT-01", "CRT-02"],
        "episodes": [
            ("CRT-L01", "CRT-E01", "PERSONAL_EXPERIENCE"),
            ("CRT-L02", "CRT-E02", "PERSONAL_EXPERIENCE"),
            ("CRT-L03", "CRT-E03", "PERSONAL_EXPERIENCE"),
            ("CRT-L04", "CRT-E04", "PERSONAL_EXPERIENCE"),
            ("CRT-L05", "CRT-E05", "PERSONAL_EXPERIENCE"),
            ("CRT-L06", "CRT-E06", "PERSONAL_EXPERIENCE"),
            ("CRT-L07", "CRT-E07", "PERSONAL_EXPERIENCE"),
            ("CRT-L08", "CRT-E08", "PERSONAL_EXPERIENCE"),
            ("CRT-L09", "CRT-E09", "PERSONAL_EXPERIENCE"),
            ("CRT-L10", "CRT-E10", "PERSONAL_EXPERIENCE"),
            ("CRT-L11", "CRT-02-E01", "PERSONAL_EXPERIENCE"),
            ("CRT-L12", "CRT-02-E05", "PERSONAL_EXPERIENCE"),
            ("CRT-L13", "CRT-02-E02", "PERSONAL_EXPERIENCE"),
            ("CRT-L14", "CRT-02-E03", "PERSONAL_EXPERIENCE"),
            ("CRT-L15", "CRT-02-E04", "PERSONAL_EXPERIENCE"),
        ],
        "narrated_context": [],
    },
    "PER-YYS": {
        "person_name": "杨永松",
        "documents": ["YYS-01"],
        "episodes": [
            ("YYS-L01", "YYS-E01", "COLLECTIVE_EXPERIENCE"),
            ("YYS-L02", "YYS-E02", "COLLECTIVE_EXPERIENCE"),
            ("YYS-L03", "YYS-E03", "PERSONAL_EXPERIENCE"),
            ("YYS-L04", "YYS-E04", "PERSONAL_EXPERIENCE"),
            ("YYS-L05", "YYS-E05", "COLLECTIVE_EXPERIENCE"),
            ("YYS-L06", "YYS-E06", "PERSONAL_EXPERIENCE"),
            ("YYS-L07", "YYS-E07", "PERSONAL_EXPERIENCE"),
        ],
        "narrated_context": [],
    },
}

