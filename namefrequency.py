###can we add in an API query to get the frequency nationwide?
#looks like it might be hard to find 


###basic framework for checking within the dataset
def calculate_name_score(name, dataset):
    total_frequency = sum(dataset.values())
    
    if name in dataset:
        name_frequency = dataset[name]
        score = name_frequency / total_frequency
        return score
    else:
        return 0  # If the name is not in the dataset, return a score of 0

# Example dataset (replace this with your actual data)
first_name_dataset = {
    'John': 150,
    'Jane': 100,
    'Bob': 50,
    # Add more names and frequencies as needed
}

last_name_dataset = {
    'Smith': 200,
    'Johnson': 150,
    'Doe': 50,
    # Add more last names and frequencies as needed
}

full_name_dataset = {
    'John Smith': 100,
    'Jane Smith': 100,
    'John Johnson': 50,
    'Jane Doe': 50
}

# Example usage
first_name_to_check = input("Enter a first name to check its score: ")
last_name_to_check = input("Enter a last name to check its score: ")
full_name_to_check = input("Enter a full name to check its score: ")

first_name_score = calculate_name_score(first_name_to_check, first_name_dataset)
last_name_score = calculate_name_score(last_name_to_check, last_name_dataset)
full_name_score = calculate_name_score(full_name_to_check, full_name_dataset)

overall_score = (first_name_score + last_name_score) / 2  # Simple average
fullname_score = (full_name_score)

print(f"The score for the first name '{first_name_to_check}' is: {first_name_score}")
print(f"The score for the last name '{last_name_to_check}' is: {last_name_score}")
print(f"The overall score for the combination is: {overall_score}")

