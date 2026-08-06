# Video Annotation Process Documentation

## Overview

This documentation explains the complete workflow for processing video URLs, creating batch files, and updating the feedback applications for both the main project and the lighting project.

## 1. Generating Main Project URLs

### Using `load_xlsx.py`

1. **Purpose**: Extracts video URLs from Excel files and creates JSON files for overlapping and non-overlapping videos.

2. **Command**:
   ```bash
   python -m caption.load_xlsx --video_data video_data/20250406_setup_and_motion/videos.json --label_collections cam_motion cam_setup
   ```

3. **Output Files**:
   - `caption/video_urls/20250406_setup_and_motion/overlap_all_X.json`: Contains all overlapping videos
   - `caption/video_urls/20250406_setup_and_motion/nonoverlap_all_X.json`: Contains all non-overlapping videos
   - `caption/video_urls/20250406_setup_and_motion/overlap_X_to_Y.json`: Split files for overlapping videos
   - `caption/video_urls/20250406_setup_and_motion/overlap_invalid.json`: Contains invalid videos from the overlap set
   - `caption/video_urls/20250406_setup_and_motion/nonoverlap_invalid.json`: Contains invalid videos from the non-overlap set
   - Excel files in `caption/excel_export/20250406_setup_and_motion/`

4. **File Naming Conventions**:
   - `overlap_all_X.json`: Contains X overlapping videos
   - `nonoverlap_all_X.json`: Contains X non-overlapping videos
   - `overlap_X_to_Y.json`: Contains videos from index X to Y
   - `overlap_invalid.json`: Contains invalid videos from the overlap set
   - `nonoverlap_invalid.json`: Contains invalid videos from the non-overlap set

5. **Invalid Video Handling**: 
   - `load_xlsx.py` now identifies and separates invalid videos (those with shot transitions) into separate files.
   - It checks each video for shot transition labels using the same approach as `prepare_lighting_urls.py`.
   - Invalid videos are removed from the overlap/nonoverlap files and saved to their respective invalid files.
   - The file counts are updated accordingly.

## 2. Generating Lighting Project URLs

### Using `prepare_lighting_urls.py`

1. **Purpose**: Creates JSON files specifically for the lighting project.

2. **Command**:
   ```bash
   python -m caption.prepare_lighting_urls --json_path video_data/20250406lighting_only/videos.json --output_dir caption/video_urls/lighting_280_new
   ```

3. **Output Files**:
   - `caption/video_urls/lighting_280_new/lighting_only.json`: Contains lighting-specific videos
   - `caption/video_urls/lighting_280_new/invalid_videos.json`: Contains invalid videos (with shot transitions)
   - `caption/video_urls/lighting_280_new/all_labels.json`: Contains videos with all label collections

4. **File Naming Conventions**:
   - `lighting_only.json`: Contains all valid lighting videos
   - `invalid_videos.json`: Contains invalid videos (with shot transitions)
   - `all_labels.json`: Contains videos with all label collections

## 3. Processing New Videos

### Optional: Finding New Videos for File Padding

Before processing new videos, you might want to pad existing batch files to end with round numbers (e.g., ending with 0 instead of 3). This creates cleaner, more organized file naming.

#### **When and Why to Use This:**
- **Aesthetic Organization**: Files ending in round numbers (e.g., `1180_to_1190.json`) look cleaner than odd endings (e.g., `1180_to_1183.json`)
- **Future Consistency**: Ensures all future batches will naturally align to round numbers
- **No Duplicates**: Need genuinely new videos, not duplicates from existing sets

#### **Usage:**
```bash
# For overlap videos
python -m caption.find_new_videos caption/video_urls/20250912_setup_and_motion/ --mode overlap

# For nonoverlap videos  
python -m caption.find_new_videos caption/video_urls/20250912_setup_and_motion/ --mode nonoverlap
```

#### **How It Works:**
1. **Automatic Detection**: Finds `overlap_all_*.json` or `nonoverlap_all_*.json` in the directory
2. **Smart Analysis**: Reads your current `main_config.py` to find the last batch number for the specified mode
3. **Gap Calculation**: Determines exactly how many videos are needed to round up to the nearest 10
4. **File Creation**: Creates a single, clearly named padding file with the exact videos needed

#### **Possible Outcomes:**

**Case 1: Padding Needed**
If your last file is `1180_to_1183.json` (needs 7 videos to reach 1190):
```
=== Created file for nonoverlap mode ===
File: caption/video_urls/20250912_setup_and_motion/nonoverlap_padding_7_videos.json
Contains: 7 videos for padding from 1183 to 1190
Note: 326 additional new videos available for future batches

=== Next steps ===
1. Add the 7 videos from caption/video_urls/20250912_setup_and_motion/nonoverlap_padding_7_videos.json
   to your current file: 1180_to_1183.json
2. Rename that file to: 1180_to_1190.json
3. Update main_config.py to reference the new filename
4. Run your process_new_videos script which will start from 1190

Details:
- Current: 1180_to_1183.json has 3 videos (positions 1180 to 1182)
- After padding: 1180_to_1190.json will have 10 videos (positions 1180 to 1189)
```

**Case 2: No Padding Needed**
If your last file already ends with 0 (e.g., `1510_to_1520.json`):
```
✓ No padding needed for nonoverlap mode - already ends with 0!
✓ Your nonoverlap batches are perfectly aligned
✓ You can proceed directly with your process_new_videos script

ℹ️  Available for future batches: 1513 new videos
   Saved to: nonoverlap_future_1513_videos.json
```

#### **After Finding New Videos (If Padding Needed):**
1. **Copy the videos**: Copy the videos from the generated `*_padding_X_videos.json` file
2. **Add to current file**: Paste them into your current batch file (e.g., `1180_to_1183.json`)
3. **Rename the file**: Change the filename to end with the target round number (e.g., `1180_to_1190.json`)
4. **Update main_config.py**: Update the `DEFAULT_VIDEO_URLS_FILES` list to reference the new filename:
   ```python
   # Change this line:
   'video_urls/20250406_setup_and_motion/1180_to_1183.json',
   # To this:
   'video_urls/20250406_setup_and_motion/1180_to_1190.json',
   ```
5. **Future batches will align**: Next files will be perfectly aligned to round numbers

### Creating Shell Scripts in `process_new_videos/`

1. **Purpose**: Process new videos and create batch files while considering existing videos.

2. **Important Note**: The script must be called **separately** for overlap and nonoverlap sets to avoid number conflicts. Never mix overlap and nonoverlap files in the same `--batch-files` argument.

3. **Script Structure**:
   ```bash
   #!/bin/bash
   
   # Process new videos from the dataset
   python caption/process_new_videos.py \
       --new-dir "caption/video_urls/NEW_DIRECTORY" \
       --valid-filename "VALID_FILENAME.json" \
       --invalid-filename "FULL_PATH_TO_INVALID_FILE.json" \
       --invalid-filename-overlap "FULL_PATH_TO_OVERLAP_INVALID_FILE.json" \
       --invalid-filename-nonoverlap "FULL_PATH_TO_NONOVERLAP_INVALID_FILE.json" \
       --batch-files \
           "FULL_PATH_TO_BATCH1.json" \
           "FULL_PATH_TO_BATCH2.json" \
           ... \
       --batch-size 10 \
       --naming-mode [batch|overlap|nonoverlap]
   ```

4. **Parameters**:
   - `--new-dir`: Directory for new batch files
   - `--valid-filename`: Filename for valid videos in the new directory
   - `--invalid-filename`: Full path to the invalid file (optional)
   - `--invalid-filename-overlap`: Full path to the overlap invalid file (optional)
   - `--invalid-filename-nonoverlap`: Full path to the nonoverlap invalid file (optional)
   - `--batch-files`: Full paths to existing batch files (optional) - **MUST be only overlap OR only nonoverlap files, never mixed**
   - `--batch-size`: Number of videos per batch
   - `--naming-mode`: Naming convention for batch files

5. **Example Scripts**:

   **For Overlap Videos** (`overlap_september_11.sh`):
   ```bash
   #!/bin/bash
   
   # Process new overlapping videos from the September dataset
   python caption/process_new_videos.py \
       --new-dir "caption/video_urls/20250911_setup_and_motion" \
       --valid-filename "overlap_all_XXX.json" \
       --invalid-filename "caption/video_urls/20250911_setup_and_motion/overlap_invalid.json" \
       --batch-files \
           "caption/video_urls/20250227_0507ground_and_setup/overlap_0_to_94.json" \
           "caption/video_urls/20250227_0507ground_and_setup/overlap_94_to_188.json" \
           ... (all overlap files only) \
           "caption/video_urls/20250406_setup_and_motion/overlap_1010_to_1020.json" \
       --batch-size 10 \
       --naming-mode overlap
   ```

   **For Nonoverlap Videos** (`nonoverlap_september_11.sh`):
   ```bash
   #!/bin/bash
   
   # Process new non-overlapping videos from the September dataset  
   python caption/process_new_videos.py \
       --new-dir "caption/video_urls/20250911_setup_and_motion" \
       --valid-filename "nonoverlap_all_XXX.json" \
       --invalid-filename "caption/video_urls/20250911_setup_and_motion/nonoverlap_invalid.json" \
       --batch-files \
           "caption/video_urls/20250406_setup_and_motion/0_to_10.json" \
           "caption/video_urls/20250406_setup_and_motion/10_to_20.json" \
           ... (all nonoverlap files only) \
           "caption/video_urls/20250406_setup_and_motion/1180_to_1190.json" \
       --batch-size 10 \
       --naming-mode nonoverlap
   ```

6. **Expected Results**:
   - **Overlap files**: Will continue from 1020 → `overlap_1020_to_1030.json`, `overlap_1030_to_1040.json`, etc.
   - **Nonoverlap files**: Will continue from 1190 → `1190_to_1200.json`, `1200_to_1210.json`, etc.

7. **After Running Scripts**:
   
   **Step 1: Update Configuration**
   Add the new batch files to `caption/config/main_config.py` in the `DEFAULT_VIDEO_URLS_FILES` list:
   ```python
   DEFAULT_VIDEO_URLS_FILES = [
       # ... existing files ...
       'video_urls/20250406_setup_and_motion/overlap_1010_to_1020.json',
       # Add new overlap files:
       'video_urls/20250911_setup_and_motion/overlap_1020_to_1030.json',
       'video_urls/20250911_setup_and_motion/overlap_1030_to_1040.json',
       # ... existing nonoverlap files ...
       'video_urls/20250406_setup_and_motion/1180_to_1190.json',
       # Add new nonoverlap files:
       'video_urls/20250911_setup_and_motion/1190_to_1200.json',
       'video_urls/20250911_setup_and_motion/1200_to_1210.json',
       # Add invalid files if they exist:
       'video_urls/20250911_setup_and_motion/overlap_invalid.json',
       'video_urls/20250911_setup_and_motion/nonoverlap_invalid.json',
   ]
   ```

   **Step 2: Verify File Structure**
   Ensure your directory structure looks like:
   ```
   caption/video_urls/20250911_setup_and_motion/
   ├── overlap_all_XXX.json          # Original file from load_xlsx.py
   ├── nonoverlap_all_XXX.json       # Original file from load_xlsx.py
   ├── overlap_1020_to_1030.json     # New batch files
   ├── overlap_1030_to_1040.json
   ├── 1190_to_1200.json
   ├── 1200_to_1210.json
   ├── overlap_invalid.json          # Invalid files (if any)
   └── nonoverlap_invalid.json
   ```

   **Step 3: Test Configuration**
   Test that your web application can load the new files:
   ```bash
   python -m streamlit run caption/apps/app.py --server.port 5191
   ```

8. **Critical Notes**:
   - **Never mix overlap and nonoverlap** files in the same script call
   - **Run scripts separately** for each type (overlap vs nonoverlap)
   - **Update main_config.py** after creating new batch files
   - **The script preserves existing video sets** - only adds truly new videos
   - **File ordering matters** - maintain chronological order in the config file

## 4. Updating Web Applications

### For Main Project (Main Config)

1. **Location**: `caption/config/main_config.py`

2. **Update Process**:
   - Open `caption/config/main_config.py`
   - Find the `DEFAULT_VIDEO_URLS_FILES` list
   - Add the new batch files from the reminder output
   - Save the file

3. **Example**:
   ```python
   DEFAULT_VIDEO_URLS_FILES = [
       'video_urls/20250227_0507ground_and_setup/overlap_0_to_94.json',
       # ... existing files ...
       'video_urls/20250406_setup_and_motion/overlap_940_to_1034.json',
       'video_urls/20250406_setup_and_motion/overlap_1034_to_1128.json',
   ]
   ```

### For Lighting Project (Lighting Config)

1. **Location**: `caption/config/lighting_config.py`

2. **Update Process**:
   - Open `caption/config/lighting_config.py`
   - Find the `LIGHTING_VIDEO_URLS_FILES` list
   - Add the new batch files from the reminder output
   - Save the file

3. **Example**:
   ```python
   LIGHTING_VIDEO_URLS_FILES = [
       'video_urls/lighting_120_new/batch1.json',
       # ... existing files ...
       'video_urls/lighting_280_new/batch11.json',
       'video_urls/lighting_280_new/batch12.json',
   ]
   ```

## 5. Complete Workflow Example

### For Main Project:

1. Generate URLs:
   ```bash
   python caption/load_xlsx.py --video_data video_data/20250406_setup_and_motion/videos.json
   ```

2. Process new videos:
   ```bash
   chmod +x caption/process_new_videos/main_april_15.sh
   ./caption/process_new_videos/main_april_15.sh
   ```

3. Update configuration:
   - Add the new files to `DEFAULT_VIDEO_URLS_FILES` in `caption/config/main_config.py`

### For Lighting Project:

1. Generate URLs:
   ```bash
   python prepare_lighting_urls.py --json_path video_data/20250406lighting_only/videos.json --output_dir caption/video_urls/lighting_280_new
   ```

2. Process new videos:
   ```bash
   chmod +x caption/process_new_videos/lighting_april_16.sh
   ./caption/process_new_videos/lighting_april_16.sh
   ```

3. Update configuration:
   - Add the new files to `LIGHTING_VIDEO_URLS_FILES` in `caption/config/lighting_config.py`

## 6. Important Notes

1. **File Paths**: Always use full paths for batch files and invalid filename in shell scripts.

2. **Naming Modes**:
   - `batch`: Creates files like `batch1.json`, `batch2.json`, etc.
   - `overlap`: Creates files like `overlap_0_to_94.json`, `overlap_94_to_188.json`, etc.
   - `nonoverlap`: Creates files like `0_to_94.json`, `94_to_188.json`, etc.

3. **Reminder Output**: The script will output a reminder with the new files that need to be added to the feedback app.

4. **Invalid Files**: The script will copy the invalid files to the new directory with the same filenames.

## 7. Recent Improvements

1. **Invalid Video Handling in `load_xlsx.py`**: 
   - `load_xlsx.py` now identifies and separates invalid videos (those with shot transitions) into separate files.
   - It uses the same approach as `prepare_lighting_urls.py` to check for shot transition labels.
   - The implementation:
     - Checks each video for shot transition labels
     - Moves videos with shot transitions to `overlap_invalid.json` or `nonoverlap_invalid.json`
     - Removes these videos from the overlap/nonoverlap files
     - Updates the file counts accordingly

2. **Enhanced `process_new_videos.py`**:
   - Added support for processing overlap and nonoverlap invalid files
   - New command-line arguments:
     - `--invalid-filename-overlap`: For specifying the path to overlap invalid videos
     - `--invalid-filename-nonoverlap`: For specifying the path to nonoverlap invalid videos
   - The script now handles all three types of invalid files (general, overlap, and nonoverlap) 