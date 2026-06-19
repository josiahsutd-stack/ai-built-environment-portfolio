# Retrieval Evaluation Report

Singapore public-source evaluation for the AEC Code Compliance RAG Assistant.

## Summary

- Cases: 11
- Answerable retrieval cases: 10
- Top-k: 4
- Recall@k: 1.0
- Precision@k: 0.85
- Hit rate: 1.0
- Mean reciprocal rank: 1.0
- Section hit rate: 1.0
- Citation coverage: 1.0
- Grounding check rate: 1.0
- Status accuracy: 1.0
- Citation check pass rate: 1.0
- Answer sentence support rate: 1.0
- Unsupported answer sentence rate: 0.0
- Hit@1: 1.0
- Hit@3: 1.0
- Average latency ms: 28.45
- No-answer accuracy: None
- Unsupported-scope accuracy: 1.0

## Per-Question Results

| Question | Expected status | Actual status | Expected section | Retrieved chunks | Recall@k | MRR | Grounding/no-answer check | Missing terms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| What does the BCA Code on Accessibility 2025 set out for accessible and inclusive buildings? | answered | answered | None | bca_code_on_accessibility_2025-code-on-accessibility-in-the-built-environment-2025-p9-000, bca_code_on_accessibility_2025-8-i-n-t-r-o-d-u-c-t-i-o-n-p8-000, nea_code_of_practice_environmental_health_2025-code-of-practice-on-environmental-health-2025-edition-p38-002, nea_code_of_practice_environmental_health_2025-code-of-practice-on-environmental-health-2025-edition-p17-004 | 1.0 | 1.0 | True | None |
| Who does BCA say should integrate accessibility and usability considerations from the onset of a building project? | answered | answered | None | bca_code_on_accessibility_2025-8-i-n-t-r-o-d-u-c-t-i-o-n-p8-001, bca_code_on_accessibility_2025-8-i-n-t-r-o-d-u-c-t-i-o-n-p8-000, bca_green_mark_2021_certification_standard_2nd_ed-page-12-of-33-p12-000, bca_green_mark_2021_certification_standard_2nd_ed-page-11-of-33-p11-002 | 1.0 | 1.0 | True | None |
| What does the BCA Approved Document provide for prescribed objectives and performance requirements? | answered | answered | None | bca_approved_document_v7_07-building-and-construction-authority-page-1-of-65-p24-001, bca_approved_document_v7_07-building-and-construction-authority-page-1-of-65-p24-000, bca_approved_document_v7_07-building-and-construction-authority-page-1-of-65-p24-002, bca_approved_document_v7_07-building-and-construction-authority-page-2-of-65-p25-000 | 1.0 | 1.0 | True | None |
| Which BCA document contains the Green Mark 2021 certification standard? | answered | answered | None | bca_green_mark_2021_certification_standard_2nd_ed-page-10-of-33-p10-003, bca_green_mark_2021_certification_standard_2nd_ed-page-10-of-33-p10-002, bca_green_mark_2021_certification_standard_2nd_ed-page-2-of-33-p2-000, bca_green_mark_2021_certification_standard_2nd_ed-page-3-of-33-p3-000 | 1.0 | 1.0 | True | None |
| What is the SCDF Fire Code 2023 used for in Singapore building fire safety design? | answered | answered | None | scdf_fire_code_2023-amendment-history-chapter-3-structural-fire-precautions-p109-005, scdf_fire_code_2023-clause-11-3-assessment-and-validation-p253-004, scdf_fire_code_2023-amendment-history-chapter-1-general-p31-000, scdf_fire_code_2023-code-of-practice-for-fire-p1-000 | 1.0 | 1.0 | True | None |
| Can this assistant certify a Singapore building plan for BCA approval? | needs_professional_review | needs_professional_review | None |  | 0.0 | 0.0 | True | None |
| What does URA say the Gross Floor Area handbook advisory notes are not exhaustive about? | answered | answered | None | ura_gfa_handbook_advisory_notes-ura-gross-floor-area-handbook-advisory-notes-006, ura_gfa_handbook_advisory_notes-ura-gfa-handbook-advisory-notes-000, ura_gfa_handbook_advisory_notes-advisory-notes-000, ura_gfa_handbook_advisory_notes-ura-gross-floor-area-handbook-advisory-notes-000 | 1.0 | 1.0 | True | None |
| Which URA GFA glance source lists items excluded, partially excluded, included, and over Master Plan control? | answered | answered | None | ura_gfa_guidelines_at_a_glance-guidelines-at-a-glance-gross-floor-area-p1-000, ura_gfa_guidelines_at_a_glance-items-excluded-from-p3-000, ura_gfa_guidelines_at_a_glance-items-excluded-from-p2-000, ura_gfa_handbook_advisory_notes-ura-gross-floor-area-handbook-advisory-notes-000 | 1.0 | 1.0 | True | None |
| What does NEA COPEH say residential buildings taller than four storeys need for refuse? | answered | answered | None | nea_code_of_practice_environmental_health_2025-code-of-practice-on-environmental-health-2025-edition-p7-002, nea_code_of_practice_environmental_health_2025-code-of-practice-on-environmental-health-2025-edition-p33-003, nea_code_of_practice_environmental_health_2025-code-of-practice-on-environmental-health-2025-edition-p11-004, nea_code_of_practice_environmental_health_2025-code-of-practice-on-environmental-health-2025-edition-p8-001 | 1.0 | 1.0 | True | None |
| What does the LTA works on public streets code set out for permits and technical requirements? | answered | answered | None | lta_code_of_practice_works_on_public_streets_2025-code-of-practice-for-works-on-public-streets-12-p12-001, lta_code_of_practice_works_on_public_streets_2025-code-of-practice-for-works-on-public-streets-7-p7-001, lta_code_of_practice_works_on_public_streets_2025-code-of-practice-for-works-on-public-streets-40-p40-000, lta_code_of_practice_works_on_public_streets_2025-code-of-practice-for-works-on-public-streets-77-p77-000 | 1.0 | 1.0 | True | None |
| What does the LTA railway protection code cover for development and building proposals? | answered | answered | None | lta_code_of_practice_railway_protection_2024-21-p-a-g-e-p22-000, lta_code_of_practice_works_on_public_streets_2025-code-of-practice-for-works-on-public-streets-38-p38-001, lta_code_of_practice_railway_protection_2024-64-p-a-g-e-p65-000, lta_code_of_practice_railway_protection_2024-2024-edition-p1-000 | 1.0 | 1.0 | True | None |
