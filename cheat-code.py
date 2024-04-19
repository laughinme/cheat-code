import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
# from lxml import etree
import time


class Cell:
    def __init__(self, x, y, walls=0, color=False, point=False, finish=False, start=False) -> None:
        self.x = x
        self.y = y
        self.walls = walls
        self.color = color
        self.point = point
        self.finish = finish
        self.start = start
        self.visited = False
        

    def __repr__(self):
        if self.finish:
            return "Б"
        elif self.color:
            return "*"
        elif self.visited:
            return "?"

        elif self.point:
            return "+"
        elif self.start:
            return "А"

        else:
            return "·"


def parse_file(file):
    with open(file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    # Пропускаем комментарии и пустые строки
    lines = [line for line in lines if line.strip() and not line.startswith(';')]
    print(''.join(lines[2:]))
    
    field_size = tuple(map(int, lines[0].split()))
    
    field = [[Cell(x, y) for x in range(field_size[0])] for y in range(field_size[1])]
    # hashstr = '\n'.join([''.join(['#' for _ in range(field_size[0])]) for _ in range(field_size[1])])
    # print(hashstr)
    
    for line in lines[2:]:
        parts = line.split()
        x, y = map(int, parts[:2])
        walls = int(parts[2])
        point = parts[-1] == '1'
        finish = 'Б' in parts
        color = bool(int(parts[3]))
        field[y][x] = Cell(x, y, walls, color, point, finish)

    x, y = tuple(map(int, lines[1].split())) # start position
    cell = field[y][x]
    cell.start = True
    # print(field[y][x].start)

    # for y in range(len(field)):
    #     for x, cell in enumerate(field[y]):
    #         if cell==None:
    #             field[y][x] = Cell(x, y)
    
    return field


def has_wall(cell, direction):
    
    walls = {
        "left": [1, 3, 5, 7, 9, 11, 13, 15],
        "right": [2, 3, 6, 7, 10, 11, 14, 15],
        "up": [8, 9, 10, 11, 12, 13, 14, 15],
        "down": [4, 5, 6, 7, 12, 13, 14, 15],
    }
    return cell.walls in walls[direction]

def get_neighbors(cell, field):
    # print(cell)
    neighbors = {} # {neighbour: 'up'}
    rows = len(field)
    cols = len(field[0])
    
    directions = [('up', -1, 0, 'down'), ('down', 1, 0, 'up'), ('left', 0, -1, 'right'), ('right', 0, 1, 'left')]
    for direction, dy, dx, revdirection in directions:
        nx, ny = cell.x + dx, cell.y + dy
        # print(newcell.x, newcell.y)
        
        if 0 <= nx < cols and 0 <= ny < rows:
            newcell = field[ny][nx]
            if not has_wall(cell, direction) and not has_wall(newcell, revdirection):
                # print(cell.walls)

                neighbors[newcell] = direction
    
    return neighbors


def find_closest_cell(start, field, points=[], mode='point'):
    # if start.point:
    #     return start, [start]

    visited = set()
    queue = [(start, [], [start])] 

    while queue:
        current, directions, path = queue.pop(0) 
        visited.add((current.y, current.x))

        if (mode == 'point' and current in points) or (mode == 'finish' and current.finish):
            for cell in path[1:-1]: cell.visited =True
            return current, directions, path


        for neighbor, direction in get_neighbors(current, field).items():
            if ((neighbor.y, neighbor.x) not in visited): #or (cell.point and not cell.color)
                queue.append((neighbor, directions + [direction], path + [neighbor]))  
                visited.add((neighbor.y, neighbor.x))

        # print(queue)
        # print(visited)

    return start, [], []

def code_builder(commands):
    kumir = {
        'up' : 'вверх',
        'down' : 'вниз',
        'right' : 'вправо',
        'left' : 'влево',
        'paint' : 'закрасить',
    }
    code = [kumir[command] for command in commands]

    return '\n'.join(code)


def solver(file):

    with open(file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    # Пропускаем комментарии и пустые строки
    lines = [line for line in lines if line.strip() and not line.startswith(';')]
    # print(''.join(lines[2:]))
    
    field_size = tuple(map(int, lines[0].split()))
    
    field = [[Cell(x, y) for x in range(field_size[0])] for y in range(field_size[1])]
    # hashstr = '\n'.join([''.join(['#' for _ in range(field_size[0])]) for _ in range(field_size[1])])
    # print(hashstr)
    
    for line in lines[2:]:
        parts = line.split()
        x, y = map(int, parts[:2])
        walls = int(parts[2])
        point = parts[-1] == '1'
        finish = 'Б' in parts
        color = bool(int(parts[3]))
        field[y][x] = Cell(x, y, walls, color, point, finish)

    x, y = tuple(map(int, lines[1].split())) # start position
    cell = field[y][x]
    cell.start = True
    
    # for row in field:
    #     print(' '.join([str(cell) for cell in row]))
    # print('\n')

    points_to_paint = [cell for row in field for cell in row if cell.point and not cell.color]
    # print([cell for row in field for cell in row])
    current_cell = [cell for row in field for cell in row if cell.start][0]


    commands = []
    while points_to_paint:
        closest_point, directions, path = find_closest_cell(current_cell, field, points_to_paint, 'point')
        # print(closest_point, directions, path)
        if closest_point is None:
            break

        closest_point.color = True
        points_to_paint = [cell for cell in points_to_paint if not cell.color]
        current_cell = closest_point
        commands += directions + ['paint']

        # for row in field:
        #     print(' '.join([str(cell) for cell in row]))

        for row in field:
            for cell in row:
                cell.visited = False

    else: closest_point = current_cell

    closest_point, directions, path = find_closest_cell(closest_point, field, mode='finish')
    # print(closest_point, directions, path)
    commands += directions

    # for row in field:
    #     print(' '.join([str(cell) for cell in row]))

    return commands


def initializate(file_path: str):
    list_path = file_path.split('/')
    form = list_path[-1].split('.')

    def lesson_name_to_id(name: str):
        lesson_number, task_letter = name.split('-')
        
        lesson_number_int = int(lesson_number)
        
        # Преобразуем букву задания в порядковый номер в алфавите (A=1, B=2, ...)
        # ord('A') возвращает ASCII код буквы 'A', вычитаем его из ASCII кода интересующей буквы и добавляем 1
        task_number = ord(task_letter[0].upper()) - ord('A') + 1
        
        lesson_id = f"{lesson_number_int}{task_number:02}"
        
        return lesson_id

    def get_tasks_paths(file_path: str):
        # Загружаем и парсим XML-файл
        tree = ET.parse(file_path)
        worksheet = tree.getroot()

        # Находим элемент 'FILE' и извлекаем значение его атрибута 'fileName'
        file_element = worksheet.find('FILE')
        if file_element is not None:
            path = file_element.get('fileName')
            
            tree = ET.parse(path)
            practicesheet = tree.getroot()
            
            tasks_paths = {}
            for isp in practicesheet.findall(".//ISP"):
                envisps = isp.findall('ENV')
                for envisp in envisps:
                    if envisp is not None:
                        envisp = envisp.text.split('/')
                        lesson = envisp[-1].split('.')[0]
                        # print(lesson)
                        if not lesson[-1].isnumeric() or int(lesson[-1]) == min(int(envisp.text.split('/')[-1].split('.')[0][-1]) for envisp in envisps if envisp is not None): #envisps[0].text.split('/')[-1].split('.')[0][-1]
                            print(lesson)
                            tasks_paths['/'.join(list_path[:-1] + envisp)] = lesson_name_to_id(lesson if not lesson[-1].isnumeric() else lesson[:-1])


            return tasks_paths

        else:
            print('Элемент FILE не найден.')


    if 'work' == form[-2]:

        return get_tasks_paths(file_path), file_path
    
    elif 'kurs' == form[-2]:

        # Создаём корневой элемент
        course = ET.Element('COURSE')

        ET.SubElement(course, 'FILE', fileName=file_path)
        
        tree = ET.ElementTree(course)
        tree.write('worksheet.work.xml', encoding='utf-8', xml_declaration=True)

        worksheet_path = '/'.join(list_path[:-1] + ['worksheet.work.xml'])

        return get_tasks_paths(worksheet_path), worksheet_path


def create_worksheet_solutions(tasks_paths: dict, worksheet_path: str):
    #xml
    worktree = ET.parse(worksheet_path)
    root = worktree.getroot()

    # Создаем или находим элемент MARKS внутри COURSE
    marks_element = root.find('MARKS')
    if marks_element is None:  # Если элемент MARKS не найден, создаем его
        marks_element = ET.SubElement(root, 'MARKS')


    times = []
    for path, xmlid in tasks_paths.items():
        
        start_time = time.time()
        commands = code_builder(solver(path))
        end_time = time.time()
        #lxml
        code = "использовать Робот&#xa;алг Миссия&#xa;нач|@protected&#xa;" + '&#xa;'.join(commands.split('\n')) + "&#xa;кон|@protected"
        #xml
        ET.SubElement(root, 'USER_PRG', prg=code, testId=xmlid)
        ET.SubElement(root, 'TESTED_PRG', prg=code, testId=xmlid)

        ET.SubElement(marks_element, 'MARK', testId=xmlid, mark="10")
        
        times.append(end_time - start_time)
    
    print(times)

    worktree.write(worksheet_path, encoding='utf-8', xml_declaration=True)
    with open(worksheet_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        print(content)
        file.seek(0)
        content = content.replace('amp;', '')
        file.write(content)
        file.truncate()

    




if __name__ == '__main__':

    # lesson = int(input('Введите номер урока: '))
    # letter = input('Введите букву урока: ').upper()
    
    # print(code_builder(solver(f'./robot/{lesson}/{lesson}-{letter}.fil')))


    worksheet = tk.Tk()
    worksheet.withdraw()

    file_path = filedialog.askopenfilename(
        title='Выберите файл тетради:',
        filetypes=(("Файл тетради .kurs/.work", "*.xml"), ("Все файлы", "*.*"))
    )

    print(file_path)
    tasks_paths, worksheet_path = initializate(file_path)
    print(tasks_paths)
    create_worksheet_solutions(tasks_paths, worksheet_path)



