# 自定义字典，包含5个条目，格式为key: (value1, value2)  
custom_dict = {  
    'a': (3, 2),  
    'b': (1, 3),  
    'c': (2, 1),  
    'd': (4, 4),  
    'e': (1, 2)  
}  
  
# 按照value1进行正排序  
sorted_by_value1 = sorted(custom_dict.items(), key=lambda item: item[1][0])  
print("按value1排序:", sorted_by_value1)  
  
# 按照value2进行正排序  
sorted_by_value2 = sorted(custom_dict.items(), key=lambda item: item[1][1])  
print("按value2排序:", sorted_by_value2)