import csv
from typing import Dict, List, Optional


def read_csv(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def apply_filter(data: List[Dict[str, str]], condition: str) -> List[Dict[str, str]]:
    operators = {'=', '>', '<'}
    for op in operators:
        if op in condition:
            column, value = condition.split(op, 1)
            column = column.strip()
            value = value.strip()
            break
    else:
        raise ValueError("Неверный формат условия фильтрации")
    
    filtered = []
    for row in data:
        if column not in row:
            continue
            
        row_val = row[column]
        try:
            num_val, row_num = float(value), float(row_val)
            if (op == '>' and row_num > num_val) or \
               (op == '<' and row_num < num_val) or \
               (op == '=' and row_num == num_val):
                filtered.append(row)
        except ValueError:
            # сравниваем как строки
            if (op == '=' and row_val.lower() == value.lower()):
                filtered.append(row)
    
    return filtered


def apply_aggregation(data: List[Dict[str, str]], aggregate: str) -> Optional[float]:
    try:
        column, operation = aggregate.split('=', 1)
        column = column.strip()
        operation = operation.strip()
    except ValueError:
        raise ValueError("Неверный формат агрегации")
    
    values = []
    for row in data:
        if column in row:
            try:
                values.append(float(row[column]))
            except ValueError:
                continue
    
    if not values:
        return None
    
    if operation == 'avg':
        return sum(values) / len(values)
    if operation == 'min':
        return min(values)
    if operation == 'max':
        return max(values)
    
    raise ValueError(f"Неизвестная операция: {operation}")


def apply_order(data: List[Dict[str, str]], order: str) -> List[Dict[str, str]]:
    try:
        column, direction = order.split('=', 1)
        column = column.strip()
        direction = direction.strip().lower()
        
        if direction not in ('asc', 'desc'):
            raise ValueError("Направление сортировки должно быть 'asc' или 'desc'")
        
        reverse_sort = (direction == 'desc')
        
        def sort_key(row):
            value = row.get(column, '')
            try:
                return float(value), value
            except ValueError:
                raise ValueError("Только числа")
        
        return sorted(data, key=sort_key, reverse=reverse_sort)
    
    except ValueError:
        raise ValueError("Неверный формат сортировки. Используйте 'column=asc' или 'column=desc'")



def process_csv(file_path: str, where: Optional[str] = None, aggregate: Optional[str] = None, order: Optional[str] = None):
    data = read_csv(file_path)
    
    if where:
        data = apply_filter(data, where)

    if order:
        data = apply_order(data, order)
    
    if aggregate:
        result = apply_aggregation(data, aggregate)
        return {aggregate.split('=')[1].strip(): result} if result is not None else None  
    
    return data