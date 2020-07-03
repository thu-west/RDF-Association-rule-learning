# *_*coding:utf-8 *_*

from itertools import permutations
from apriori import apriori
import rdflib
import os, re, time, sys
import argparse


def get_index(g):
    index = 1
    dict_forward = {}
    dict_reverse = {}
    for subject, predicate, obj in g:
        if not (subject, predicate, obj) in g:
            raise Exception("Iterator / Container Protocols are Broken!!")
        if dict_forward.get(str(subject), -1) == -1:
            dict_forward[str(subject)] = index
            dict_reverse[index] = str(subject)
            index = index + 1
        if dict_forward.get(str(predicate), -1) == -1:
            dict_forward[str(predicate)] = index
            dict_reverse[index] = str(predicate)
            index = index + 1
        if dict_forward.get(str(obj), -1) == -1:
            dict_forward[str(obj)] = index
            dict_reverse[index] = str(obj)
            index = index + 1
    return dict_forward,dict_reverse

def match_path(g,path,path1,dict_forward):
    match_result = {}
    if len(path) == 1:
        for sub in g.subjects():
            if re.search(path[0], sub) is None:
                continue
            if match_result.get(sub, -1) == -1:
                match_result[sub] = {sub}
            else:
                match_result[sub].add(sub)
    else:
        if int(path1[0]) == 1:
            for sub in g.subjects():
                if re.search(path[0], sub) is None:
                    continue
                for pre, obj in g.predicate_objects(sub):
                    if re.search(path[1], obj) is None:
                        continue
                    if match_result.get(sub, -1) == -1:
                        match_result[sub] = {obj}
                    else:
                        match_result[sub].add(obj)
        else:
            for obj in g.objects():
                if re.search(path[0], obj) is None:
                    continue
                for sub, pre in g.subject_predicates(obj):
                    if re.search(path[1], sub) is None:
                        continue
                    if match_result.get(obj, -1) == -1:
                        match_result[obj] = {sub}
                    else:
                        match_result[obj].add(sub)
        for idx, val in enumerate(path1[1:], 1):
            if int(val) == 1:
                for key, values in match_result.items():
                    set_tmp = set()
                    for value in values:
                        for pre, obj in g.predicate_objects(value):
                            if re.search(path[idx + 1], obj) is None:
                                continue
                            set_tmp.add(obj)
                    match_result[key] = set_tmp
            else:
                for key, values in match_result.items():
                    set_tmp = set()
                    for value in values:
                        for sub, pre in g.subject_predicates(value):
                            if re.search(path[idx + 1], sub) is None:
                                continue
                            set_tmp.add(sub)
                    match_result[key] = set_tmp
    record = []
    for key, values in match_result.items():
        for value in values:
            list_tmp = []
            for pre, obj in g.predicate_objects(key):
                list_tmp.append(dict_forward[str(obj)])
            for sub, pre in g.subject_predicates(key):
                list_tmp.append(dict_forward[str(sub)])
            if key == value:
                continue
            for pre, obj in g.predicate_objects(value):
                list_tmp.append(dict_forward[str(obj)])
            for sub, pre in g.subject_predicates(value):
                list_tmp.append(dict_forward[str(sub)])
            list_tmp = list(set(list_tmp))
            record.append(list_tmp)
    return record
def match_path2(g,path,path1,dict_forward):
    match_result = {}
    if len(path) == 1:
        for sub in g.subjects():
            if sub.find(path[0]) < 0:
                continue
            if match_result.get(sub, -1) == -1:
                match_result[sub] = {sub}
            else:
                match_result[sub].add(sub)
    else:
        if int(path1[0]) == 1:
            for sub in g.subjects():
                if sub.find(path[0]) < 0:
                    continue
                for pre, obj in g.predicate_objects(sub):
                    if obj.find(path[1]) < 0:
                        continue
                    if match_result.get(sub, -1) == -1:
                        match_result[sub] = {obj}
                    else:
                        match_result[sub].add(obj)
        else:
            for obj in g.objects():
                if obj.find(path[0]) < 0:
                    continue
                for sub, pre in g.subject_predicates(obj):
                    if sub.find(path[1]) < 0:
                        continue
                    if match_result.get(obj, -1) == -1:
                        match_result[obj] = {sub}
                    else:
                        match_result[obj].add(sub)
        for idx, val in enumerate(path1[1:], 1):
            if int(val) == 1:
                for key, values in match_result.items():
                    set_tmp = set()
                    for value in values:
                        for pre, obj in g.predicate_objects(value):
                            if obj.find(path[idx + 1]) < 0:
                                continue
                            set_tmp.add(obj)
                    match_result[key] = set_tmp
            else:
                for key, values in match_result.items():
                    set_tmp = set()
                    for value in values:
                        for sub, pre in g.subject_predicates(value):
                            if sub.find(path[idx + 1]) < 0:
                                continue
                            set_tmp.add(sub)
                    match_result[key] = set_tmp
    record = []
    for key, values in match_result.items():
        for value in values:
            list_tmp = []
            for pre, obj in g.predicate_objects(key):
                list_tmp.append(dict_forward[str(obj)])
            for sub, pre in g.subject_predicates(key):
                list_tmp.append(dict_forward[str(sub)])
            if key == value:
                continue
            for pre, obj in g.predicate_objects(value):
                list_tmp.append(dict_forward[str(obj)])
            for sub, pre in g.subject_predicates(value):
                list_tmp.append(dict_forward[str(sub)])
            list_tmp = list(set(list_tmp))
            record.append(list_tmp)
    return record

def match_sparql(g,sparql_query,dict_forward):
    qres = g.query(sparql_query)
    record = []
    for row in qres:
        list_tmp = []
        for item in row:
            for pre, obj in g.predicate_objects(item):
                list_tmp.append(dict_forward[str(obj)])
            for sub, pre in g.subject_predicates(item):
                list_tmp.append(dict_forward[str(sub)])
        list_tmp = list(set(list_tmp))
        record.append(list_tmp)
    return record


def write_file(graphfile, record,query_node,dict_reverse):
    itemfile = "path_itemsets.txt"
    rulesfile = "path_rules.txt"
    rulesdict_file= "path_rule_dict.text"
    if os.path.exists(itemfile):
        os.remove(itemfile)
    if os.path.exists(rulesfile):
        os.remove(rulesfile)
    if os.path.exists(rulesdict_file):
        os.remove(rulesdict_file)
    itemfile_write = open(itemfile, 'a', encoding='utf-8')
    rulesfile_write = open(rulesfile, 'a', encoding='utf-8')

    #print(len(record))
    itemsets, rules = apriori(record,query_node=query_node, min_support=0.5, min_confidence=0.9)
    for (key, value) in itemsets.items():
        itemset = []
        for item_tuple in value.keys():
            for item in item_tuple:
                itemset.append(dict_reverse[item])
        #print(itemset)
        itemfile_write.write(str(itemset))
        itemfile_write.write("\n")
    rule_dict = {}
    for rule in rules:
        lhs_itemset = []
        rhs_itemset = []
        for item in rule.lhs:
            lhs_itemset.append(dict_reverse[item])
        for item in rule.rhs:
            rhs_itemset.append(dict_reverse[item])
        for item in rule.lhs+rule.rhs:
            if rule_dict.get(dict_reverse[item], -1) == -1:
                rule_dict[dict_reverse[item]] = [str(lhs_itemset) + "->" + str(rhs_itemset)+"\tsupport="+str(rule.support)+"\tconfidence="+str(rule.confidence)+'\tlift='+str(rule.lift)]
            else:
                rule_dict[dict_reverse[item]].append(str(lhs_itemset) + "->" + str(rhs_itemset)+"\tsupport="+str(rule.support)+"\tconfidence="+str(rule.confidence)+'\tlift='+str(rule.lift))

        rulesfile_write.write(str(lhs_itemset))
        rulesfile_write.write("->")
        rulesfile_write.write(str(rhs_itemset))
        rulesfile_write.write("\n")
    with open(rulesdict_file, 'w', encoding='utf8') as outfile:
        for key, values in rule_dict.items():
            outfile.write(key + ":[")
            for value in values:
                lhs_itemset = []
                rhs_itemset = []
                for item in rule.lhs:
                    lhs_itemset.append(dict_reverse[item])
                for item in rule.rhs:
                    rhs_itemset.append(dict_reverse[item])
                outfile.write(str(lhs_itemset))
                outfile.write("->")
                outfile.write(str(rhs_itemset))
                outfile.write(", ")
            outfile.write("]\n")
    return rule_dict
def get_query_node_result(query_node,rule_dict,dict_reverse):
    rule_set=set(rule_dict[dict_reverse[query_node[0]]])
    for node in query_node[1:]:
        node=dict_reverse[node]
        rule_set=rule_set.intersection(rule_dict[node])
    with open("query_result.txt",'w',encoding='utf8') as outfile:
        for rule in rule_set:
            outfile.write(rule+'\n')
    for i in range(len(query_node)):
        query_node[i]=dict_reverse[query_node[i]]

    for p in permutations(query_node):
        for i in range(1,len(query_node)):
            rule_str='[\''
            for j in range(i):
                rule_str+=p[j]+'\', \''
            rule_str=rule_str[:-3]+']->[\''
            for j in range(i,len(p)):
                rule_str+=p[j]+'\', \''
            rule_str=rule_str[:-3]+']'
            result_dict={"rule":rule_str}
            for rule in rule_set:
                if rule.find(rule_str)>=0:
                    re_group=re.search('support=(.*?)confidence=(.*?)lift=(.*)', rule)
                    result_dict["support"]=re_group[1]
                    result_dict["confidence"]=re_group[2]
                    result_dict["lift"]=re_group[3]
                    print(result_dict)




def main_algorithm(args):
    graphfile = args.graph_file
    g = rdflib.Graph()
    result = g.parse(graphfile, format="nt")
    dict_forward,dict_reverse=get_index(g)
    query_node=args.query_node.strip('\n').split(',')
    for i in range(len(query_node)):
        query_node[i]='http://www.tsinghua-west.com/Guxi/'+query_node[i]

    if args.query_type == 'path':
        path_node_list=args.query_file.strip('\n').split(',')
        path=path_node_list[:int((len(path_node_list)+1)/2)]
        path1=path_node_list[int((len(path_node_list)+1)/2):]
        #print(path,path1)
        match_result = match_path2(g, path, path1, dict_forward)
        for i in range(len(query_node)):
            query_node[i]=dict_forward[query_node[i]]

        rule_dict=write_file(g,match_result,query_node,dict_reverse)
        get_query_node_result(query_node,rule_dict,dict_reverse)
    else:
        sparql_query=args.query_file
        sparql_query=sparql_query.replace('_',' ')
        match_result = match_sparql(g, sparql_query, dict_forward)
        for i in range(len(query_node)):
            query_node[i]=dict_forward[query_node[i]]
        rule_dict = write_file(g, match_result, query_node, dict_reverse)
        get_query_node_result(query_node, rule_dict, dict_reverse)

if __name__ == '__main__':
    start_time=time.time()
    parser = argparse.ArgumentParser()
    basic = parser.add_argument('-g', '--graph_file',dest='graph_file', type=str, required=True, help='input graph file')
    basic = parser.add_argument('-t', '--query_type',dest='query_type', type=str, required=True, help='query type')
    basic = parser.add_argument('-q', '--query_file', dest='query_file', type=str, required=True, help='query file')
    basic = parser.add_argument('-x', '--query_node', dest='query_node', type=str, required=True, help='query node')
    if len(sys.argv[1:])!=8:
        parser.print_help()        #print usage
        parser.exit()
    args = parser.parse_args()

    main_algorithm(args)
