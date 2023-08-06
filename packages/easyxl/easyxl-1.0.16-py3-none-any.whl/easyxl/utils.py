import re
import xlwings as xw

keys_to_remove = ['_type', '_has_content']
# empties = [set(), list(), dict(), None, ""]

def remove_keys(udata, keys_to_remove):
    keys = set(udata.__dict__.keys())
    for i in keys_to_remove:
        if i in keys:
            keys.remove(i)
    keys = sorted(list(keys))
    return keys

def udata_to_json(obj, ignore_null=True):
    if type(obj) is uData:
        keys = remove_keys(obj, keys_to_remove)
        # 如果数据类型是list，那么需要对key进行排序，按照数字大小排序输出为list
        if obj._type == 'list':
            sorted_keys = sorted([int(i) for i in keys])
                # print("ignore is False and sorted_keys is {0}".format(sorted_keys))
            l = len(sorted_keys)
            remap_keys = range(l)
            m = {remap_keys[i]:str(sorted_keys[i]) for i in range(l)}
            rlt = [None for i in range(l)]
            for idx, attr in m.items():
                # if type(obj.__dict__[attr]) is UnifiedData:
                rlt[idx] = udata_to_json(obj.__dict__[attr])
                # else:
                #     rlt[idx] = obj[attr]
        # 如果数据类型是dict，那么直接输出为dict
        elif obj._type == 'dict':
            rlt = {}
            for i in keys:
                # if type(obj.__dict__[i]) is UnifiedData:
                rlt[i] = udata_to_json(obj.__dict__[i])
                # else:
                #     rlt[i] = obj[i]
    else:
        if type(obj) is list:
            rlt = []
            for i in obj:
                rlt.append(udata_to_json(i))
        elif type(obj) is dict:
            rlt = {}
            for k, v in obj.items():
                rlt[k] = udata_to_json(v)
        else:
            rlt = obj
        # raise ValueError("obj._type error")
    return rlt

def json_to_udata(jdata):
    if type(jdata) is list:
        rlt = uData('list')
        for idx, i in enumerate(jdata):
            rlt[str(idx)] = json_to_udata(i)
    elif type(jdata) is dict:
        rlt = uData('dict')
        for k, v in jdata.items():
            rlt[k] = json_to_udata(v)
    else: # 基本类型
        rlt = jdata
    return rlt

def tag_udata(obj):
    if type(obj) is uData:
        has_content = []
        keys = remove_keys(obj, keys_to_remove)
        for key in keys:
            has_content.append(tag_udata(obj[key]))
        rlt = 1 if sum(has_content) else 0
        obj._has_content = rlt
        # print("===")
        # print(udata_to_json(obj))
        # print(rlt)
    else:
        if obj or obj == 0:
            rlt = 1
        else:
            rlt = 0
    return rlt


def prune_udata(obj, key, f_obj, rm_empty_dict_item=False, \
    rm_empty_list_item=False):

    if rm_empty_dict_item:
        if type(obj) is uData:
            # print("==")
            # print('i am udata')
            # print(udata_to_json(obj))
            if obj._has_content:
                # print("udata has content")
                ks = remove_keys(obj, keys_to_remove)
                for k in ks:
                    # print(k)
                    prune_udata(obj[k], k, obj, \
                        rm_empty_dict_item, rm_empty_list_item)
            else:
                if f_obj._type =='dict':
                    f_obj.__delattr__(key)
                else:
                    ks = remove_keys(obj, keys_to_remove)
                    for k in ks:
                        prune_udata(obj[k], k, obj, \
                            rm_empty_dict_item, rm_empty_list_item)
        else:
            if obj or obj == 0:
                pass
            else:
                if f_obj._type =='dict':
                    f_obj.__delattr__(key)

    if rm_empty_list_item:
        if type(obj) is uData:
            if obj._has_content:
                ks = remove_keys(obj, keys_to_remove)
                for k in ks:
                    prune_udata(obj[k], k, obj, \
                        rm_empty_dict_item, rm_empty_list_item)
            else:
                if f_obj._type =='list':
                    f_obj.__delattr__(key)
                else:
                    ks = remove_keys(obj, keys_to_remove)
                    for k in ks:
                        prune_udata(obj[k], k, obj, \
                                    rm_empty_dict_item, rm_empty_list_item)
        else:
            if obj or obj == 0:
                pass
            else:
                if f_obj._type =='list':
                    f_obj.__delattr__(key)
                        

class uData:
    # 标记数据类型，把数据注册到这个类里面
    def __init__(self, t):
        if t in ('list', 'dict'):
            self._type = t
        else:
            raise ValueError("type input error {0}".format(t))
    
    def __setitem__(self, index, value):
        self.__dict__[str(index)] = value
    def __getitem__(self, index):
        return self.__dict__[str(index)]
    def __setattr__(self, index, value):
        self.__dict__[str(index)] = value
    def __getattr__(self, index):
        return self.__dict__[str(index)]

def xw_open(wb_path, if_visible=True):
    apps = xw.apps
    if apps:
        for ap in apps:
            if wb_path in [b.fullname for b in ap.books]:
                app = ap
            else:
                ap.kill()
    if not apps:
        app = xw.apps.add(visible=if_visible)
    books = app.books
    book_names = [b.fullname for b in books]
    if books and wb_path in book_names:
        book_idx = book_names.index(wb_path)
        wb = books[book_idx]
    else:
        wb = app.books.open(wb_path)
    return app, wb
        

# if try decorator
def deco_try(if_try=True):
    def deco(func):
        def wrapper(*args, **kwargs):
            if if_try:
                try:
                    rlt = func(*args, **kwargs)
                except Exception as e:
                    print(e)
            else:
                rlt = func(*args, **kwargs)
            return rlt
        return wrapper
    return deco

def convert_xlsx_addr(addr):
    def col_to_num(col_str):
        """ Convert base26 column string to number. """
        expn = 0
        col_num = 0
        for char in reversed(col_str):
            col_num += (ord(char) - ord('A') + 1) * (26 ** expn)
            expn += 1
        return col_num
    reg = re.compile(r"([a-zA-Z]+|[0-9]+)")
    strs = reg.findall(addr)
    rlts = []
    for s in strs:
        if s.isdigit():
            rlts.append(int(s))
        else:
            rlts.append(col_to_num(s.upper()))
    if len(rlts) == 1:
        result = rlts[0]
    elif len(rlts) == 2:
        result = tuple([(rlts[1], rlts[0])])
    elif len(rlts) == 4:
        result = ((rlts[1], rlts[0]), (rlts[3], rlts[2]))
    else:
        raise ValueError("address format error")

    return result


if __name__ == "__main__":
    my_dict = [{'LB': [0, {}]}, {}]
    obj = json_to_udata(my_dict)
    tag_udata(obj)
    keys = remove_keys(obj, keys_to_remove)
    print(keys)
    for key in keys:
        prune_udata(obj[key], key, obj, rm_empty_dict_item=True, rm_empty_list_item=True)
    data = udata_to_json(obj)

    print(data)


    pass