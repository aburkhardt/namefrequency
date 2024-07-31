
from config import config

from get_datasets import get_data

###basic framework for checking within the dataset
def calculate_name_score(name, dataset):
    """Calculates the score of a name based on its frequency in the dataset."""
    total_frequency = sum(dataset.values())
    
    if name in dataset:
        name_frequency = dataset[name]
        score = name_frequency / total_frequency
        return score
    else:
        return 0  # If the name is not in the dataset, return a score of 0
    
def process_dataset(data):
    """Processes data to create frequency dictionaries for first names, last names, and full names."""
    first_name_dict = {}
    last_name_dict = {}
    full_name_dict = {}
    
    for entry in data:
        first_name = entry.get('FN', '').strip().lower()  # Normalize and trim
        last_name = entry.get('LN', '').strip().lower()  # Normalize and trim
        full_name = f"{first_name} {last_name}" if first_name and last_name else None

        if first_name:
            first_name_dict[first_name] = first_name_dict.get(first_name, 0) + 1
        if last_name:
            last_name_dict[last_name] = last_name_dict.get(last_name, 0) + 1
        if full_name:
            full_name_dict[full_name] = full_name_dict.get(full_name, 0) + 1

    return first_name_dict, last_name_dict, full_name_dict

def categorize_score(score):
    """batch scores into flag colors"""
    if score >= 0.007:
        return "red"
    elif score >= 0.003:
        return "yellow"
    else:
        return "green"

def main():
    # Get data from Google Sheets
    data = get_data(gbook=config['GOOGLE']['GBOOK'], sheet=config['GOOGLE']['SimplifiedDataset'])

    # Process data into frequency dictionaries for first names, last names, and full names
    first_name_dataset, last_name_dataset, full_name_dataset = process_dataset(data)

    # Example usage
    first_name_input = input("Enter a first name to check its score: ")
    last_name_input = input("Enter a last name to check its score: ")
    full_name_input = f"{first_name_input} {last_name_input}"

    # Normalize submitted names from first and last name
    first_name_to_check = first_name_input.strip().lower()
    last_name_to_check = last_name_input.strip().lower()
    full_name_to_check = f"{first_name_to_check} {last_name_to_check}"

    # Calculate scores
    first_name_score = calculate_name_score(first_name_to_check, first_name_dataset)
    last_name_score = calculate_name_score(last_name_to_check, last_name_dataset)
    full_name_score = calculate_name_score(full_name_to_check, full_name_dataset)

    # Calculate overall score
    overall_score = (first_name_score + last_name_score + full_name_score) / 3  # Average of all three scores

    # Categorize overall score
    score_category = categorize_score(overall_score)

    print(f"The score for the first name '{first_name_input}' is: {first_name_score}")
    print(f"The score for the last name '{last_name_input}' is: {last_name_score}")
    print(f"The score for the full name '{full_name_input}' is: {full_name_score}")
    print(f"The overall score for the combination is: {overall_score}")
    print(f"Score category: {score_category}")

if __name__ == "__main__":
    main()