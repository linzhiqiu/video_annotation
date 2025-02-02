import os
import json
from label import Label

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
    """Convert a single JSON label file into a GitHub-friendly collapsible Markdown section with font sizes."""
    entry = load_json(file_path)
    label = entry["label"]

    # Start collapsible section for the label
    markdown_content = [f"<details>\n<summary><h2>{label}</h2></summary>\n"]

    # Add Label Name (H3 for Larger Font)
    label_name = entry.get("label_name", "")
    markdown_content.append(f"\n<h3>🔵 Label Name:</h3>\n<code>{label_name}</code>\n")

    # Extract the first definition from def_question (if available)
    def_question = entry.get("def_question", [])
    if def_question:
        definition = def_question[0]  # First item in def_question
        markdown_content.append(f"\n<h3>📖 Definition:</h3>\n{definition}\n")

    for json_key, display_name in FIELD_MAPPING.items():
        if json_key in entry and json_key != "label_name" and entry[json_key]:
            field_content = entry[json_key]

            if isinstance(field_content, dict):  # Handle dictionary fields
                markdown_content.append(f'<details>\n<summary><h4>🔴 {display_name}</h4></summary>\n')
                for key, value in field_content.items():
                    markdown_content.append(f"- <b>{key}</b>: <code>{value}</code>\n")
                markdown_content.append("</details>\n")

            elif isinstance(field_content, list):  # Handle list fields
                # Special handling for def_question (so that it's not duplicated)
                if json_key == "def_question":
                    markdown_content.append(f'<details>\n<summary><h4> Question (Definition)</h4></summary>\n')
                    for item in field_content[1:]:  # Exclude the first definition
                        markdown_content.append(f"- {item}\n")
                    markdown_content.append("</details>\n")
                else:
                    markdown_content.append(f'<details>\n<summary><h4> {display_name}</h4></summary>\n')
                    for item in field_content:
                        markdown_content.append(f"- {item}\n")
                    markdown_content.append("</details>\n")

            else:  # Handle string fields (Rules & Others)
                emoji = "🟢" if "pos_rule" in json_key else "🔴" if "neg_rule" in json_key else "🔵"
                markdown_content.append(f"<h4>{emoji} {display_name}:</h4>\n<code>{field_content}</code>\n")

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
    
    # Load all labels with nested structure
    labels = Label.load_all_labels()
    
    # Print the entire label hierarchy
    # print("\nLabel Hierarchy:")
    # print(labels)

    print(f"Processing '{LABELS_DIR}' into '{MARKDOWN_OUTPUT_DIR}'...")
    process_labels_directory(LABELS_DIR, MARKDOWN_OUTPUT_DIR)
    print("✅ Markdown generation complete!")
