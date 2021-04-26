from colorama import Fore


class AsciiExporter:
    """
    Creates an AsciiExporter object. The AsciiExporter takes a state and creates a readable output that
    represents the current state of a game. Can be shown in both command line and in file output.
    """
    @staticmethod
    def _get_unit_dict(units):
        """
        Creates a dictionary of Units on the playing field by position and id.
        :param units: Units on the playing field.
        :return: A dictionary of Units with position and an id.
        """
        res = dict()
        for unit in units:
            res[(unit.x, unit.y)] = unit
        return res

    @staticmethod
    def _create_color_dict(state):
        """
        Creates a dictionary of teams mapped to colors.
        :param state: The State object of the game.
        :return: A dictionary with a team and color pairing.
        """
        colors = [Fore.RED, Fore.BLUE, Fore.GREEN, Fore.YELLOW]
        teams = list(set(u.team for u in state.original_units))
        return {t: c for t, c in zip(teams, colors)}

    @staticmethod
    def export(state, file_name=None):
        """
        Exports the output of a State to either the command line or an output file if one is given.
        :param state: The State of which the output it to be exported.
        :param file_name: Name of the file to which the output should be written. Output is written to command line if
        no file name is given.
        :return: A list of strings that comprise the output of a State.
        """
        grid_line = '+---' * state.board_dimensions[0] + '+'
        result = [grid_line]
        unit_dict = AsciiExporter._get_unit_dict(state.units)
        colors = AsciiExporter._create_color_dict(state)
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
        """
        Creates a legend so that it is shown which Units are on which team.
        :param units: A list of Units on the playing field.
        :param color_dict: A dictionary of teams mapped to colors.
        :return: Returns a legend with team colors for the command line if color_dict is given,
        a legend without team colors otherwise.
        """
        if color_dict:
            return '\n'.join(f'{color_dict[u.team]}{u.id}{Fore.RESET}: {u}' for u in units)
        return '\n'.join(f'{u.id}: {u}' for u in units)

    @staticmethod
    def _pad_to_three(unit_id):
        """
        Padds string of unit_id to three characters if necessary
        so that it is centered within a grid cell representation.
        :param unit_id: Id of Unit for which padding is checked and applied.
        :return: A string padded to three characters (if necessary) including unit_id.
        """
        id_str = str(unit_id)
        spaces_left = 3 - len(id_str)
        return ' ' * (spaces_left // 2) + id_str + ' ' * (spaces_left - spaces_left // 2)

    @staticmethod
    def _export_to_file(filename, output):
        """
        Exports State information and legend to the given file.
        :param filename: The file to which output is written.
        :param output: Output to be written in file.
        """
        with open(filename, 'w') as f:
            f.write(output)
