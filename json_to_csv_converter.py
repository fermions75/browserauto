import json
import csv
import sys
from pathlib import Path

def convert_json_to_csv(json_file_path, csv_file_path=None):
    """
    Convert JSON file to CSV format with proper UTF-8 encoding
    """
    try:
        # Read the JSON file with UTF-8 encoding
        print(f"Reading JSON file: {json_file_path}")
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        if not data:
            print("No data found in JSON file")
            return False
        
        # Generate CSV filename if not provided
        if csv_file_path is None:
            json_path = Path(json_file_path)
            csv_file_path = json_path.with_suffix('.csv')
        
        print(f"Converting to CSV: {csv_file_path}")
        
        # Get all unique keys from all records to create comprehensive headers
        all_keys = set()
        for record in data:
            if isinstance(record, dict):
                all_keys.update(record.keys())
        
        # Sort keys for consistent column order
        fieldnames = sorted(list(all_keys))
        
        # Write to CSV with UTF-8 encoding
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write data rows
            for record in data:
                if isinstance(record, dict):
                    # Handle None values and ensure all fields are present
                    row = {}
                    for field in fieldnames:
                        value = record.get(field, '')
                        # Convert None to empty string for CSV
                        if value is None:
                            value = ''
                        # Ensure value is string
                        row[field] = str(value)
                    writer.writerow(row)
        
        print(f"Successfully converted {len(data)} records to CSV")
        print(f"CSV file saved as: {csv_file_path}")
        return True
        
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file_path}' not found")
        return False
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
        return False
    except Exception as e:
        print(f"Error converting to CSV: {e}")
        return False

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        print("Usage: python json_to_csv_converter.py <json_file> [csv_file]")
        print("Example: python json_to_csv_converter.py processed_user_data.json")
        print("Example: python json_to_csv_converter.py processed_user_data.json output.csv")
        return
    
    json_file = sys.argv[1]
    csv_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = convert_json_to_csv(json_file, csv_file)
    if success:
        print("Conversion completed successfully!")
    else:
        print("Conversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
