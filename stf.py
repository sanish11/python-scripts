import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Change to logging.INFO for less verbose logs
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("process_stf.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

REMOVE_KEYWORDS = [
    "SF_Rendition_Provider_Callout",
    "Total_Number_Of_Incomplete_Action_Plans",
    "SQX_User_Job_Function__c.compliancequest__Uniqueness_Constraint.FieldLabel",
    "SQX_SFC_VIEW_URL"
]

def escape_special_chars(text):
    return text.replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")

def process_stf_file(input_file, output_file, language_code, char_limit=38):
    """
    Process the .stf file and handle issues like character limits, duplicate keys, and unsupported elements.

    :param input_file: Path to the input .stf file.
    :param output_file: Path to save the processed file.
    :param language_code: Language code for appending translations (e.g., 'es', 'fr').
    :param char_limit: Maximum allowed character length for any field (default: 255).
    """
    try:
        logging.info(f"Starting processing: {input_file}")
        
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        processed_lines = []
        key_map = defaultdict(list)  # To track duplicate keys
        bilingual_started = False

        for line in lines:
            stripped_line = line.strip()

            # Check if the line contains any of the keywords to remove
            if any(keyword in stripped_line for keyword in REMOVE_KEYWORDS):
                logging.debug(f"Skipping line containing keyword: {stripped_line}")
                continue
            
            if stripped_line.startswith("Flow."):
                logging.debug(f"Skipped flow element: {stripped_line}")
                continue

            # Preserve comment lines or metadata lines
            if stripped_line.startswith("#") or stripped_line.lower().startswith("language code:") or stripped_line.lower().startswith("type:") or stripped_line.lower().startswith("translation type:"):
                processed_lines.append(stripped_line)
                logging.debug(f"Retaining metadata or comment line: {stripped_line}")
                continue
            

            # Match and process lines with the regex replacement logic
            match = re.match(r"^([^\t]+)\t([^\t]+)$", line.strip())
            if match:
                key, label = match.groups()
                replacement = f"{key}\t{escape_special_chars(label)}\t{escape_special_chars(label)} {language_code}\t- "
                parts = replacement.split("\t")
                if len(parts) >= 3:
                    if "FieldLabel" in key or "CrtColumn" in key or "WebTab" in key:
                    # Truncate the third part (label {language_code}) to 39 characters
                        parts[2] = parts[2][:39]
                    elif "RelatedListLabel" in key:
                    # Truncate the third part to 80 characters
                        parts[2] = parts[2][:80]
    
            # Reconstruct the line after truncation
                replacement = "\t".join(parts)

                processed_lines.append(replacement)
                logging.debug(f"Processed line with replacement: {replacement}")
            continue

            # Ignore comments or unsupported elements
            if line.strip().startswith("#") or not line.strip():
                logging.debug(f"Ignoring line: {line.strip()}")
                continue

        # Save the processed lines
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("\n".join(processed_lines) + "\n")

        logging.info(f"Processed file saved at: {output_file}")

    except Exception as e:
        logging.error(f"Error processing the file: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    # Command-line arguments
    parser = argparse.ArgumentParser(description="Process Salesforce Translation .stf files with issue handling.")
    parser.add_argument("input_file", help="Path to the input .stf file")
    parser.add_argument("output_file", help="Path to save the processed .stf file")
    parser.add_argument("language_code", help="Language code (e.g., 'es', 'fr')")
    parser.add_argument("--char_limit", type=int, default=255, help="Character limit for fields (default: 255)")

    args = parser.parse_args()

    # Process the file
    process_stf_file(args.input_file, args.output_file, args.language_code, args.char_limit)
