import pdfplumber
import pandas as pd
import numpy as np
import re
import argparse
import json
import os


def extract_tables_from_pdf(pdf_path, table_mapping):
    """
    Extract tables from specified pages of a PDF file using pdfplumber's line extraction.

    Args:
        pdf_path (str): Path to the PDF file
        table_mapping (dict): Mapping of page numbers to list of MapUnitIds

    Returns:
        pd.DataFrame: Combined DataFrame containing all extracted tables
    """
    tables = []

    with pdfplumber.open(pdf_path) as pdf:
        current_data = []
        current_class = None

        for page_num, mapunit_ids in table_mapping.items():
            page_num = int(page_num)

            # pdfplumber uses 0-based indexing
            page = pdf.pages[page_num - 1]

            # Get all lines from the page
            lines = page.extract_text_lines()

            for line in lines:
                text = line["text"].strip()

                # Skip empty lines
                if not text:
                    continue

                # Stop if we hit an appendix footer (e.g., "A - 6")
                if re.match(r"^[A-Z] - \d+$", text):
                    break

                # Skip the "Stand Table" header and other non-data lines
                if (
                    text
                    in [
                        "Stand Table",
                        "Lifeform Species Name Con Avg Min Max D Ch Ab Oft",
                        "January 2012",
                    ]
                    or "January" in text
                ):
                    continue

                # Check if this is a classification line
                if text in ["Tree", "Shrub", "Herb", "Nonvascular"]:
                    current_class = text
                    continue

                # Try to parse the data line
                parts = text.split()
                if len(parts) >= 5:  # Need at least species name and 4 numbers
                    try:
                        # Find where the numbers start
                        for i, part in enumerate(parts):
                            if re.match(r"^\d+(?:\.\d+)?$", part):
                                numeric_start = i
                                break
                        else:
                            continue

                        species_name = " ".join(parts[:numeric_start])
                        numbers = parts[numeric_start : numeric_start + 4]

                        # Convert numbers to float
                        con, avg, min_val, max_val = map(float, numbers)

                        for mapunit_id in mapunit_ids:
                            current_data.append(
                                {
                                    "MapUnit_ID": mapunit_id,  # Case to match jotr_geodatabase
                                    "Species": species_name,
                                    "Class": current_class,
                                    "Con": con,
                                    "Avg": avg,
                                    "Min": min_val,
                                    "Max": max_val,
                                }
                            )
                    except (ValueError, IndexError):
                        print(f"Failed to parse line in mapunit {mapunit_id}: {text}")
                        continue

            # Create DataFrame for this page if we have data
            if current_data:
                df = pd.DataFrame(current_data)
                tables.append(df)
                current_data = []  # Reset for next page
            print(f"Finished mapUnitId: {mapunit_id}")

    # Concatenate all DataFrames into one
    if tables:
        combined_df = pd.concat(tables, ignore_index=True)
    else:
        combined_df = pd.DataFrame()

    return combined_df


def clean_table(df):
    """
    Clean the extracted table by fixing data types and handling missing values.
    """
    # Convert numeric columns to float
    numeric_cols = ["Con", "Avg", "Min", "Max"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sort by Class and Species
    df = df.sort_values(["Class", "Species"])

    return df


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--pdf", help="Path to the PDF file", required=True)
    argparser.add_argument(
        "--table_mapping_json",
        help="Mapping of MapUnitId to the page containing the stand table",
        required=True,
    )
    argparser.add_argument(
        "--output_csv_dir",
        help="Path to dir to save the combined table as a CSV file",
        required=True,
    )

    args = argparser.parse_args()
    table_mapping_json = args.table_mapping_json

    output_csv_dir = args.output_csv_dir
    if not os.path.exists(output_csv_dir):
        os.makedirs(output_csv_dir)

    demo_name = os.getenv("DEMO_NAME")
    output_csv = os.path.join(output_csv_dir, f"{demo_name}.csv")

    with open(table_mapping_json, "r") as f:
        table_mapping = json.load(f)

    tables = extract_tables_from_pdf(args.pdf, table_mapping)

    if not tables.empty:
        tables = clean_table(tables)
        tables.to_csv(output_csv, index=False)
        print(
            f"Combined table saved to '{output_csv}' (according to DEMO_NAME set in `.devcontainer/env`: {demo_name})."
        )
    else:
        print("No tables extracted.")
