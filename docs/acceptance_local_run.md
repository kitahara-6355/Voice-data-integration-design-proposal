# Acceptance Test Procedures for Local Windows Run

This document outlines the steps to verify that the application is running correctly in a local, non-Docker environment.

## Prerequisites

1.  The local environment has been set up using `scripts/setup_windows_env.ps1`.
2.  The application has been started using `.\run_local.ps1`.
3.  A sample audio file (e.g., `sample.m4a`) has been placed in the `storage/processed/audio/` directory.

## Test Cases

### 1. Health Check

-   **Action:** Open a new PowerShell terminal.
-   **Command:** `curl http://localhost:8000/api/health`
-   **Expected Result:** The command should return `{"status":"ok"}`.

### 2. Frontend Accessibility

-   **Action:** Open a web browser.
-   **URL:** `http://localhost:3000`
-   **Expected Result:** The "会議検索 (SpeechHub)" web page should load correctly.

### 3. Audio Ingestion

-   **Action:** In a PowerShell terminal, run the following command (replace `sample.m4a` with your actual file name).
-   **Command:**
    ```bash
    curl -X POST "http://localhost:8000/api/ingest/audio" -F "file=@storage/processed/audio/sample.m4a"
    ```
-   **Expected Result:** A JSON response containing `"status":"ok"` and `"segments_found"` with a number greater than 0.

### 4. Search Functionality

-   **Action:** In a PowerShell terminal, run the following command.
-   **Command:**
    ```bash
    curl -X POST "http://localhost:8000/api/search" -H "Content-Type: application/json" -d '{"q":"test","top":1}'
    ```
-   **Expected Result:** A JSON response containing a `"hits"` array. The array may be empty if no relevant text was found, but the key must exist.

### 5. Audio File Serving

-   **Action:** In a web browser, navigate to the following URL (replace `sample.m4a` with your file name).
-   **URL:** `http://localhost:8000/api/audio/sample.m4a`
-   **Expected Result:** The browser should show an audio player and be able to play the audio file.
