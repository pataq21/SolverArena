import json
import time
from ortools.math_opt.python import mathopt


def create_data(dataset_name):
    with open(f"datasets/{dataset_name}.json", "r") as file:
        data = json.load(file)

    group_sizes = [len(members) for members in data["group_people"].values()]
    table_capacities = data["table_capacities"]
    people_groups = {int(k): v for k, v in data["group_people"].items()}
    num_groups = len(people_groups.keys())
    num_tables = len(table_capacities)

    return num_groups, num_tables, group_sizes, table_capacities, people_groups


def build_model(num_groups, num_tables, group_sizes, table_capacities, people_groups):
    # Crear el solver usando GLOP
    model = mathopt.Model(name="getting_started_lp")
    people = [p for group in people_groups.values() for p in group]

    # Variables
    print("Variable 1")
    assignment = {
        (p, t): model.add_variable(lb=0, ub=1, name=f"assignment_{p}_{t}") for p in people for t in range(num_tables)
    }
    print("Variable 2")
    group_present = {
        (g, t): model.add_variable(lb=0, ub=1, name=f"group_present_{g}_{t}")
        for g in range(num_groups)
        for t in range(num_tables)
    }

    # Variable para contar grupos divididos
    print("Variable 3")
    group_split = {g: model.add_variable(lb=0, ub=1, name=f"group_split_{g}") for g in range(num_groups)}
    print(len(group_split.keys()) + len(group_present.keys()) + len(assignment.keys()))
    # Función objetivo: Minimizar el número de grupos divididos
    model.minimize(sum(group_split[g] for g in range(num_groups)))

    # Restricciones
    count = 0
    # Cada persona debe ser asignada a exactamente una mesa
    print("Constraint 1")
    for p in people:
        model.add_linear_constraint(sum(assignment[p, t] for t in range(num_tables)) == 1)
        count += 1

    # La capacidad de las mesas no puede ser excedida
    print("Constraint 2")

    for t in range(num_tables):
        model.add_linear_constraint(sum(assignment[p, t] for p in people) <= table_capacities[t])
        count += 1

    # Cada grupo debe ser completamente asignado a una o más mesas
    print("Constraint 3")
    for g in range(num_groups):
        model.add_linear_constraint(
            sum(assignment[p, t] for p in people_groups[g + 1] for t in range(num_tables)) == group_sizes[g]
        )
        count += 1

    # If a group is at a table, the group_present variable must be 1
    print("Constraint 4")
    for g in range(num_groups):
        for t in range(num_tables):
            model.add_linear_constraint(
                sum(assignment[p, t] for p in people_groups[g + 1]) <= table_capacities[t] * group_present[g, t]
            )
            count += 1

    # Detectar si un grupo ha sido dividido
    print("Constraint 5")
    for g in range(num_groups):
        model.add_linear_constraint(
            sum(group_present[g, t] for t in range(num_tables)) - 1 <= num_tables * group_split[g]
        )
    print(count)
    return model


def main(filename):
    num_groups, num_tables, group_sizes, table_capacities, people_groups = create_data(filename)
    start_model_time = time.time()
    solver = build_model(num_groups, num_tables, group_sizes, table_capacities, people_groups)
    end_model_time = time.time()
    model_construction_time = end_model_time - start_model_time

    # Medir el tiempo de resolución
    start_time = time.time()
    params = mathopt.SolveParameters(enable_output=True)
    result = mathopt.solve(solver, mathopt.SolverType.GUROBI, params=params)
    end_time = time.time()
    execution_time = end_time - start_time

    # Imprimir resultados
    print("MathOpt solve succeeded")
    print("Objective value:", result.objective_value())
    print("Time to build model:", model_construction_time)
    print("Time to solve:", execution_time)


if __name__ == "__main__":
    filename = "dataset1000b"
    main(filename)
