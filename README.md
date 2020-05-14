# RDF-Association-rule-learning
挖掘给定节点的邻居集合中的关联规则，并返回包含查询节点的关联规则。

## 安装环境

Python 3.6 + rdflib + efficient_apriori + argparse

## 通过给定路径查询
```sh
Python3 patient_and_zhuyuan.py -g graph_file -t path -q query.txt
```
### 路径查询文件说明

第一行给出要查询的实体，输出文件query_result.txt会给出包含查询实体的所有关联规则。第二行给出路径上所有的主语和宾语。第三行中1代表前面试主语，后面是宾语，-1则相反。

## 通过SPARQL查询
```sh
Python3 patient_and_zhuyuan.py -g graph_file -t sparql -q sparql_query.txt
```
### SPARQL查询文件说明

第一行给出要查询的实体，输出文件query_result.txt会给出包含查询实体的所有关联规则。后面则是SPARQL查询语句。

## 数据格式说明

输入数据为nq格式。


