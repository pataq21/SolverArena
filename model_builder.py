import json
from pyomo.environ import *


def create_data(dataset_name):
    with open(f"datasets/{dataset_name}.json", "r") as file:
        data = json.load(file)

    group_sizes = [len(members) for members in data["group_people"].values()]
    sum(group_sizes)
    table_capacities = data["table_capacities"]
    people_groups = {int(k): v for k, v in data["group_people"].items()}
    num_groups = len(people_groups.keys())
    num_tables = len(table_capacities)

    return num_groups, num_tables, group_sizes, table_capacities, people_groups


def build_model(num_groups, num_tables, group_sizes, table_capacities, people_groups):
    model = ConcreteModel()

    # Sets
    model.Groups = RangeSet(num_groups)
    model.Tables = RangeSet(num_tables)
    model.People = Set(initialize=[p for group in people_groups.values() for p in group])

    # Parameters
    model.group_size = Param(model.Groups, initialize=lambda model, g: group_sizes[g - 1])
    model.table_capacity = Param(model.Tables, initialize=lambda model, t: table_capacities[t - 1])
    model.person_to_group = Param(
        model.People, initialize=lambda model, p: next(g for g, people in people_groups.items() if p in people)
    )

    # Decision Variables
    print("Variable 1")
    model.assignment = Var(model.People, model.Tables, domain=Binary)
    print("Variable 2")
    model.group_split = Var(model.Groups, domain=Binary)
    print("Variable 3")
    model.group_present = Var(model.Groups, model.Tables, domain=Binary)  # New binary variable

    # Objective Function
    model.objective = Objective(expr=sum(model.group_split[g] for g in model.Groups), sense=minimize)

    # Constraints

    # Each person must be assigned to exactly one table
    print("Constraint 1")

    def person_assignment_constraint(model, p):
        return sum(model.assignment[p, t] for t in model.Tables) == 1

    model.person_assignment_constraint = Constraint(model.People, rule=person_assignment_constraint)

    # The capacity of the tables cannot be exceeded
    print("Constraint 2")

    def table_capacity_constraint(model, t):
        return sum(model.assignment[p, t] for p in model.People) <= model.table_capacity[t]

    model.table_capacity_constraint = Constraint(model.Tables, rule=table_capacity_constraint)

    # Each group must be completely assigned to one or more tables
    print("Constraint 3")

    def group_assignment_constraint(model, g):
        return (
            sum(model.assignment[p, t] for p in model.People if model.person_to_group[p] == g for t in model.Tables)
            == model.group_size[g]
        )

    model.group_assignment_constraint = Constraint(model.Groups, rule=group_assignment_constraint)

    # New constraint: If a group is at a table, the group_present variable must be 1
    print("Constraint 4")

    def group_presence_constraint(model, g, t):
        return (
            sum(model.assignment[p, t] for p in model.People if model.person_to_group[p] == g)
            <= model.table_capacity[t] * model.group_present[g, t]
        )

    model.group_presence_constraint = Constraint(model.Groups, model.Tables, rule=group_presence_constraint)

    # Constraint to detect if a group has been split
    print("Constraint 5")

    def group_split_constraint(model, g):
        return sum(model.group_present[g, t] for t in model.Tables) - 1 <= model.group_split[g] * len(
            model.Tables.value
        )

    model.group_split_constraint = Constraint(model.Groups, rule=group_split_constraint)

    return model


def main(dataset_name):
    num_groups, num_tables, group_sizes, table_capacities, people_groups = create_data(dataset_name)
    model = build_model(num_groups, num_tables, group_sizes, table_capacities, people_groups)
    model.write(f"mps_files/model_{dataset_name}.mps", io_options={"symbolic_solver_labels": True})
    print("done")


if __name__ == "__main__":
    dataset_name = "dataset100"
    main(dataset_name)
