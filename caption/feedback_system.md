# Video Caption Feedback System Documentation

## Overview
The feedback system is designed to manage the review and revision process for video captions. It involves two main roles: annotators (who create captions) and reviewers (who evaluate and provide feedback).

## Key Components

### 1. User Roles
- **Annotators**: Create initial captions and can modify them based on feedback
- **Reviewers**: Evaluate captions and provide feedback (must be in `APPROVED_REVIEWERS` list)
- **Reviewer Restrictions**:
  - Cannot review their own captions
  - Cannot review captions they previously annotated
  - Must be an approved reviewer

### 2. File Structure
- `_feedback.json`: Current feedback file
- `_feedback_prev.json`: Previous feedback file (created when a caption is rejected)
- `_review.json`: Reviewer's decision (approval/rejection)

### 3. States and Transitions
- **Initial State**: Annotator creates caption
- **Review State**: Reviewer evaluates caption
  - **Approval**: Sets `reviewer_double_check = True`
  - **Rejection**: 
    - Copies current feedback to previous feedback
    - Creates new reviewer data with `reviewer_double_check = False`
    - Clears current feedback for new input

### 4. Feedback Display
The system provides detailed feedback comparison with:
- Word-level diff highlighting (red for deletions, green for additions)
- GPT-powered difference summarization
- Clear identification of annotator and reviewer feedback
- Warning when a caption is rejected but not corrected

### 5. Key Functions
- `can_reviewer_redo()`: Checks if a user can review a caption
- `copy_to_prev_feedback()`: Handles feedback file management during rejection
- `display_feedback_differences()`: Shows differences between annotator and reviewer feedback
- `handle_rejection()`: Manages the rejection process

### 6. User Interface Features
- Clear status indicators (✅ for completed, ✅✅ for approved, ❌ for rejected)
- Detailed feedback comparison with both visual and GPT-powered analysis
- Error messages for invalid review attempts

## Detailed Rules and Logic

### 1. Annotator Identification
- If only `_feedback.json` exists: Annotator is the user in this file
- If both `_feedback.json` and `_feedback_prev.json` exist:
  - Annotator is the user in `_feedback_prev.json`
  - Reviewer is the user in `_feedback.json`
  - Exception: If files are identical, it means the reviewer rejected but hasn't fixed the caption yet

### 2. Same Annotator Redo Rules
- **Not Reviewed Yet**: 
  - Can redo freely
  - Updates current feedback file only (no `_feedback_prev.json` created)
- **Already Reviewed**:
  - Cannot redo
  - Shows appropriate message:
    - If approved: "This caption has been approved."
    - If rejected: "This caption has been rejected. Please see the difference between your feedback and reviewer feedback below" (shows GPT-polished feedback comparison)

### 3. Different User Access Rules
- **Non-Approved User**:
  - Cannot redo
  - Shows message: "You are not an approved reviewer. Please reach out to Zhiqiu Lin if you want to review"
- **Approved Reviewer**:
  - Can redo if caption not reviewed
  - If caption rejected:
    - Can only overwrite current feedback
    - Previous feedback remains unchanged
  - Cannot review if they are the annotator (skips review expander with explanation)

### 4. Review Process Rules
- Annotator cannot review their own captions
- Reviewers must be in `APPROVED_REVIEWERS` list
- Rejection process:
  - Creates `_feedback_prev.json` if not exists
  - Sets `reviewer_double_check = False`
  - Requires reviewer to provide new feedback
- Approval process:
  - Sets `reviewer_double_check = True`
  - Preserves existing feedback structure

## Workflow Example

1. **Annotator Creates Caption**:
   - Creates initial caption
   - Receives feedback from reviewer

2. **Reviewer Evaluates**:
   - Can approve or reject
   - If rejected, must provide feedback
   - Cannot review their own captions

3. **After Rejection**:
   - Original feedback is preserved in `_feedback_prev.json`
   - New feedback can be added
   - System tracks who rejected and who needs to correct

4. **After Approval**:
   - Caption is marked as approved
   - Can still be rejected if needed

## Difference Highlighting System

The system uses two main libraries for difference highlighting:
1. **difflib**: For basic word-level differences and run length detection
2. **diff_match_patch**: For HTML-formatted word-level differences with custom styling

Key functions:
- `highlight_differences()`: Uses difflib for basic highlighting
- `html_word_diff()`: Uses diff_match_patch for HTML-formatted differences
- `is_large_diff()`: Detects significant changes (≥5 consecutive tokens)

### When to Use Which Function
- Use `html_word_diff()` when there are large changes (≥5 consecutive tokens) for better readability
- Use `highlight_differences()` for smaller changes where simple highlighting is sufficient
- `is_large_diff()` is used internally to determine which highlighting method to use

### GPT Summary
The system uses GPT to provide a natural language summary of the differences between feedback versions. This helps reviewers quickly understand the key changes made to the caption.