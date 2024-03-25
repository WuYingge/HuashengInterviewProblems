"""
列表的sort和sorted区别主要是在是否修改原始列表
sort会在原地排序，返回None
sorted会返回一个新的排好序的列表，原始列表不动
"""


origin_list = [3, 2, 1]

if __name__ == "__main__":
    copy_list = origin_list.copy()
    none_return = copy_list.sort()
    
    copy2_list = origin_list.copy()
    sorted_list = sorted(copy2_list)
    
    
    # sort后的列表和sorted后的列表排序一致
    assert copy_list == sorted_list
    
    # sorted后的列表是返回了一个新列表
    assert isinstance(sorted_list, list)
    # sort后的返回值是None
    assert isinstance(none_return, type(None))
    
    # sort后的列表被改动了
    assert origin_list != copy_list
    # sorted后列表没有被改动
    assert origin_list == copy2_list
    
    print("all assertion passed")
