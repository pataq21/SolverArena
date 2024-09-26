import json
import random


def generate_dictionary_and_list(n):
    # Generate the table capacities, ensuring they sum to n
    table_capacities = []
    remaining = n

    while remaining > 0:
        if remaining <= 3:  # Ensure no tables have a capacity smaller than 1
            table_capacities.append(remaining)
            break

        # Choose a random size for the table between 1 and min(remaining, 10)
        capacity = random.randint(1, min(remaining, 10))
        table_capacities.append(capacity)
        remaining -= capacity

    # Generate the dictionary of people assigned to tables
    group_people = {}
    person_id = 1
    remaining_people = n
    index = 1
    while remaining_people > 0:
        if remaining_people <= 3:  # Ensure no groups have a size smaller than 1
            group_people[index] = list(range(person_id, person_id + remaining_people))
            break

        # Choose a random size for the group between 1 and min(remaining, 10)
        group_size = random.randint(1, min(remaining_people, 10))
        group_people[index] = list(range(person_id, person_id + group_size))
        person_id += group_size
        remaining_people -= group_size
        index += 1

    return {"table_capacities": table_capacities, "group_people": group_people}


if __name__ == "__main__":
    total_people = 6000
    dataset = generate_dictionary_and_list(total_people)
    with open(f"datasets/dataset{total_people}b.json", "w") as json_file:
        json.dump(dataset, json_file, indent=4)
