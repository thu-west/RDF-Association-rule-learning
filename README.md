# RDF-Association-rule-learning
挖掘给定节点的邻居集合中的关联规则，并返回包含查询节点的关联规则。

## 安装环境

Python 3.6 + rdflib + efficient_apriori + argparse

## 通过给定路径查询
```sh
Python3 patient_and_zhuyuan.py -g graph_file -t path -q path_node+direction -x query_node
Python3 patient_and_zhuyuan.py -g new2_Guxi2_2020-03-19_16-26-01.nq -t path -q Patient,times,住院手术报告,1,-1 -x instance/minzu-汉族,instance/guoji-中国
```
### 路径查询格式说明

-g 给出查询的图文件，-t规定查询类型是路径还是SPARQL，-q给出路径上节点的关键词，后面数字1代表路径上两个节点前面试主语，后面是宾语，-1则相反。-x则给出查询的节点。

## 通过SPARQL查询
```sh
Python3 patient_and_zhuyuan.py -g graph_file -t sparql -q sparql_query -x query_node
Python3 patient_and_zhuyuan.py -g new2_Guxi2_2020-03-19_16-26-01.nq -t sparql -q SELECT_DISTINCT_?patient_?c_WHERE_{_?patient_<http://www.tsinghua-west.com/Guxi/Pt>_?id_._?c_<http://www.tsinghua-west.com/Guxi/PTE#TLINK>_?id_.___} -x instance/minzu-汉族,instance/guoji-中国,times/1409045

```
### SPARQL查询格式说明

基本和路径查询相同，需要注意的是-q后面跟随的是SPARQL查询语句，并且用'\_' 替换掉空格。

## 数据格式说明

输入数据为nq格式。


