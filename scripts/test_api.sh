#!/bin/bash
#
# Simple E2E test script for the SpeechHub API.
#
# Usage:
# 1. Make sure the server is running (e.g., via `docker-compose up`).
# 2. (Optional) Place a sample audio file at `storage/processed/audio/sample.m4a`.
# 3. Run this script from the project root: `bash scripts/test_api.sh`
#

set -e

# --- Configuration ---
API_BASE_URL="http://localhost:8000"
# The user needs to provide a sample file with this exact name for the ingest test to work.
SAMPLE_AUDIO_FILENAME="sample.m4a"
SAMPLE_AUDIO_FILE_PATH="storage/processed/audio/$SAMPLE_AUDIO_FILENAME"
SEARCH_KEYWORD="test" # A keyword to search for after ingestion

# --- Helper Functions ---
function print_header() {
    echo ""
    echo "================================================="
    echo "  $1"
    echo "================================================="
}

function check_server() {
    print_header "Checking if server is running at $API_BASE_URL"
    if curl -s -f "$API_BASE_URL/api/health" > /dev/null; then
        echo "✅ Server is running."
    else
        echo "❌ Server is not running. Please start it first (e.g., with 'docker-compose up')."
        exit 1
    fi
}

# --- Main Test Logic ---
check_server

# 1. Test Ingest API
print_header "1. Testing Audio Ingest API (POST /api/ingest/audio)"
if [ ! -f "$SAMPLE_AUDIO_FILE_PATH" ]; then
    echo "⚠️  Sample audio file not found at '$SAMPLE_AUDIO_FILE_PATH'."
    echo "    Skipping ingest test. To run this test, please add a sample file with that name."
else
    echo "Found sample audio file. Uploading..."
    response=$(curl -s -X POST "$API_BASE_URL/api/ingest/audio" -F "file=@$SAMPLE_AUDIO_FILE_PATH")
    echo "    Response: $response"
    if echo "$response" | grep -q '"status":"ok"'; then
        echo "✅ Ingest API test PASSED."
    else
        echo "❌ Ingest API test FAILED."
        exit 1
    fi
fi

# 2. Test Search API
print_header "2. Testing Search API (POST /api/search)"
echo "Searching for keyword: '$SEARCH_KEYWORD'"
response=$(curl -s -X POST "$API_BASE_URL/api/search" -H "Content-Type: application/json" -d "{\"q\":\"$SEARCH_KEYWORD\",\"top\":1}")
echo "    Response: $response"
# A simple check to see if the 'hits' array is present
if echo "$response" | grep -q '"hits":'; then
    echo "✅ Search API test PASSED."
else
    echo "❌ Search API test FAILED."
    exit 1
fi

# 3. Test Audio File API
print_header "3. Testing Audio File API (GET /api/audio/{filename})"
if [ ! -f "$SAMPLE_AUDIO_FILE_PATH" ]; then
    echo "⚠️  Sample audio file not found. Skipping audio file API test."
else
    echo "Attempting to fetch audio file headers for: $SAMPLE_AUDIO_FILENAME"
    # We use -I to get headers only, to confirm the file can be served, without downloading it.
    response_code=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE_URL/api/audio/$SAMPLE_AUDIO_FILENAME")
    echo "    HTTP Response Code: $response_code"
    if [ "$response_code" -eq 200 ]; then
        echo "✅ Audio File API test PASSED."
    else
        echo "❌ Audio File API test FAILED."
        exit 1
    fi
fi

print_header "All available tests passed successfully!"
