# Video Caption Export System Documentation

## Overview: The Caption Task System

The video caption system processes videos through **5 distinct caption tasks**, each focusing on different aspects of video content:

### **Caption Tasks**
| Task | Code | Focus | Example |
|------|------|-------|---------|
| **Subject Description** | `subject` | Main subjects/objects in the video | `"A person walking with a dog"` |
| **Scene Composition and Dynamics** | `scene` | Environment, setting, overall composition | `"Outdoor park setting with trees and pathways"` |
| **Subject Motion and Dynamics** | `motion` | How subjects move and behave | `"Walking at a steady pace, occasionally stopping"` |
| **Spatial Framing and Dynamics** | `spatial` | Camera positioning and spatial relationships | `"Medium shot following the subject from behind"` |
| **Camera Framing and Dynamics** | `camera` | Camera movement and framing techniques | `"Steady handheld tracking shot with slight camera shake"` |

Each video can be processed through all 5 tasks independently. Each task follows the same annotation workflow but produces focused captions for its specific aspect.

## Task-Level Status Categories

Each caption task for each video has one of these statuses:

### 1. **Not Completed** (`not_completed`)
- **Description**: No annotation work has begun for this task
- **File State**: No `_feedback.json` file exists
- **Export**: Status marker only

### 2. **Completed Not Reviewed** (`completed_not_reviewed`) 
- **Description**: Annotator has completed the caption task, waiting for reviewer
- **File State**: `_feedback.json` exists, no `_review.json` file
- **Export**: Single entry with annotator's complete workflow

### 3. **Approved** (`approved`)
- **Description**: Reviewer approved the annotator's caption for this task
- **File State**: `_feedback.json` + `_review.json` with `reviewer_double_check: true`
- **Export**: Single entry (annotator's work that was approved)

### 4. **Rejected** (`rejected`)
- **Description**: Reviewer rejected annotator's caption and provided improved version for this task
- **File State**: `_feedback.json` (reviewer's version) + `_feedback_prev.json` (annotator's version) + `_review.json` with `reviewer_double_check: false`
- **Export**: Two entries - reviewer's improved version + annotator's rejected version as negative example

## Workflow Data Structure

Every caption entry contains complete workflow data from both annotation stages:

### **Stage 1: Pre-Caption Generation**

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `pre_caption` | string | AI-generated initial caption | `"A person walking in a park"` |
| `pre_caption_prompt` | string | Prompt used to generate pre-caption | `"Describe the main subject activity in this video"` |
| `pre_caption_llm` | string | Model used for pre-caption | `"gpt-4o-2024-08-06"` |
| `pre_caption_mode` | string | Generation mode (Text/Image/Video) | `"Video"` |
| `initial_caption_rating_score` | integer | User's 1-5 rating of pre-caption | `3` |
| `feedback_is_needed` | boolean | Whether improvement workflow needed | `true` |

### **Stage 2: Feedback and Final Caption**

| Field | Type | Present When | Description |
|-------|------|--------------|-------------|
| `initial_feedback` | string | `feedback_is_needed` | User's raw feedback on pre-caption |
| `gpt_feedback` | string | `feedback_is_needed` | AI-polished version of feedback |
| `gpt_feedback_llm` | string | `feedback_is_needed` | Model used for feedback polishing |
| `gpt_feedback_prompt` | string | `feedback_is_needed` | Prompt used for feedback polishing |
| `feedback_rating_score` | integer | `feedback_is_needed` | User's 1-5 rating of polished feedback |
| `final_feedback` | string | `feedback_is_needed` | Final feedback used for caption generation |
| `gpt_caption` | string | `feedback_is_needed` | AI-generated improved caption |
| `gpt_caption_prompt` | string | `feedback_is_needed` | Prompt used for caption improvement |
| `gpt_caption_llm` | string | `feedback_is_needed` | Model used for caption generation |
| `caption_rating_score` | integer | `feedback_is_needed` | User's 1-5 rating of generated caption |
| `final_caption` | string | Always | Final caption text (either pre-caption or improved version) |

### **Review Metadata (Approved/Rejected Tasks)**

| Field | Type | Description |
|-------|------|-------------|
| `reviewer` | string | Name of the reviewer |
| `review_timestamp` | string | When the review occurred |
| `reviewer_double_check` | boolean | True if approved, False if rejected |
| `original_annotator` | string | Original annotator's name (rejected tasks only) |

## Export Structure

Each video contains task-level data organized by caption type:

```json
{
  "video_id": "video_001",
  "video_url": "https://example.com/video_001.mp4",
  "captions": {
    "subject": { 
      "status": "approved",
      "caption_data": { /* complete workflow data with review metadata */ }
    },
    "scene": { 
      "status": "completed_not_reviewed",
      "caption_data": { /* complete workflow data */ }
    },
    "motion": { 
      "status": "rejected",
      "caption_data": { /* reviewer's improved version */ },
      "negative_example": { /* annotator's rejected version */ }
    },
    "spatial": { 
      "status": "not_completed" 
    },
    "camera": { 
      "status": "approved",
      "caption_data": { /* complete workflow data with review metadata */ }
    }
  }
}
```

## Export Files

The export system creates files organized by meaningful completion levels:

### **Export Structure**
```
caption_export/
└── export_YYYYMMDD_HHMM/
    ├── all_videos_with_captions_YYYYMMDD_HHMM.json
    ├── reviewed_videos_YYYYMMDD_HHMM.json  
    ├── not_completed_videos_YYYYMMDD_HHMM.json
    └── comprehensive_statistics_YYYYMMDD_HHMM.json
```

When uploaded to HuggingFace, this appears as:
- https://huggingface.co/datasets/zhiqiulin/caption_export/tree/main/export_YYYYMMDD_HHMM/

### **Core Export Files**
- `all_videos_with_captions_YYYYMMDD_HHMM.json` - All videos with any completed caption tasks
- `reviewed_videos_YYYYMMDD_HHMM.json` - Videos with any reviewed tasks (approved OR rejected)
- `not_completed_videos_YYYYMMDD_HHMM.json` - Videos with no annotation work begun
- `comprehensive_statistics_YYYYMMDD_HHMM.json` - Detailed progress and quality metrics

## Why This Approach Works Better

## Environment Setup

### HuggingFace Token
Create a `.env` file in your project root:
```
HF_TOKEN=your-huggingface-token
```

The export script will automatically read this token for uploads. Never commit the `.env` file to git.

### Git Configuration
Add `caption_export/` to your `.gitignore` file to avoid committing large export files:
```
caption_export/
```

### **Task-Level Analysis vs Video-Level Categorization**
Videos typically have mixed completion status across their 5 tasks. For example:
- Subject: approved
- Scene: rejected  
- Motion: completed_not_reviewed
- Spatial: not_completed
- Camera: approved

Forcing such videos into a single "approved" or "rejected" category loses critical information and creates misleading categorizations.

### **Meaningful File Organization**
The export files are organized by completion levels that support real analysis needs:

- **all_videos_with_captions.json**: For general dataset analysis and model training
- **reviewed_videos.json**: For quality-assured data where human review has occurred
- **not_completed_videos.json**: For tracking remaining annotation work

## Usage

### **Basic Usage**
```bash
# Export all videos using default configuration (saves locally only)
python -m caption.export --export_dir caption_export

# Export and upload to HuggingFace (default repo: zhiqiulin/caption_export)
python -m caption.export --export_dir caption_export --hf_dataset zhiqiulin/caption_export

# Export and upload to custom HuggingFace dataset
python -m caption.export --export_dir caption_export --hf_dataset your_username/your_dataset

### **Configuration Options**
```bash
# Use lighting project configuration
python -m caption.export --config-type lighting --export_dir caption_export --hf_dataset zhiqiulin/caption_export

# Export only videos with reviewed tasks
python -m caption.export --only_reviewed --export_dir caption_export --hf_dataset zhiqiulin/caption_export

# Continue export even if edge cases found
python -m caption.export --ignore_errors --export_dir caption_export --hf_dataset zhiqiulin/caption_export
```

### **Key Features**
- **Task-Level Organization**: Preserves the multi-dimensional nature of caption data
- **Complete Workflow Preservation**: Captures all annotation and review metadata
- **Negative Examples**: Includes rejected captions for training contrast
- **Edge Case Detection**: Identifies rejected captions that haven't been improved
- **HuggingFace Integration**: Direct upload to HuggingFace datasets with secure token handling
- **Git-Safe Storage**: Exports saved to ignored directory to avoid large file commits
- **Comprehensive Statistics**: Detailed progress tracking and quality metrics

## Data Analysis Examples

### **Finding High-Quality Captions**
```python
import json

# Load the main export file
with open('all_videos_with_captions_20250910_1430.json', 'r') as f:
    videos = json.load(f)

# Extract all approved captions
approved_captions = []
for video in videos:
    for task_name, task_data in video["captions"].items():
        if task_data.get("status") == "approved":
            approved_captions.append({
                "video_id": video["video_id"],
                "task": task_name,
                "caption": task_data["caption_data"]["final_caption"],
                "workflow_type": task_data["caption_data"]["workflow_type"]
            })

print(f"Found {len(approved_captions)} approved captions")
```

### **Analyzing Review Progress by Task**
```python
# Count completion by task type
task_progress = {}
for video in videos:
    for task_name, task_data in video["captions"].items():
        if task_name not in task_progress:
            task_progress[task_name] = {"total": 0, "completed": 0, "reviewed": 0}
        
        task_progress[task_name]["total"] += 1
        
        status = task_data.get("status", "not_completed")
        if status != "not_completed":
            task_progress[task_name]["completed"] += 1
        if status in ["approved", "rejected"]:
            task_progress[task_name]["reviewed"] += 1

# Print progress report
for task, stats in task_progress.items():
    completion_rate = (stats["completed"] / stats["total"]) * 100
    review_rate = (stats["reviewed"] / stats["completed"]) * 100 if stats["completed"] > 0 else 0
    print(f"{task}: {completion_rate:.1f}% completed, {review_rate:.1f}% reviewed")
```

### **Extracting Training Data with Negative Examples**
```python
# Get training pairs (positive and negative examples)
training_pairs = []
for video in videos:
    for task_name, task_data in video["captions"].items():
        if task_data.get("status") == "rejected" and "negative_example" in task_data:
            training_pairs.append({
                "video_id": video["video_id"],
                "task": task_name,
                "positive_caption": task_data["caption_data"]["final_caption"],
                "negative_caption": task_data["negative_example"]["final_caption"],
                "reviewer": task_data["caption_data"]["reviewer"]
            })

print(f"Found {len(training_pairs)} positive/negative training pairs")
```

## Export Examples

### **Mixed Status Video (Common Scenario)**
```json
{
  "video_id": "video_123",
  "video_url": "https://example.com/video_123.mp4",
  "captions": {
    "subject": {
      "status": "approved",
      "caption_data": {
        "user": "alice_smith",
        "timestamp": "2025-06-29T11:45:00",
        "reviewer": "jane_doe",
        "review_timestamp": "2025-06-29T14:15:00",
        "reviewer_double_check": true,
        "workflow_type": "improved_precaption",
        "pre_caption": "Person with dog",
        "pre_caption_llm": "gpt-4o-2024-08-06",
        "initial_caption_rating_score": 3,
        "feedback_is_needed": true,
        "initial_feedback": "Add more specific details about clothing and setting",
        "gpt_feedback": "Please describe the person's clothing and the park environment more specifically",
        "final_feedback": "Add clothing details and park setting description",
        "gpt_caption": "Person in blue jacket walking small brown dog on leash through park",
        "final_caption": "Person in blue jacket walking small brown dog on leash through sunny suburban park"
      }
    },
    "scene": {
      "status": "rejected",
      "caption_data": {
        "user": "jane_reviewer",
        "timestamp": "2025-06-29T16:20:00",
        "reviewer": "jane_reviewer",
        "review_timestamp": "2025-06-29T15:30:00",
        "reviewer_double_check": false,
        "original_annotator": "bob_smith",
        "workflow_type": "improved_precaption",
        "pre_caption": "Park environment with trees and pathways",
        "initial_caption_rating_score": 2,
        "feedback_is_needed": true,
        "initial_feedback": "Need more environmental detail and atmosphere",
        "final_caption": "Suburban park setting with mature oak trees, paved walking paths, and well-maintained grassy areas under clear sky"
      },
      "negative_example": {
        "user": "bob_smith",
        "timestamp": "2025-06-29T12:15:00",
        "workflow_type": "improved_precaption",
        "pre_caption": "Outdoor area",
        "initial_caption_rating_score": 2,
        "feedback_is_needed": true,
        "initial_feedback": "Add more detail about the setting",
        "final_caption": "Park with trees and pathways"
      }
    },
    "motion": {
      "status": "completed_not_reviewed",
      "caption_data": {
        "user": "charlie_doe",
        "timestamp": "2025-06-29T13:30:00",
        "workflow_type": "perfect_precaption",
        "pre_caption": "Walking at steady pace with dog occasionally sniffing ground and pausing",
        "initial_caption_rating_score": 5,
        "feedback_is_needed": false,
        "final_caption": "Walking at steady pace with dog occasionally sniffing ground and pausing"
      }
    },
    "spatial": {
      "status": "not_completed"
    },
    "camera": {
      "status": "approved",
      "caption_data": {
        "user": "diana_kim",
        "timestamp": "2025-06-29T14:45:00",
        "reviewer": "jane_doe",
        "review_timestamp": "2025-06-29T16:30:00",
        "reviewer_double_check": true,
        "workflow_type": "improved_precaption",
        "pre_caption": "Wide shot",
        "initial_caption_rating_score": 2,
        "feedback_is_needed": true,
        "initial_feedback": "Specify camera position and framing details",
        "final_caption": "Static wide shot from slightly elevated position capturing the full scene with balanced composition"
      }
    }
  }
}
```

This example demonstrates why task-level organization is essential - this single video has 5 different completion states across its caption tasks, making video-level categorization meaningless.


## Critique Generation for Exported Data

After exporting caption data, you can generate various types of critiques for evaluation and analysis purposes using the critique generation script.

### **How It Works**

The critique generation system processes caption data through several key steps:

1. **Input Filtering**: Only processes captions with status "approved" or "rejected" - these are the only captions that should have critiques generated
2. **Smart Skipping**: Some critique types (replacement_error, deletion_error, nonconstructive) automatically skip captions with perfect scores (5/5) since there's insufficient content to modify
3. **Incremental Processing**: Detects changes in caption data and configuration parameters, only regenerating critiques when necessary to avoid redundant work
4. **Multi-Model Generation**: Uses different LLMs depending on critique type - GPT-4.1 for text-only error critiques, Gemini for video-enabled critiques
5. **Data Preservation and Merging**: Loads the original caption export data and merges critique fields into the existing structure, preserving all original data
6. **Complete Dataset Upload**: Only exports and uploads when ALL seven critique types are successfully completed (no failures across any critique type)

**Key Insight**: The script is designed for large-scale processing (thousands of videos) with robust error handling, progress tracking, and parallel execution support. Upload only happens when you have a complete dataset with all critique types.

### **Data Preservation and Merging**

The critique generation system preserves all original caption export data:

1. **Loads Original Export**: Reads `all_videos_with_captions_*.json` from the specified export folder
2. **Merges Critique Data**: Adds critique fields to existing caption type entries without modifying original structure
3. **Preserves Everything**: All original fields remain intact:
   - `video_url`
   - `caption_data` with complete workflow information
   - `negative_example` for rejected captions
   - Review metadata and timestamps
4. **Only Adds Critique Fields**: Each critique type becomes an additional field within the caption type structure

**Result**: The final export contains both the complete original caption data AND all seven critique types in a single unified structure.

### **Overview**

The critique generation system creates seven types of critiques for each completed caption task:

1. **Insertion Error Critique** - Adds incorrect/irrelevant details to original feedback
2. **Replacement Error Critique** - Replaces correct details with wrong information  
3. **Deletion Error Critique** - Removes important details making critique incomplete
4. **Non-Constructive Critique** - Removes helpful suggestions, leaving only criticism
5. **Video Model Critique** - Direct critique from Gemini with video access
6. **Blind Model Critique** - Critique from Gemini without video access (hallucinated)
7. **Worst Caption Generation** - Generates entirely new incorrect caption (no critique or revision)

### **Basic Usage**

Generate all seven critique types for the same export folder:

```bash
# Generate insertion error critiques
python -m caption.generate_critiques --critique-type insertion_error_critique --export-folder caption_export/export_20251121_1332

# Generate replacement error critiques  
python -m caption.generate_critiques --critique-type replacement_error_critique --export-folder caption_export/export_20251121_1332

# Generate deletion error critiques
python -m caption.generate_critiques --critique-type deletion_error_critique --export-folder caption_export/export_20251121_1332

# Generate non-constructive critiques
python -m caption.generate_critiques --critique-type nonconstructive_critique --export-folder caption_export/export_20251121_1332

# Generate video model critiques
python -m caption.generate_critiques --critique-type video_model_critique --export-folder caption_export/export_20251121_1332

# Generate blind model critiques
python -m caption.generate_critiques --critique-type blind_model_critique --export-folder caption_export/export_20251121_1332

# Generate worst caption
python -m caption.generate_critiques --critique-type worst_caption_generation --export-folder caption_export/export_20251121_1332
```

**Note**: The `--export-folder` parameter is required so the script can:
1. Load the original caption export data to merge with critique data
2. Process only the videos from that specific export
3. Save the consolidated output back to the same export folder location
4. Maintain the connection between captions and their critiques

By default, each script automatically exports consolidated JSON and uploads to HuggingFace (`zhiqiulin/caption_export`) when all critiques are successful.

### **Critique Type Details**

#### Error Modification Critiques (Based on Original Feedback)
These critiques start with the original feedback and modify it in specific ways:

- **Insertion Error**: Adds one irrelevant or incorrect detail to the feedback
- **Replacement Error**: Replaces one correct detail with wrong information (skips perfect scores)
- **Deletion Error**: Removes one important detail from the feedback (skips perfect scores)
- **Non-Constructive**: Removes all constructive suggestions, leaving only criticisms (skips perfect scores)

#### Direct Generation Critiques (No Original Feedback)
These critiques generate new content directly:

- **Video Model**: Gemini generates critique with full video access
- **Blind Model**: Gemini generates critique without video access (hallucinated)
- **Worst Caption Generation**: GPT-4.1 generates entirely new incorrect caption with a completely different JSON structure

### **Configuration Options**

```bash
# Dry run to check what would be processed
python -m caption.generate_critiques --critique-type deletion_error_critique --export-folder caption_export/export_20251121_1332 --dry-run

# Force regeneration of all critiques
python -m caption.generate_critiques --critique-type video_model_critique --export-folder caption_export/export_20251121_1332 --force-regenerate

# Use lighting project configuration
python -m caption.generate_critiques --config-type lighting --export-folder caption_export/export_20251121_1332

# Custom retry settings
python -m caption.generate_critiques --critique-type insertion_error_critique --export-folder caption_export/export_20251121_1332 --max-retries 5

# Only process videos without existing critique files
python -m caption.generate_critiques --critique-type blind_model_critique --export-folder caption_export/export_20251121_1332 --new-only

# Verbose output with progress tracking
python -m caption.generate_critiques --critique-type nonconstructive_critique --export-folder caption_export/export_20251121_1332 --verbose
```

### **Parallel Processing**

Run different critique types simultaneously in separate terminals:

```bash
# Terminal 1: Generate insertion error critiques
python -m caption.generate_critiques --critique-type insertion_error_critique --export-folder caption_export/export_20251121_1332

# Terminal 2: Generate video model critiques  
python -m caption.generate_critiques --critique-type video_model_critique --export-folder caption_export/export_20251121_1332

# Terminal 3: Generate worst caption
python -m caption.generate_critiques --critique-type worst_caption_generation --export-folder caption_export/export_20251121_1332
```

### **Export and Upload**

**Automatic Export**: By default, each critique generation script automatically:
1. Loads the original caption export data from the export folder
2. Merges all critique data into the original structure
3. Exports consolidated JSON when **ALL SEVEN critique types** complete successfully across the entire dataset
4. Uploads to HuggingFace dataset `zhiqiulin/caption_export` (requires `HF_TOKEN` environment variable)
5. Falls back to local save if HuggingFace upload fails

**Upload Conditions ("Wait for All" Logic):**
- Only uploads when ALL critique types across ALL videos are either "success" or "skipped" (no "failed" status anywhere)
- Each individual script checks the global completion status of all 7 critique types
- Maintains original export folder structure in HuggingFace dataset
- Creates timestamped files: `all_videos_with_captions_and_critiques_[EXPORT_TIMESTAMP].json`

**Example Workflow:**
1. Run all 7 critique type scripts in parallel
2. Each script generates its own critique files
3. When the last critique type completes successfully, that script triggers the upload
4. The consolidated file contains all 7 critique types merged with original caption data for all videos

**Example Output:**
- Export folder: `caption_export/export_20251121_1332`
- Generated file: `all_videos_with_captions_and_critiques_20251121_1332.json`

### **Output Structure**

The script creates individual critique files in this directory structure:

```
output_critiques/
├── insertion_error_critique/
│   ├── subject_description/
│   │   ├── video_001_critique.json
│   │   └── video_002_critique.json
│   ├── scene_composition_dynamics/
│   └── ...
├── video_model_critique/
│   ├── subject_description/
│   └── ...
├── worst_caption_generation/
│   ├── subject_description/
│   └── ...
└── ...
```

The final consolidated JSON file merges critique data with the original export structure, preserving all original fields:

```json
{
  "video_id": "...",
  "video_url": "...",  // Preserved from original export
  "captions": {
    "subject": {
      "status": "approved",  // Preserved from original export
      "caption_data": { 
        // All original workflow data preserved:
        "user": "alice_smith",
        "timestamp": "2025-06-29T11:45:00",
        "reviewer": "jane_doe",
        "workflow_type": "improved_precaption",
        "pre_caption": "...",
        "final_caption": "...",
        // ... all other original fields intact
      },
      "insertion_error_critique": {  // Added by generate_critiques.py
        "status": "success",
        "model": "gpt-4.1-2025-04-14", 
        "prompt_name": "INSERTION_ERROR_CRITIQUE_PROMPT",
        "mode": "Text Only",
        "generated_critique": "The caption should mention the bright lighting...",
        "revised_caption_by_generated_critique": "The video features...",
        "timestamp": "2025-09-27T10:30:00Z"
      },
      "replacement_error_critique": {
        "status": "skipped",
        "skip_reason": "Perfect score (5/5) - this critique type skips perfect scores",
        "timestamp": "2025-09-27T10:32:00Z"
      },
      "video_model_critique": {
        "status": "success",
        "model": "gemini-2.5-pro",
        "mode": "Video",
        "generated_critique": "...",
        "revised_caption_by_generated_critique": "...",
        "timestamp": "2025-09-27T10:35:00Z"
      },
      "worst_caption_generation": {
        "status": "success",
        "model": "gpt-4.1-2025-04-14",
        "mode": "Text Only",
        "bad_caption": "A person wearing a red jacket walks through a snowy forest...",
        "timestamp": "2025-09-27T10:40:00Z"
      }
      // ... other critique types
    }
  }
}
```

### **Critique Generation Logic**

#### Processing Rules
- **Input**: Only processes captions with status "approved" or "rejected"
- **Always Generate**: Insertion Error, Video Model, Blind Model, Worst Caption Generation critiques
- **Skip for Perfect Scores**: Replacement Error, Deletion Error, Non-Constructive critiques skip when `initial_caption_rating_score == 5`

#### Model Usage
- **Text-Only Critiques**: GPT-4.1 (error modifications, worst caption generation) or Gemini (non-constructive, blind model)
- **Video-Enabled Critiques**: Gemini with direct video access
- **Caption Improvement**: GPT-4o for revision generation (not applicable for Worst Caption Generation)

#### Error Handling
- **Retry Logic**: Up to 3 attempts (configurable with `--max-retries`)
- **Individual Failures**: Failed critiques don't block other critiques for the same video
- **Incremental Processing**: Skip unchanged caption data and existing successful critiques
- **Change Detection**: Regenerates only when caption data or generation parameters change

### **Worst Caption Generation (New)**

The Worst Caption Generation type has a unique structure and purpose:

- **Purpose**: Generate a completely new, incorrect caption that replaces the original final caption entirely
- **Model**: GPT-4.1 (text-only, no video access)
- **Input**: Uses the final (high-quality) caption, not the pre_caption
- **JSON Structure**: 
  - Uses `bad_caption` field instead of `generated_critique` and `revised_caption_by_generated_critique`
  - Directly stores the incorrect caption without intermediate critique step
- **Behavior**: 
  - Generates a plausible-sounding but factually wrong caption
  - Maintains similar structure and length to the original
  - Ensures no details from the original caption are reused
  - No separate revision step - the generated bad caption is the final output
- **Use Case**: Testing model robustness against completely fabricated descriptions

### **Progress Tracking**

For large datasets with thousands of videos, the script provides:

- **Initial Analysis**: Detailed breakdown of what will be processed vs skipped
- **Progress Updates**: Shows completion percentage every 500 operations
- **Final Summary**: Complete statistics of successes, failures, and skips
- **Clean Output**: No individual video processing messages for large datasets

### **Troubleshooting**

#### Common Issues
1. **API Key Errors**: Ensure keys are properly configured in `.streamlit/secrets.toml`
2. **Failed Critiques**: Use `--force-regenerate` to retry all failed critiques
3. **Large Files**: Progress tracking prevents timeout concerns
4. **HuggingFace Upload**: Ensure `HF_TOKEN` is set in environment for uploads

#### Output Files
- **Individual Critiques**: Saved in `output_critiques/` directory structure
- **Consolidated Export**: `all_videos_with_captions_and_critiques_[timestamp].json` in export folder
- **HuggingFace**: Same structure as local export when uploaded

This system provides comprehensive critique generation capabilities while maintaining data integrity and supporting robust error recovery for large-scale processing.