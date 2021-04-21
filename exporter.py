from colorama import Fore, init


class AsciiExporter:
    @staticmethod
    def _get_unit_dict(units):
        res = dict()
        id = 1
        for unit in units:
            setattr(unit, 'id', id)
            res[(unit.x, unit.y)] = unit
            id += 1
        return res

    @staticmethod
    def _create_color_dict(units):
        colors = [Fore.RED, Fore.BLUE, Fore.GREEN, Fore.YELLOW]
        teams = list(set(u.team for u in units))
        return {t: c for t, c in zip(teams, colors)}

    @staticmethod
    def export(state, file_name=None):
        grid_line = '+---' * state.board_dimensions[0] + '+'
        result = [grid_line]
        unit_dict = AsciiExporter._get_unit_dict(state.units)
        colors = AsciiExporter._create_color_dict(state.units)
        for y in range(state.board_dimensions[1]):
            temp = ''
            for x in range(state.board_dimensions[0]):
                if (x, y) in unit_dict:
                    unit = unit_dict[(x, y)]
                    id_str = AsciiExporter._pad_to_three(unit.id)
                    if file_name:
                        temp += f'|{id_str}'
                    else:
                        temp += f'|{colors[unit.team]}{id_str}{Fore.RESET}'
                else:
                    temp += '|   '
            result.append(temp + '|')
            result.append(grid_line)
        if file_name:
            result.append('\n' + AsciiExporter._legend(state.units))
        else:
            result.append('\n' + AsciiExporter._legend(state.units, colors))
        result = '\n'.join(result)
        if file_name:
            AsciiExporter._export_to_file(file_name, result)
        return result

    @staticmethod
    def _legend(units, color_dict=None):
        if color_dict:
            return '\n'.join(f'{color_dict[u.team]}{u.id}{Fore.RESET}: {u}' for u in units)
        return '\n'.join(f'{u.id}: {u}' for u in units)
            
        
    @staticmethod
    def _pad_to_three(unit_id):
        id_str = str(unit_id)
        spaces_left = 3 - len(id_str)
        return ' ' * (spaces_left // 2) + id_str + ' ' * (spaces_left - spaces_left // 2)

    @staticmethod
    def _export_to_file(filename, output):
        with open(filename, 'w') as f:
            f.write(output)
