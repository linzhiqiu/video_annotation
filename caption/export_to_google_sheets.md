# Google Sheets Export System Documentation

## Overview

The Google Sheets export system automatically generates comprehensive statistics for video caption annotation and review work. It creates a master tracking sheet with links to individual user performance sheets, providing detailed metrics for payment calculation and quality monitoring.

## System Architecture

```
Master Sheet
├── Annotators Tab (all users who created captions)
└── Reviewers Tab (all users who reviewed captions)
    │
    ├── Links to Individual User Sheets
    │
    └── Individual User Sheets (e.g. "John Doe Annotator")
        ├── Payment Tab (salary/payment info)
        └── Feedback Tab (performance feedback)
```

---

## Master Sheet Structure

### Annotators Tab

| Column | Description | Calculation |
|--------|-------------|-------------|
| **User Name** | Full name of annotator | From `ANNOTATORS` config |
| **Email** | Email address | From `ANNOTATORS` config |
| **Annotation Sheet** | 🔗 Smart chip link to user's annotation sheet | Hyperlink to individual sheet |
| **Last Annotated Time** | Most recent annotation submission | Latest `timestamp` from feedback files |
| **🧍‍♂️Subject Total** | Total Subject captions completed | Count of completed Subject tasks |
| **🏞️Scene Total** | Total Scene captions completed | Count of completed Scene tasks |
| **🏃‍♂️Motion Total** | Total Motion captions completed | Count of completed Motion tasks |
| **🗺️Spatial Total** | Total Spatial captions completed | Count of completed Spatial tasks |
| **📷Camera Total** | Total Camera captions completed | Count of completed Camera tasks |
| **🎨Color Total** | Total Color captions completed | Count of completed Color tasks |
| **💡Lighting Total** | Total Lighting captions completed | Count of completed Lighting tasks |
| **🌟Effects Total** | Total Effects captions completed | Count of completed Effects tasks |

### Reviewers Tab

| Column | Description | Calculation |
|--------|-------------|-------------|
| **User Name** | Full name of reviewer | From `ANNOTATORS` config |
| **Email** | Email address | From `ANNOTATORS` config |
| **Review Sheet** | 🔗 Smart chip link to user's review sheet | Hyperlink to individual sheet |
| **Last Review Time** | Most recent review submission | Latest `review_timestamp` from review files |
| **🧍‍♂️Subject Total** | Total Subject reviews completed | Count of completed Subject reviews |
| **🏞️Scene Total** | Total Scene reviews completed | Count of completed Scene reviews |
| **🏃‍♂️Motion Total** | Total Motion reviews completed | Count of completed Motion reviews |
| **🗺️Spatial Total** | Total Spatial reviews completed | Count of completed Spatial reviews |
| **📷Camera Total** | Total Camera reviews completed | Count of completed Camera reviews |
| **🎨Color Total** | Total Color reviews completed | Count of completed Color reviews |
| **💡Lighting Total** | Total Lighting reviews completed | Count of completed Lighting reviews |
| **🌟Effects Total** | Total Effects reviews completed | Count of completed Effects reviews |

---

## Permission Management

The export system automatically manages Google Sheets permissions for all created sheets:

### **Editor Access (Full Edit Permissions)**
The following users receive automatic editor access to all sheets:
- zhiqiulin98@gmail.com
- ttiffanyyllingg@gmail.com  
- isaacli@andrew.cmu.edu
- huangyuhan1130@gmail.com
- edzee1701@gmail.com

### **Commenter Access (View + Comment Only)**
All other users who have access to the sheets receive commenter permissions only.

### **Automatic Permission Updates**
- Permissions are updated every time the export runs
- Applied to both the master sheet and all individual user sheets
- If someone's access level needs to change, it's automatically corrected
- No manual permission management required

### **Security Features**
- Only specified editor emails can modify data
- Other collaborators can view and comment but cannot edit
- Sheet owners retain full control
- Individual user sheets inherit the same permission structure

---

## Individual User Sheets

Each user has their own Google Sheet with two tabs: **Payment** and **Feedback**. The structure differs slightly between Annotators and Reviewers.

**Important Note**: The **Video Count** column only appears in individual user sheets, not in the master sheet. This column shows how many videos are in each JSON sheet file to provide context for the completion percentages.

### Multi-Row Header Structure

The sheets use a **2-row header system** with merged cells for better organization:

**Row 1**: Main category headers (spans multiple columns)
**Row 2**: Specific metric headers (individual columns)

### Annotator Sheet Structure

#### Common Columns (Both Tabs)

```
Row 1: | Json Sheet Name | Video Count | Completion Ratio | Reviewed Ratio | Last Submitted | Payment/Feedback | 🧍‍♂️Subject              | 🏞️Scene                |
Row 2: |                 |             | All | Current    | All | Current  | Timestamp      | Column           | Acc | Comp | Rev | ... | Acc | Comp | Rev | ... |
```

| Column Group | Sub-Column | Description | Formula |
|--------------|------------|-------------|---------|
| **Json Sheet Name** | - | Video file identifier | Video URLs filename |
| **Video Count** | - | Number of videos in this JSON file | `len(video_urls)` from JSON file |
| **Completion Ratio** | All Users | % of all tasks completed by anyone | `completed_all_users / total_possible` |
| | Current User | % of all tasks completed by this user | `completed_current_user / total_possible` |
| **Reviewed Ratio** | All Users | % of completed tasks that are reviewed | `reviewed_all_users / completed_all_users` |
| | Current User | % of this user's work that was reviewed | `reviewed_current_user_work / completed_current_user` |
| **Last Submitted Timestamp** | - | Most recent annotation by this user | Latest `timestamp` from user's feedback files |
| **Payment Tab Only** | Payment Timestamp | When payment was made | **Manual Entry** |
| | Base Salary | Base payment amount | **Manual Entry** |
| | Bonus Salary | Performance bonus | **Manual Entry** |
| **Feedback Tab Only** | Feedback to Annotator | Performance feedback | **Manual Entry** |

#### Per-Task Columns (6 columns per task)

```
Row 1: | 🧍‍♂️Subject                                    |
Row 2: | Accuracy | Completion | Reviewed | Completed | Reviewed | Rejected |
```

| Sub-Column | Description | Formula |
|------------|-------------|---------|
| **Accuracy** | % of reviewed work that was accepted | `(reviewed - rejected) / reviewed` |
| **Completion** | % of total task completed by user | `completed / total` |
| **Reviewed** | % of user's work that was reviewed | `reviewed / completed` |
| **Completed** | Number of tasks completed | Count of completed tasks |
| **Reviewed** | Number of tasks reviewed | Count of reviewed tasks |
| **Rejected** | Number of tasks rejected | Count of rejected tasks |

### Reviewer Sheet Structure

#### Common Columns (Both Tabs)

```
Row 1: | Json Sheet Name | Video Count | Completion Ratio | Reviewed Ratio    | Last Submitted | Payment/Feedback | 🧍‍♂️Subject   | 🏞️Scene     |
Row 2: |                 |             | All Users        | All | Current     | Timestamp      | Column           | Comp | Comp | Comp | Comp |
```

| Column Group | Sub-Column | Description | Formula |
|--------------|------------|-------------|---------|
| **Json Sheet Name** | - | Video file identifier | Video URLs filename |
| **Video Count** | - | Number of videos in this JSON file | `len(video_urls)` from JSON file |
| **Completion Ratio** | All Users | % of all tasks completed by anyone | `completed_all_users / total_possible` |
| **Reviewed Ratio** | All Users | % of completed tasks reviewed by anyone | `reviewed_all_users / completed_all_users` |
| | Current User | % of completed tasks reviewed by this user | `reviewed_by_current_user / completed_all_users` |
| **Last Submitted Timestamp** | - | Most recent review by this user | Latest `review_timestamp` from user's review files |

#### Per-Task Columns (2 columns per task)

```
Row 1: | 🧍‍♂️Subject   |
Row 2: | Completion | Completed |
```

| Sub-Column | Description | Formula |
|------------|-------------|---------|
| **Completion** | % of total task reviewed by user | `reviewed / total` |
| **Completed** | Number of tasks reviewed | Count of reviewed tasks |

---

## Calculation Details

### Key Metrics Explained

#### For Annotators

1. **Video Count**: Number of videos in the JSON sheet file
   ```
   len(video_urls) from the JSON file
   ```

2. **Completion Ratio (All Users)**: Shows overall progress on the video batch
   ```
   (Total tasks completed by anyone) / (Video Count × Number of Tasks)
   ```

3. **Completion Ratio (Current User)**: Shows this annotator's contribution
   ```
   (Tasks completed by this user) / (Video Count × Number of Tasks)
   ```

4. **Reviewed Ratio (All Users)**: Shows overall review progress
   ```
   (Total tasks reviewed by anyone) / (Total tasks completed by anyone)
   ```

5. **Reviewed Ratio (Current User)**: Shows review rate of this annotator's work
   ```
   (This user's tasks that were reviewed) / (This user's completed tasks)
   ```

6. **Task Accuracy**: Quality metric for each task type
   ```
   (Reviewed tasks - Rejected tasks) / (Reviewed tasks)
   ```

#### For Reviewers

1. **Video Count**: Same as annotators - number of videos in the JSON sheet file

2. **Completion Ratio (All Users)**: Same as annotators - overall batch progress

3. **Reviewed Ratio (All Users)**: Overall review progress across all reviewers

4. **Reviewed Ratio (Current User)**: This reviewer's contribution to reviews
   ```
   (Tasks reviewed by this user) / (Total completed tasks)
   ```

### Status Definitions

- **Completed**: Task has a feedback file (`_feedback.json`)
- **Reviewed**: Task has a review file (`_review.json`) 
- **Approved**: Review file has `reviewer_double_check: true`
- **Rejected**: Review file has `reviewer_double_check: false`

---

## File Structure Mapping

### Video File Organization
```
caption/
├── output/
│   ├── subject_description/
│   │   ├── video123_feedback.json
│   │   ├── video123_review.json
│   │   └── ...
│   ├── scene_composition/
│   └── ...
└── data/
    ├── batch1_videos.json
    ├── batch2_videos.json
    └── ...
```

### JSON Sheet Name
The "Json Sheet Name" column refers to the video batch files:
- `batch1_videos.json` → "batch1_videos.json"
- `batch2_videos.json` → "batch2_videos.json"

Each row in the user sheets represents statistics for that user's work on that specific video batch.

---

## Manual vs Automatic Columns

### Automatic Columns (Updated on every export)
- All completion and review ratios
- Task statistics (completed, reviewed, rejected counts)
- Timestamps
- Accuracy calculations

### Manual Columns (Preserved during updates)
- **Payment Tab**: Payment Timestamp, Base Salary, Bonus Salary
- **Feedback Tab**: Feedback to Annotator

**Important**: The export system will never overwrite data in manual columns. You can safely enter payment information and feedback without losing it on subsequent exports.

---

## Usage Examples

### Export for Main Configuration
```bash
python caption/export_to_google_sheet.py --config-type main --master-sheet-id 1ABC123XYZ
```

### Export for Lighting Configuration  
```bash
python caption/export_to_google_sheet.py --config-type lighting --master-sheet-id 1ABC123XYZ
```

### Reading the Data

#### Payment Calculation Example
For annotator "John Doe" working on "batch1_videos.json":
- Video Count: 50 videos (shown in individual sheet, not master sheet)
- Completion Ratio (Current User): 85% → John completed 85% of possible tasks (85% of 50 videos × 8 tasks = 340 tasks)
- Task Accuracy: 92% → 92% of John's reviewed work was approved
- Base Salary: $500 (manual entry)
- Bonus: $50 (manual entry based on 92% accuracy)

#### Quality Monitoring Example
For reviewer "Jane Smith":
- Video Count: 50 videos (shown in individual sheet only)
- Reviewed Ratio (Current User): 30% → Jane reviewed 30% of all completed work
- Last Review Time: Shows when Jane last submitted a review (displayed in master sheet)
- Individual task completion shows which task types Jane focuses on

#### Batch Progress Example
Looking at "batch2_videos.json":
- Video Count: 25 videos (shown in individual sheets)
- Total possible tasks: 25 videos × 8 tasks = 200 tasks
- Completion Ratio (All Users): 60% → 120 tasks completed across all annotators
- Reviewed Ratio (All Users): 75% → 90 of the 120 completed tasks have been reviewed

#### Permission Management Example
When the export runs:
- zhiqiulin98@gmail.com automatically gets editor access to all sheets
- Other collaborators get commenter access only
- No manual permission sharing required
- All individual user sheets inherit the same permission structure

---

## Best Practices

### For Administrators
1. **Run exports regularly** to keep data current
2. **Fill payment columns manually** after reviewing performance
3. **Use accuracy metrics** to identify training needs
4. **Monitor completion ratios** to track project progress
5. **Verify permissions** are automatically managed correctly

### For Quality Control
1. **Check accuracy trends** across different annotators
2. **Review timestamp patterns** to identify productivity issues
3. **Use feedback columns** to provide targeted guidance
4. **Monitor reviewed ratios** to ensure adequate quality control

### For Payment Processing
1. **Verify completion ratios** before processing payments
2. **Apply bonus criteria** based on accuracy metrics
3. **Document payment dates** in manual columns
4. **Cross-reference with individual task counts** for validation
5. **Trust automatic permission management** for secure access control

---

## Troubleshooting

### Common Issues

**Authentication Errors**: 
- Ensure OAuth 2.0 credentials are saved as `caption/credentials.json`
- Verify both Sheets and Drive permissions were granted during OAuth flow
- Check that `caption/token_export.json` was created after first successful authentication
- If token expires, delete `caption/token_export.json` and re-authenticate

**Missing Data**: Ensure all feedback and review JSON files are properly formatted and contain required fields (`timestamp`, `user`, `reviewer_name`, etc.)

**Incorrect Ratios**: Check that video URL files match the actual video data and all tasks are properly configured

**Permission Errors**: 
- The script automatically manages permissions for specified editor emails
- Ensure you have access to create new Google Sheets in your Google Drive
- Master sheet will be shared automatically with editor emails on export

**Export Failures**: 
- Rate limiting: Wait 1 hour or use `--resume-from 'User Name Role'` to continue
- Use `--skip-individual` to update only the master sheet
- Check Google Drive storage quota if sheet creation fails

### Data Validation

Always verify a few sample calculations manually:
1. Pick a user and video batch
2. Count actual completed tasks in the file system
3. Compare with sheet values
4. Check that manual columns are preserved after re-export
5. Verify permission settings are applied correctly