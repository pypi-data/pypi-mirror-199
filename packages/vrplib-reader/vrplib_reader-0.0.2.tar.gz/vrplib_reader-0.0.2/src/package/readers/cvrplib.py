from dataclasses import dataclass
from enum import Enum
from math import ceil
import os

from ..interfaces import Read
from .reader import Reader


@dataclass
class InstanceMapActions(Enum):
    Header = 1,
    Coords = 2,
    Demands = 3,
    Depot = 4


@dataclass
class SolutionMapActions(Enum):
    Route = 1,
    Cost = 2


class ReaderCVRPLib(Reader):
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.file_path})'

    def clean_line(self, line: str) -> str:
        return line.strip().replace('\n', '')

    def map_header_line(self, line: str) -> tuple[str, str]:
        if (':' not in line):
            return line.strip(), ''

        key, value = line.split(':', 1)
        return key.strip(), value.strip()

    def map_coords_line(self, line: str) -> tuple[float, float]:
        _, x, y = line.split(' ')
        return float(x), float(y)

    def map_demands_line(self, line: str) -> int:
        _, demand = line.split(' ')
        return int(demand)

    def map_depot_line(self, line: str) -> int:
        return int(line)

    def map_solution_line(self, line: str) -> tuple[int, ...]:
        _, value = line.split(':', 1)
        return tuple(map(int, value.strip().split(' ')))

    def map_solution_cost(self, line: str) -> int:
        _, value = line.split(' ', 1)
        return int(value)

    def do_instance_action(
            self,
            action: InstanceMapActions,
            line: str,
            result: Read) -> None:

        print(action == InstanceMapActions.Demands)

        if action is InstanceMapActions.Header:
            key, value = self.map_header_line(line)

            if key in self.optional_keys:
                result['optional_data'][key] = value

            if key == 'CAPACITY':
                result['vehicle_capacity'] = int(value)

        elif action is InstanceMapActions.Coords:
            result['coords'] += (self.map_coords_line(line),)

        elif action is InstanceMapActions.Demands:
            result['demands'] += (self.map_demands_line(line),)
        elif action is InstanceMapActions.Depot:
            if 'DEPOT_SECTION' not in result['optional_data']:
                result['optional_data']['DEPOT_SECTION'] = tuple()

            result['optional_data']['DEPOT_SECTION'] += (self.map_depot_line(
                line),)

    def do_solution_action(self, action: SolutionMapActions, line: str,
                           result: Read) -> None:
        if 'solution' not in result:
            result['solution'] = {
                'cost': 0,
                'routes': tuple()
            }

        if action is SolutionMapActions.Route:
            result['solution']['routes'] += (((result['depot'],) +
                                             self.map_solution_line(line)
                                             + (result['depot'],)),)

        elif action is SolutionMapActions.Cost:
            result['solution']['cost'] = self.map_solution_cost(line)

    def read(self) -> Read:
        try:
            path: str = os.path.join(os.getcwd(), str(self.file_path))
            result: Read = {
                'depot': 0,
                'nodes': tuple(),
                'clients': tuple(),
                'coords': tuple(),
                'demands': tuple(),
                'total_demand': 0,
                'vehicle_capacity': 0,
                'k_routes': 0,
                'tightness_ratio': 0.0,
                'optional_data': {}
            }

            with open(f'{path}.vrp', 'r') as file:
                instance_lines: list = file.readlines()
                instance_action: str = InstanceMapActions.Header.name

                for line in instance_lines:
                    instance_cleaned_line: str = self.clean_line(line)

                    if instance_cleaned_line == '':
                        continue
                    elif 'EOF' in instance_cleaned_line:
                        break
                    elif 'NODE_COORD_SECTION' in instance_cleaned_line:
                        instance_action = InstanceMapActions.Coords.name
                        continue
                    elif 'DEMAND_SECTION' in instance_cleaned_line:
                        instance_action = InstanceMapActions.Demands.name
                        continue
                    elif 'DEPOT_SECTION' in instance_cleaned_line:
                        instance_action = InstanceMapActions.Depot.name
                        continue

                    self.do_instance_action(
                        InstanceMapActions[instance_action],
                        instance_cleaned_line,
                        result)

            if self.with_solution:
                with open(f'{path}.sol', 'r') as file:
                    solution_lines: list = file.readlines()
                    solution_action: str = SolutionMapActions.Route.name

                    for line in solution_lines:
                        solution_cleaned_line: str = self.clean_line(line)

                        if solution_cleaned_line == '':
                            continue
                        elif 'EOF' in solution_cleaned_line:
                            break
                        else:
                            if 'Route' in solution_cleaned_line:
                                solution_action = SolutionMapActions.Route.name
                            elif 'Cost' in solution_cleaned_line:
                                solution_action = SolutionMapActions.Cost.name

                        self.do_solution_action(
                            SolutionMapActions[solution_action],
                            solution_cleaned_line,
                            result)

            result['nodes'] = tuple(range(0, len(result['coords'])))
            result['clients'] = result['nodes'][1:]
            result['total_demand'] = sum(result['demands'])
            result['k_routes'] = ceil(
                result['total_demand']/result['vehicle_capacity'])
            result['tightness_ratio'] = result['total_demand'] / \
                (result['k_routes'] * result['vehicle_capacity'])

            return result
        except FileNotFoundError:
            raise FileNotFoundError(
                f'File {self.file_path} not found')
