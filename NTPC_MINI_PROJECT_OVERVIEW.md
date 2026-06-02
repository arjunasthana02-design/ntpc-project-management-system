# NTPC AI Assisted Engineering Drawing Review & Progress Monitoring System

## Project Summary

The NTPC AI Assisted Engineering Drawing Review & Progress Monitoring System is a full-stack enterprise web application for digitizing vendor drawing review, DPR progress tracking, AI-assisted compliance analysis, and project-level analytics for large infrastructure projects.

The system supports Prime Admin, Admin, and Vendor workflows. Vendors upload engineering drawings and DPR progress reports, admins review submissions, and prime administrators control governance approvals. The application maintains centralized Pending, Approved, and Rejected repositories with deletion control, audit-friendly record tracking, and role-based access flow.

## Core Modules

### 1. User and Vendor Management

- Prime Admin approval workflow for administrators
- Admin and Vendor login paths
- Vendor upload dashboard
- Pending, Approved, and Rejected drawing repositories
- Primary-key based delete actions with server file cleanup

### 2. AI Assisted Drawing Review

- Extracts drawing text from uploaded PDFs
- Compares submission content against NTPC rule datasets
- Categorizes observations across engineering, layout, foundation, electrical, structural, and safety areas
- Calculates compliance and vendor accuracy metrics
- Generates senior-review-style approval recommendations
- Provides detailed clause-level analysis for each observation

### 3. DPR Progress Monitoring

- Processes vendor DPR Excel files
- Extracts activity name, vendor, scope, progress, completion percentage, and DPR date
- Stores persistent analytics in `running_progress_metrics`
- Builds DPR date-wise progress trend charts
- Builds top activity completion charts
- Calculates average yield benchmark and OK/0 status
- Preserves activity/vendor/date context for management reporting

### 4. AI Learning Centre

- Uploads PDF, DOCX, Excel, TXT, and CSV knowledge files
- Extracts technical text and tabular content
- Stores learned knowledge in `ai_learning`
- Provides knowledge statistics, learned document register, and search
- Supports learned-reference lookup during AI drawing review

## Business Value

- Reduces manual review effort
- Improves consistency of NTPC engineering compliance checks
- Tracks vendor performance against DPR progress benchmarks
- Provides management-level progress analytics
- Creates a foundation for a continuously learning engineering review ecosystem

## Future Enhancement Roadmap

- Vector embeddings for semantic search over learned documents
- Approved drawing similarity comparison
- Automatic recurring vendor mistake detection
- Review comment generation from learned NTPC standards
- Dashboard exports for management review
- Full audit logging for every approval, rejection, deletion, and learning event
