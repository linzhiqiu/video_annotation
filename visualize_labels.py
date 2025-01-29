import os
import json

# Mapping JSON field names to human-readable names
FIELD_MAPPING = {
    "label_name": "Label Name",
    "def_question": "Question (Definition)",
    "alt_question": "Alternative Question",
    "def_prompt": "Prompt (Definition)",
    "alt_prompt": "Alternative Prompt",
    "pos_rule_str": "Positive",
    "neg_rule_str": "Negative",
    "easy_neg_rule_str": "Negative (Easy)",
    "hard_neg_rule_str": "Negative (Hard)"
}

def load_json(file_path):
    """Load a JSON file and return its content."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def process_json_file(file_path):
    """Convert a single JSON label file into a GitHub-friendly collapsible Markdown section."""
    entry = load_json(file_path)
    label = entry["label"]

    # Start collapsible section for the label
    markdown_content = [f"<details>\n<summary><b>{label}</b></summary>\n"]

    # Add Label Name (Styled with 🔵 Emoji)
    label_name = entry.get("label_name", "")
    markdown_content.append(f"\n**🔵 Label Name:** `{label_name}`  \n")

    for json_key, display_name in FIELD_MAPPING.items():
        if json_key in entry and json_key != "label_name" and entry[json_key]:
            field_content = entry[json_key]

            if isinstance(field_content, dict):  # Handle dictionary fields
                markdown_content.append(f'<details>\n<summary><b>🟠 {display_name}</b></summary>\n')
                for key, value in field_content.items():
                    markdown_content.append(f"- **{key}**: `{value}`  \n")
                markdown_content.append("</details>\n")

            elif isinstance(field_content, list):  # Handle list fields
                markdown_content.append(f'<details>\n<summary><b>🟠 {display_name}</b></summary>\n')
                for item in field_content:
                    markdown_content.append(f"- {item}  \n")
                markdown_content.append("</details>\n")

            else:  # Handle string fields (Rules & Others)
                emoji = "🟢" if "pos_rule" in json_key else "🔴" if "neg_rule" in json_key else "🔵"
                markdown_content.append(f"**{emoji} {display_name}:** `{field_content}`  \n")

    markdown_content.append("</details>\n")  # Close outer label collapse
    return "\n".join(markdown_content)




def generate_folder_markdown(folder_path):
    """
    Given a folder, returns markdown content including:
    (1) All labels (fully rendered Markdown with collapsible sections)
    (2) Links to subfolders pointing to their index.md
    """
    folder_name = os.path.basename(folder_path)
    markdown_content = [f"# {folder_name.capitalize()} Overview\n"]

    subfolder_links = []
    label_sections = []

    for item in sorted(os.listdir(folder_path)):
        item_path = os.path.join(folder_path, item)

        if item.endswith(".json"):  # Process JSON label files
            label_sections.append(process_json_file(item_path))

        elif os.path.isdir(item_path):  # Add subfolder links
            subfolder_links.append(f"- [{item.capitalize()}](./{item}/index.md)")

    # Embed all label Markdown sections
    if label_sections:
        markdown_content.append("\n".join(label_sections))

    # Add subcategories section if present
    if subfolder_links:
        markdown_content.append("\n## Subcategories\n")
        markdown_content.append("\n".join(subfolder_links))

    return "\n".join(markdown_content)

def process_labels_directory(input_dir, output_dir):
    """Recursively processes the labels/ directory and generates Markdown in labels_markdown/."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for folder_name in sorted(os.listdir(input_dir)):
        folder_path = os.path.join(input_dir, folder_name)
        output_folder_path = os.path.join(output_dir, folder_name)

        if os.path.isdir(folder_path):
            os.makedirs(output_folder_path, exist_ok=True)

            # Generate markdown for this folder
            markdown_text = generate_folder_markdown(folder_path)

            # Save the index.md file
            index_path = os.path.join(output_folder_path, "index.md")
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(markdown_text)

            # Recursively process subfolders
            process_labels_directory(folder_path, output_folder_path)

if __name__ == "__main__":
    LABELS_DIR = "labels"
    MARKDOWN_OUTPUT_DIR = "labels_markdown"

    print(f"Processing '{LABELS_DIR}' into '{MARKDOWN_OUTPUT_DIR}'...")
    process_labels_directory(LABELS_DIR, MARKDOWN_OUTPUT_DIR)
    print("✅ Markdown generation complete!")
