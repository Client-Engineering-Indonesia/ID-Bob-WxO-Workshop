# Building a watsonx Orchestrate Financial Intelligence Agent

## Overview
This document provides instructions for creating a watsonx Orchestrate agent that scrapes financial news with sentiment analysis. Students will use an existing Yahoo Finance agent as a reference to build a News Scraper agent.

---

## Project Goal
Build an AI agent on IBM watsonx Orchestrate that:
1. Scrapes financial news from Yahoo Finance
2. Performs VADER sentiment analysis
3. Filters news by stock ticker
4. Provides market sentiment insights

---

## Reference Agent Structure

Students have access to `yahoo-finance-agent.yaml` as a reference. This agent demonstrates:
- Proper YAML structure for watsonx Orchestrate
- How to define agent behavior and instructions
- Tool integration patterns
- Error handling approaches

**Key sections in the reference agent:**
- `spec_version`: Always use `v1`
- `kind`: Always use `native`
- `name`: Unique agent identifier (snake_case)
- `description`: Clear explanation of agent capabilities
- `instructions`: Detailed behavior guidelines
- `llm`: Model specification
- `tools`: List of tool functions the agent can use

---

## Step-by-Step Build Instructions

### Phase 1: Project Setup

The project structure is already set up:
```
Lab 2 - Materials/
├── agents/
│   └── yahoo-finance-agent.yaml (reference)
├── tools/
│   └── yahoo_finance.py (reference)
├── requirements.txt (dependencies)
├── env.example (environment template)
└── BOB_INSTRUCTIONS.md (this file)
```

**Note:** `requirements.txt` already contains all necessary dependencies. Do NOT include `ibm-watsonx-orchestrate` - it causes conflicts in cloud runtime.

---

### Phase 2: Build Python Tool

#### Step 2.1: Create News Scraper Tool
**File:** `tools/news_scraper_tool.py`

**Key Requirements:**
- Import: `from ibm_watsonx_orchestrate.agent_builder.tools import tool`
- Use `@tool` decorator for the function
- Function name: `scrape_financial_news`
- Implement VADER sentiment analysis
- Handle ticker filtering intelligently

**Critical Implementation Details:**
```python
@tool
def scrape_financial_news(ticker: str = "", max_articles: int = 10) -> str:
    """
    Scrape financial news with sentiment analysis.
    
    Args:
        ticker: Optional ticker to filter (e.g., 'TSLA')
        max_articles: Maximum articles to return
    
    Returns:
        Formatted string with news and sentiment
    """
    # Implementation:
    # 1. Scrape general Yahoo Finance news page
    # 2. If ticker provided, filter articles mentioning it
    # 3. Use VADER for sentiment analysis
    # 4. Format with sentiment scores
    # 5. Calculate overall sentiment distribution
```

**Critical Fix for Ticker-Specific News:**
```python
# Use general news page, not ticker-specific URLs
url = "https://finance.yahoo.com/news/"

# Filter articles by ticker mention
if ticker and ticker.upper() not in title.upper():
    if ticker.upper() not in summary_text.upper():
        continue  # Skip non-relevant articles
```

**Error Handling:**
```python
except requests.exceptions.RequestException as e:
    logger.error(f"Error fetching Yahoo Finance news: {str(e)}")
    return f"Error fetching news: {str(e)}. Please try again later."
```

---

### Phase 3: Create Agent YAML Specification

#### Step 3.1: Study the Reference Agent
**File:** `yahoo-finance-agent.yaml` (provided)

Review these key elements:
1. **spec_version and kind**: Standard headers
2. **name and description**: Clear identification
3. **instructions section**: Detailed behavior guidelines including:
   - Behavior and sources
   - Reasoning and brevity controls
   - Formatting rules
   - Error handling
   - Workflow steps
4. **llm**: Model specification (`groq/openai/gpt-oss-120b`)
5. **tools**: List of available functions

#### Step 3.2: Create News Scraper Agent
**File:** `agents/news-scraper-agent.yaml`

**Task:** Create this file based on the reference `yahoo-finance-agent.yaml` structure.

**Required elements:**
```yaml
spec_version: v1
kind: native
name: news_scraper_agent
description: [Your description of news scraping capabilities]

instructions: |
  Behavior and sources:
  - [Define how agent should behave]
  
  Reasoning and brevity controls:
  - [Define response style]
  
  Error handling:
  - [Define error responses]
  
  News analysis workflow:
  1. [Step-by-step process]
  2. IMPORTANT: When user asks for ticker-specific news:
     - Call scrape_financial_news with ticker="TSLA"
     - DO NOT call with empty ticker (ticker="")
  
  Tool usage examples:
  - Ticker-specific: scrape_financial_news(ticker="TSLA", max_articles=10)
  - General market: scrape_financial_news(ticker="", max_articles=10)

llm: groq/openai/gpt-oss-120b
style: default
collaborators: []

tools:
  - scrape_financial_news
```

**Critical Points:**
- MUST include explicit ticker parameter instructions
- Provide tool usage examples
- This prevents circular behavior bugs
- Tool name must match Python function name exactly

---

### Phase 4: Deployment to watsonx Orchestrate

#### Step 4.1: Setup Environment
```bash
# Navigate to project directory
cd "ID-Bob-WxO-Workshop/Lab 2 - Materials"

# Set API key (if not already set)
export WXO_API_KEY="your_api_key_here"

# Add environment (if not already added)
orchestrate env add -n production \
  -u https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/YOUR_INSTANCE_ID \
  -a

# Activate environment
orchestrate env activate production
```

#### Step 4.2: Import Tools with Dependencies
```bash
# Import Yahoo Finance tools (reference - already done)
orchestrate tools import -k python \
  -f tools/yahoo_finance.py \
  -r requirements.txt

# Import News Scraper tool
orchestrate tools import -k python \
  -f tools/news_scraper_tool.py \
  -r requirements.txt
```

**Critical Notes:**
- MUST use `-r requirements.txt` flag
- This installs dependencies in cloud runtime
- Wait for "Tool imported successfully" message
- All commands run from "ID-Bob-WxO-Workshop/Lab 2 - Materials" directory
- Only scrape_financial_news will be deployed (Yahoo Finance)

#### Step 4.3: Import Agents
```bash
# Import Yahoo Finance agent (reference - already done)
orchestrate agents import -f agents/yahoo-finance-agent.yaml

# Import News Scraper agent
orchestrate agents import -f agents/news-scraper-agent.yaml
```

**Critical Notes:**
- Wait for "Agent imported successfully" message
- Verify agent name matches YAML specification

#### Step 4.4: Verify Deployment
```bash
# List all agents
orchestrate agents list

# List all tools
orchestrate tools list
```

**Expected Output:**
```
Agents:
- yahoo_finance_agent
- news_scraper_agent

Tools:
- get_formatted_stock_data
- get_stock_comparison
- scrape_financial_news
```

---

### Phase 5: Testing & Validation

#### Test Case 1: General Financial News
**Query:** "Show me recent financial news sentiment"

**Expected:**
- Returns 8-10 articles
- Includes sentiment scores and distribution
- Shows overall market sentiment

#### Test Case 2: Ticker-Specific News
**Query:** "Get news and sentiment for Tesla stock"

**Expected:**
- Returns Tesla-filtered news articles
- Includes sentiment analysis
- MUST NOT return general news with empty ticker

#### Test Case 3: Sentiment Analysis
**Query:** "What's the market sentiment today?"

**Expected:**
- Overall sentiment summary
- Distribution of positive/negative/neutral articles
- Confidence scores

---

## Common Issues & Solutions

### Issue 1: ModuleNotFoundError for bs4/vaderSentiment
**Symptom:** `ModuleNotFoundError: No module named 'vaderSentiment'`

**Solution:**
```bash
# Re-import tool with requirements file from Lab 2 - Materials directory
cd "ID-Bob-WxO-Workshop/Lab 2 - Materials"
orchestrate tools import -k python \
  -f tools/news_scraper_tool.py \
  -r requirements.txt
```

### Issue 2: Ticker-Specific News Returns General News
**Symptom:** Agent calls `scrape_financial_news(ticker="")` instead of `ticker="TSLA"`

**Solution:**
- Add explicit instructions in news-scraper-agent.yaml
- Include tool usage examples
- Agent must understand when to pass ticker parameter

### Issue 3: Network Errors
**Symptom:** `Error fetching news: Connection timeout` or similar network errors

**Solution:**
- Check internet connectivity
- Retry the request
- Yahoo Finance may be temporarily unavailable
- Wait a few moments and try again

---

## Success Criteria

Your implementation is complete when:

1. Tool deployed to watsonx Orchestrate with dependencies
2. Agent deployed successfully
3. All 3 test cases passing
4. Ticker-specific news filtering working correctly
5. Error handling graceful for all failure modes
6. Agent follows reference structure from yahoo-finance-agent.yaml

---

## Quick Start Command Sequence

```bash
# 1. Navigate to project
cd "ID-Bob-WxO-Workshop/Lab 2 - Materials"

# 2. Create News Scraper files
# - tools/news_scraper_tool.py
# - agents/news-scraper-agent.yaml

# 3. Deploy
export WXO_API_KEY="your_key"
orchestrate env activate production
orchestrate tools import -k python -f tools/news_scraper_tool.py -r requirements.txt
orchestrate agents import -f agents/news-scraper-agent.yaml

# 4. Verify
orchestrate agents list
orchestrate tools list
```

---

## Key Learnings & Best Practices

### 1. Tool Development
- Always use `@tool` decorator from IBM ADK
- Return formatted strings, not JSON objects
- Handle edge cases (empty data, errors)
- Provide helpful error messages

### 2. Agent Configuration
- Study reference agent structure carefully
- Keep instructions concise but explicit
- Provide tool usage examples
- Include error handling guidance

### 3. Deployment
- Use requirements.txt (no IBM packages)
- Import tools with `-r requirements.txt` flag for dependencies
- All commands run from "ID-Bob-WxO-Workshop/Lab 2 - Materials" directory
- Verify each step before proceeding

### 4. Testing
- Test with general queries first
- Test ticker-specific filtering
- Test error scenarios
- Validate sentiment analysis output
