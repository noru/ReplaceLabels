__author__ = 'xiua'

from xml.etree.ElementTree import ElementTree, Element

def read_xml(in_path):
    '''''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree

def write_xml(tree, out_path):
    '''''将xml文件写出
       tree: xml树
       out_path: 写出路径'''
    tree.write(out_path, encoding="utf-8",xml_declaration=True)

def if_match(node, kv_map):
    '''''判断某个节点是否包含所有传入参数属性
       node: 节点
       kv_map: 属性及属性值组成的map'''
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True

#---------------search -----

def find_nodes(tree, path):
    '''''查找某个路径匹配的所有节点
       tree: xml树
       path: 节点路径'''
    return tree.findall(path)


def get_node_by_keyvalue(nodelist, kv_map):
    '''''根据属性及属性值定位符合的节点，返回节点
       nodelist: 节点列表
       kv_map: 匹配属性及属性值map'''
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes

#---------------change -----

def change_node_properties(nodelist, kv_map, is_delete=False):
    '''''修改/增加 /删除 节点的属性及属性值
       nodelist: 节点列表
       kv_map:属性及属性值map'''
    for node in nodelist:
        for key in kv_map:
            if is_delete:
                if key in node.attrib:
                    del node.attrib[key]
            else:
                node.set(key, kv_map.get(key))

def change_node_text(nodelist, text, is_add=False, is_delete=False):
    '''''改变/增加/删除一个节点的文本
       nodelist:节点列表
       text : 更新后的文本'''
    for node in nodelist:
        if is_add:
            node.text += text
        elif is_delete:
            node.text = ""
        else:
            node.text = text

def create_node(tag, property_map, content):
    '''''新造一个节点
       tag:节点标签
       property_map:属性及属性值map
       content: 节点闭合标签里的文本内容
       return 新节点'''
    element = Element(tag, property_map)
    element.text = content
    return element

def add_child_node(nodelist, element):
    '''''给一个节点添加子节点
       nodelist: 节点列表
       element: 子节点'''
    for node in nodelist:
        node.append(element)

def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
    '''''同过属性及属性值定位一个节点，并删除之
       nodelist: 父节点列表
       tag:子节点标签
       kv_map: 属性及属性值列表'''
    for parent_node in nodelist:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag and if_match(child, kv_map):
                parent_node.remove(child)

def GetFileList(FindPath,FlagStr=['Labels.', '.resx']):
    def IsSubString(SubStrList,Str):
        '''''
        #判断字符串Str是否包含序列SubStrList中的每一个子字符串
        #>>>SubStrList=['F','EMS','txt']
        #>>>Str='F06925EMS91.txt'
        #>>>IsSubString(SubStrList,Str)#return True (or False)
        '''
        flag=True
        for substr in SubStrList:
            if not(substr in Str):
                flag=False

        return flag
    '''''
    #获取目录中指定的文件名
    #>>>FlagStr=['F','EMS','txt'] #要求文件名称中包含这些字符
    #>>>FileList=GetFileList(FindPath,FlagStr) #
    '''
    import os
    FileList=[]
    FileNames=os.listdir(FindPath)
    if (len(FileNames)>0):
       for fn in FileNames:
           if (len(FlagStr)>0):
               #返回指定类型的文件名
               if (IsSubString(FlagStr,fn)):
                   fullfilename=os.path.join(FindPath,fn)
                   FileList.append(fullfilename)
           else:
               #默认直接返回所有文件名
               fullfilename=os.path.join(FindPath,fn)
               FileList.append(fullfilename)

    #对文件名排序
    if (len(FileList)>0):
        FileList.sort()

    return FileList

if __name__ == "__main__":

    path = 'D:/workspace/'
    list = "ZeroAppText,ServerErrorOccur,SubscriptionCancellationBodyToPublisher,SubscriptionCancellationBodyToSubscriber,WebServicesEmailSentDesc,WebServicesLoginADSKDesc,NewAppSubmittedEmailSignature".split(',')
    old1 = "@autodesk.com"
    old2 = "@autodesk.com"
    new1 = "@autodesk.com"
    new2 = "@autodesk.com"

    l=GetFileList(path)

    for fp in l:
        root = read_xml(fp)
        for name in list:
            old = old1
            new = new1
            if name == 'ZeroAppText':
                old = old2
            if name == 'NewAppSubmittedEmailSignature':
                new = new2
            target = get_node_by_keyvalue(find_nodes(root,"data"), {"name": name})
            change_node_text(target[0],find_nodes(target[0], "value")[0].text.replace(old, new))
        write_xml(root, fp)

    # #1. 读取xml文件
    # tree = read_xml(path)
    # write_xml(tree, "C:/1.xml")
    #
    # #2. 属性修改
    #   #A. 找到父节点
    # nodes = find_nodes(tree, "data")
    #   #B. 通过属性准确定位子节点
    # target = get_node_by_keyvalue(nodes, {"name":"ZeroAppText"})
    #
    # # node = find_nodes(target[0], "value")
    # # print(node[0].text)
    # change_node_text(target[0], "hehe")
    # # print(node[0].text)
    # write_xml(tree, "C:/2.xml")


























    #   #C. 修改节点属性
    # change_node_properties(result_nodes, {"age": "1"})
    #   #D. 删除节点属性
    # change_node_properties(result_nodes, {"value":""}, True)

    # #3. 节点修改
    #   #A.新建节点
    # a = create_node("person", {"age":"15","money":"200000"}, "this is the firest content")
    #   #B.插入到父节点之下
    # add_child_node(result_nodes, a)
    #
    # #4. 删除节点
    #    #定位父节点
    # del_parent_nodes = find_nodes(tree, "processers/services/service")
    #    #准确定位子节点并删除之
    # target_del_node = del_node_by_tagkeyvalue(del_parent_nodes, "chain", {"sequency" : "chain1"})
    #
    # #5. 修改节点文本
    #    #定位节点
    # text_nodes = get_node_by_keyvalue(find_nodes(tree, "processers/services/service/chain"), {"sequency":"chain3"})
    # change_node_text(text_nodes, "new text")

    #6. 输出到结果文件
    # write_xml(tree, path)