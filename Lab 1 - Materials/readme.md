# Lab 1: Building an OCR AI Agent for ID Cards and Receipts

## Overview

In this lab, you will learn how to create an AI agent that can automatically classify and extract information from documents using Optical Character Recognition (OCR). The agent will be able to:

- **Classify documents** into two categories: KTP (Indonesian ID Cards) and Receipts
- **Extract structured data** from both document types
- **Return formatted results** based on the document type

**Prerequisites:**
- Access to watsonx Orchestrate instance
- Sample documents provided in the `KTP/` and `Invoice/` folders

---

## What You'll Build

An intelligent OCR agent that:
1. Accepts document uploads (images or PDFs)
2. Automatically classifies the document type
3. Extracts relevant information based on the document type
4. Returns structured data in a user-friendly format

---

## Step 1: Access watsonx Orchestrate

1. Open your web browser and navigate to your watsonx Orchestrate instance
2. Log in with your credentials

![watsonx Orchestrate Main Page](readme-asset/step01-wxo-main-page.png)

You should see the main dashboard with various options for building AI agents and tools.

---

## Step 2: Navigate to the Build Page

1. Look at the **left sidebar**
2. Click on the **"Build"** option

![Navigate to Build Page](readme-asset/step02-navigate-to-build-page.png)

This will take you to the agent creation interface where you can build and manage your AI agents.

---

## Step 3: Create a New Agent

1. On the Build page, click the **"Create agent"** button

![Create Agent Button](readme-asset/step03-create-agent-button.png)

2. Select **"Create from scratch"**
3. Fill in the agent details:
   - **Name:** `ID&ReceiptOCR`
   - **Description:** `An AI agent to extracts and structures data from Indonesia National IDs and receipts`
4. Click **"Create"**

![Create Agent Form](readme-asset/step03-create-agent-form.png)

---

## Step 4: Add an Agentic Workflow Tool

Now we'll add the OCR processing capability to our agent.

1. In the agent page, click **"Toolset"** in the sidebar
2. Click **"Add tool"**

![Add Tool](readme-asset/step04-add-tool-button.png)

3. Select **"Agentic workflow"** tool

![Select Agentic Workflow](readme-asset/step04-select-agentic-workflow.png)

4. Give your workflow a name (e.g., `ID & Receipts OCR Workflow`)
5. Click **"Start building"**

![Name Workflow](readme-asset/step04-name-workflow.png)

---

## Step 5: Build the Workflow - Add File Upload

The workflow builder will open. Now we'll create the processing pipeline.

1. In the first step, add a **"File upload"** component

![Add File Upload](readme-asset/step05-add-file-upload.png)

This allows users to upload documents (KTP or receipts) to the agent.

---

## Step 6: Add Document Classifier

1. **Hover over the line** below the File Upload step
2. Click the **"+"** (add) button that appears
3. Select **"Document classifier"**

![Add Document Classifier](readme-asset/step06-add-document-classifier.png)

The Document Classifier will automatically determine whether the uploaded document is a KTP or a Receipt.

---

## Step 7: Add Branch Flow Control

1. Under the Document Classifier, add a **"Branch"** flow control

![Add Branch](readme-asset/step07-add-branch-control.png)

The Branch creates two separate paths based on the classification result - one for KTP and one for Receipts.

---

## Step 8: Add Document Extractors to Both Paths

1. For **both paths** (Path 1 and Path 2), add a **"Document extractor"** component

![Add Document Extractors](readme-asset/step08-add-document-extractors.png)

2. Your workflow should now look like this:

![Complete Flow Structure](readme-asset/step08-complete-flow-structure.png)

Now we have the complete structure. Let's configure each component!

---

## Step 9: Configure Document Classifier

1. Click on the **Document Classifier** step
2. Click **"Add classes"**

![Configure Document Classifier](readme-asset/step09-configure-classifier.png)

3. Add two classes:
   - `KTP`
   - `Receipts`

![Add Classes](readme-asset/step09-add-classes.png)

These are the two document types our agent will recognize.

---

## Step 10: Configure Branch Conditions

Now we need to set up the conditions for each path.

### Configure Path 1 (for KTP):

1. Click on the **Branch** component
2. Click **"Edit"** on Path 1 condition

![Edit Path 1](readme-asset/step10-edit-path1-condition.png)

3. Click on **"Document classifier"** and select the `class_name` value

![Select class_name](readme-asset/step10-select-class-name.png)

4. Click the **"=="** operator
5. Fill in the value with `KTP`

![Set KTP Condition](readme-asset/step10-set-ktp-condition.png)

![KTP Condition Complete](readme-asset/step10-ktp-condition-complete.png)

This ensures Path 1 only executes when the document is classified as KTP.

### Configure Path 2 (Else - for Receipts):

**Path 2 is automatically configured as the "else" path.** This means:
- If the document is **NOT** classified as KTP, it will automatically go to Path 2
- Since we only have two document types (KTP and Receipts), any document that isn't a KTP will be treated as a Receipt
- **No additional condition configuration is needed for Path 2** - it acts as the default/fallback path

This is a common pattern in branching logic:
- **Path 1:** Specific condition (class_name == "KTP")
- **Path 2:** Everything else (automatically handles Receipts)

---

## Step 11: Configure Path 1 Document Extractor (KTP)

1. Click on **Path 1's Document Extractor**
2. Select **"Structured"** extraction type

![Select Structured](readme-asset/step11-select-structured-extraction.png)

3. **Drag and drop** the sample KTP files:
   - `KTP_1.jpg`
   - `KTP_2.jpg`
   - `KTP_3.jpg`

![Upload KTP Samples](readme-asset/step11-upload-ktp-samples.png)

4. Click **"Define schema"**

![Define Schema](readme-asset/step11-define-schema.png)

5. Select **"National ID Card"** from the pre-built schemas
6. Click **"Create"**

![Select National ID Card](readme-asset/step11-select-national-id-schema.png)

7. The system will **automatically map** the fields from the KTP documents

![Auto-mapped Fields](readme-asset/step11-auto-mapped-fields.png)

Great! The KTP extractor is now configured to extract standard ID card information like name, ID number, address, etc.

---

## Step 12: Configure Path 2 Document Extractor (Receipts)

Now let's configure the receipt extraction.

1. Click on **Path 2's Document Extractor**
2. Select **"Structured"** extraction type

![Select Structured for Path 2](readme-asset/step12-path2-select-structured.png)

3. **Upload** the sample invoice files:
   - `invoice_1.jpg`
   - `invoice_2.jpg`
   - `invoice_3.jpg`
4. Click **"Define schema"**

![Upload Invoices](readme-asset/step12-upload-invoices.png)

5. Select **"User defined schema"** (since receipts vary more than ID cards)
6. Click **"Create"**

![User Defined Schema](readme-asset/step12-user-defined-schema.png)

---

## Step 13: Define Receipt Fields

1. Click **"Add field"**

![Add Field](readme-asset/step13-add-field.png)

2. Add the following fields:
   - `TotalPurchase` (for the total amount)
   - `Date` (for the transaction date)

![Add Fields](readme-asset/step13-add-receipt-fields.png)

The system will learn to extract these specific fields from receipts based on the sample documents you provided.

---

## Step 14: Configure Agent Behavior

Now let's go back to the main agent page and set up how the agent should interact with users.

1. Navigate back to the **main agent page**
2. Find the **"Behavior"** or **"Instructions"** section
3. Fill in the behavior instructions:

```
If the user intent involves receipt processing, expense capture, or OCR, immediately call the 'ocr receipts' tool as the first action. Do not ask for files, clarification, or confirmation. Assume file handling is managed within the tool. Respond only based on the tool's output or next system step
```

![Configure Behavior](readme-asset/step14-configure-behavior.png)

---

## Step 15: Test Your Agent with KTP

Now let's test the agent!

1. In the agent test panel, type a prompt like:
   ```
   I need to extract an information from a document
   ```

![Prompt Agent](readme-asset/step15-prompt-agent.png)

2. Click **"Add files"**

![Add Files](readme-asset/step15-add-files.png)

3. Upload a test KTP file (e.g., `KTP_5.jpg`)
4. The agent will process the document and return the extracted information

![KTP Result](readme-asset/step15-ktp-result.png)

You should see structured data extracted from the ID card, including name, ID number, address, and other fields!

---

## Step 16: Test Your Agent with Receipts

1. Try the same process with a receipt:
   ```
   Please extract information from this receipt
   ```
2. Upload a receipt image
3. The agent will extract the total purchase amount and date

![Receipt Result](readme-asset/step16-receipt-result.png)

---

## 🎉 Congratulations!

You've successfully built an OCR AI agent that can:
- ✅ Accept document uploads
- ✅ Automatically classify documents (KTP vs Receipts)
- ✅ Extract structured information based on document type
- ✅ Return formatted results to users

---

## Key Concepts Learned

1. **Agentic Workflows** - Creating multi-step processing pipelines
2. **Document Classification** - Automatically categorizing documents
3. **Branch Logic** - Creating conditional paths in workflows
4. **Document Extraction** - Using OCR to extract structured data
5. **Schema Definition** - Using pre-built and custom schemas
6. **Agent Behavior** - Configuring how agents interact with users

---



## Troubleshooting

### Issue: Document not classified correctly
**Solution:** 
- Ensure you uploaded clear, high-quality sample documents
- Add more sample documents for training
- Check that document classes are spelled correctly

### Issue: Fields not extracted properly
**Solution:**
- Verify sample documents contain the fields you want to extract
- Ensure field names match the data in documents
- Try adding more sample documents

### Issue: Agent not responding
**Solution:**
- Check that the workflow is properly connected
- Verify all steps are configured
- Ensure the agent behavior is filled in

---

## Resources

- **Sample Documents:** Use the files in `KTP/` and `Invoice/` folders
- **watsonx Orchestrate Documentation:** [ibm.com/docs/en/watsonx/watson-orchestrate/base](https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base)
- **Document Processing Guide:** Check the official documentation for advanced features

---

## Summary

In this lab, you learned how to:
1. Create an AI agent from scratch
2. Build an agentic workflow with multiple steps
3. Implement document classification
4. Configure conditional branching
5. Set up document extraction with both pre-built and custom schemas
6. Test and validate your OCR agent

**Great job!** You now have a working OCR agent that can process real-world documents. This foundation can be extended to handle many other document types and business processes.

---

*Lab 1 Complete - Ready for Lab 2!*
