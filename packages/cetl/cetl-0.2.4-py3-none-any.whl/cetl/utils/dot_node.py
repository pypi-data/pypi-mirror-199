import re
import inspect
import graphviz

display_parallel = False
display_sub_pipeline = True

def init_digraph():
    return graphviz.Digraph("pipeline graph", format='png')

def update_node(current_node=None, new_node=None):
    return current_node, new_node

def recursive_build_digraph(_predot, _dot, node_pairs, parallel_index, pipeline_index):
    """
    shape reference: https://graphviz.org/doc/info/shapes.html

    format for node_pairs:
    with display_parallel=True
    --------------------
    [   ('', '1.addRowNumber'), 
        ('1.addRowNumber', 'parallel #1', 'parallelTransformer'), 
        {   'process #0': ('parallel #1', '2.format2String'), 
            'process #1': [ ('parallel #1', '3.filterBy'), 
                            ('3.filterBy', 'parallel #2', 'parallelTransformer'), 
                            {   'process #0': ('parallel #2', '4.addRowNumber'), 
                                'process #1': ('parallel #2', '5.passDataFrame')}, 
                            ('4.addRowNumber', '6.toCSV'), 
                            ('5.passDataFrame', '6.toCSV')], 
            'process #2': [('parallel #1', '7.paddingZero')], 
            'process #3': ('parallel #1', '8.dropColumns')}, 
                            ('2.format2String', '9.passDataFrame'), 
                            ('6.toCSV', '9.passDataFrame'), 
                            ('7.paddingZero', '9.passDataFrame'), 
                            ('8.dropColumns', '9.passDataFrame'), 
                            [('9.passDataFrame', '10.passDataFrame'), ('10.passDataFrame', '11.toCSV')]]
    
    with display_parallel=False
    --------------------
    [('', '1.addRowNumber'), 
        {   'process #0': ('1.addRowNumber', '2.format2String'), 
            'process #1': [('1.addRowNumber', '3.filterBy'), {'process #0': ('3.filterBy', '4.addRowNumber'), 
                                                            'process #1': ('3.filterBy', '5.passDataFrame')}, 
                                                            ('4.addRowNumber', '6.toCSV'), ('5.passDataFrame', '6.toCSV')], 
            'process #2': [('1.addRowNumber', '7.paddingZero')], 
            'process #3': ('1.addRowNumber', '8.dropColumns')}, 
        ('2.format2String', '9.passDataFrame'), 
        ('6.toCSV', '9.passDataFrame'), 
        ('7.paddingZero', '9.passDataFrame'), 
        ('8.dropColumns', '9.passDataFrame'), 
        [('9.passDataFrame', '10.passDataFrame'), ('10.passDataFrame', '11.toCSV')]]

    """
    
    for i, sub_node_pairs in enumerate(node_pairs):
        if isinstance(sub_node_pairs, dict):
            num_parallel_pairs = len(sub_node_pairs)
            # make parallelTransformer cluster
            # if display_parallel:
            #     parallel_index = parallel_index + 1 if num_parallel_pairs>1 else parallel_index
            #     _sub_dot = _dot.subgraph(name=f"cluster_{str(parallel_index)}")
            #     _sub_dot.attr(label=f"parallel cluster #{str(parallel_index)}", color="blue")
            # else:
            _sub_dot = _dot
            
            for j, sub_node_pair in enumerate(sub_node_pairs.values()):
                
                if isinstance(sub_node_pair, tuple):
                    
                    _usage_dot_ = _sub_dot  if j!=0 else _dot
                    if sub_node_pair[0]!="":
                        _usage_dot_.edge(sub_node_pair[0], sub_node_pair[1], label="")

                elif isinstance(sub_node_pair, list):
                    
                    # if display_sub_pipeline:
                    #     num_sub_pipeline_pairs = len(sub_node_pair)
                    #     pipeline_index = pipeline_index + 1 if num_sub_pipeline_pairs>1 else pipeline_index
                    #     with _sub_dot.subgraph(name=f"cluster_{str(pipeline_index)}") as _sub_pipeline_dot:
                    #         _sub_pipeline_dot.attr(label=f"pipeline cluster #{str(pipeline_index)}", color="blue")
                    #         _, _, parallel_index, pipeline_index = recursive_build_digraph(_sub_dot, _sub_pipeline_dot, sub_node_pair, parallel_index, pipeline_index)
                    # else:
                    _sub_pipeline_dot = _sub_dot
                    _, _, parallel_index, pipeline_index = recursive_build_digraph(_sub_dot, _sub_pipeline_dot, sub_node_pair, parallel_index, pipeline_index)

        elif isinstance(sub_node_pairs, list):
            num_pipeline_pairs = len(sub_node_pairs)
            # make pipeline cluster
            # if display_sub_pipeline:
            #     pipeline_index = pipeline_index + 1 if num_pipeline_pairs> 1 else pipeline_index
            #     with _dot.subgraph(name=f"cluster_{str(pipeline_index)}") as c:
            #         c.attr(label=f"pipeline cluster #{str(pipeline_index)}", color="blue")
            #         _, _, parallel_index, pipeline_index = recursive_build_digraph(_dot, c, sub_node_pairs, parallel_index, pipeline_index)
            # else:
            # if display_pipeline is False, do not use subgraph
            _, _, parallel_index, pipeline_index = recursive_build_digraph(_dot, _dot, sub_node_pairs, parallel_index, pipeline_index)

        elif isinstance(sub_node_pairs, tuple):
            _usage_dot_ = _dot if i!=0 else _predot
            # make transformer edge
            node_pair = sub_node_pairs
            if node_pair[0]!="":
                _usage_dot_.edge(node_pair[0], node_pair[1], label="") 
                if len(node_pair)>2:
                    if node_pair[2]=="parallelTransformer":
                        _usage_dot_.node(node_pair[1], shape='Msquare')
                else:
                    pass
                    # _dot.node(node_pair[0], shape='rect')
                    # _dot.node(node_pair[1], shape='rect')

    return _predot, _dot, parallel_index, pipeline_index



def get_node_text(nodes_text, node_name):
    return nodes_text[node_name]

def append_node_text(nodes_text, node_name, append_text, limit, apply_limit=False):

    if apply_limit:
        if len(append_text)>limit:
            append_text = append_text[:limit]+"..."
    
    nodes_text[node_name] = nodes_text[node_name]+f"{append_text}\l"

def append_description_node_text(nodes_text, node_name, description, limit):
    """
    \l means new line
    """

    if len(description)>limit:
        description = description[:limit]+"..."
    if description:
        description = f"{description}"

    description = description if description else "no description"
    sep_line = "".join(["-" for i in range(int(len(description)*3/2))])
    # print("##########33", sep_line)

    description_text = f"{description}\l{sep_line}"
    append_node_text(nodes_text, node_name, description_text, limit)



def append_input_node_text(nodes_text, node_name, inputs, limit):
    input_text=""
    for input in inputs:
        # print(input, len(input))
        if len(input)>limit:
            input_text += "        " + input[:limit]+"...\l"
        else:
            input_text += "        " + input+"\l"
    #https://www.digitalocean.com/community/tutorials/python-trim-string-rstrip-lstrip-strip
    input_text = input_text.lstrip()[:-2] if input_text else input_text
    append_node_text(nodes_text, node_name, f"Input: {input_text}", limit)


def append_output_node_text(nodes_text, node_name, output, limit):

    if len(output)>limit:
        output = output[:limit]+"..."
    append_node_text(nodes_text, node_name, f"Output: {output}", limit)


def add_dot_node(DataPipeline, _nodename2transformer, transformers_set):
    self=DataPipeline

    nodes_text={}
    for key in _nodename2transformer.keys():
        nodes_text[key]=""
    
    for nodename in transformers_set:
        if "parallelTransformer" in nodename:
            pass
        elif "parallel" in nodename:
                self._dot.node(nodename)
        else:
            transformer = _nodename2transformer[nodename]
            # get transformer description
            description = transformer.description
            #get the arguments of transformer.transform() as input
            # inputs = [nodename for nodename in inspect.getfullargspec(transformer.transform).args if nodename not in ["self"]]
            # get the return value type
            # https://stackoverflow.com/questions/49560974/inspect-params-and-return-types
            # output = str(inspect.signature(transformer.transform).return_annotation)
            # # "<class 'int'>" extract the 'int'
            # output = re.findall("\<class '+(.*?)\'>",output)
            # output = output[0].split(".")[-1] if output else ""

            ############### description text
            append_description_node_text(nodes_text, nodename, description, self.limit)
            ############### nodename text
            append_node_text(nodes_text, nodename, f"Task ID: {nodename}", self.limit, apply_limit=True)
            ############### Input text
            input = transformer.total_input
            input_textline = f"Input: {input:.0f} records"
            append_node_text(nodes_text, nodename, input_textline, self.limit, apply_limit=True)
            ############### Output text
            output = transformer.total_output
            output_textline = f"Output: {output:.0f} records"
            append_node_text(nodes_text, nodename, output_textline, self.limit, apply_limit=True)
            # get the time of execution
            total_time = transformer.total_time
            total_time_textline = f"Take time: {total_time:.4f} seconds"
            append_node_text(nodes_text, nodename, total_time_textline, self.limit, apply_limit=True)

            # get the start time of execution
            start_datetime = transformer.start_datetime
            start_datetime_textline = f"Start at: {start_datetime}"
            append_node_text(nodes_text, nodename, start_datetime_textline, self.limit, apply_limit=True)

            # get the end time of execution
            end_datetime = transformer.end_datetime
            end_datetime_textline = f"End at: {end_datetime}"
            append_node_text(nodes_text, nodename, end_datetime_textline, self.limit, apply_limit=True)

            self._dot.node(nodename, nodes_text[nodename])


# def create_simple_dot_graph(self):
#     """
#     Tutorial: https://graphviz.readthedocs.io/en/stable/examples.html

#     Variables:
#         - _simple_node_pairs = [("1", "2"), ("2", "3), ("3", )]
#             "1" > "2" > "3"
#         - transformers_set = ["1", "2", "3"]
#     """
#     self._dot = graphviz.Graph("pipeline graph", format='png')
#     # general styel
#     self._dot.attr('node', 
#                     shape="rect", 
#                     style="filled", 
#                     fillcolor="skyblue4", 
#                     color="white", 
#                     fontcolor="white")
#     self._dot.attr('edge',
#                     arrowhead="normal",
#                     arrowsize='1.0')
#     # self._dot.graph_attr.update(directed="true")
#     # self._dot.edge_attr(("directed","true"))
    

#     # add node
#     transformers_list=[]
#     for item in self._simple_node_pairs:
#         transformers_list = transformers_list + list(item)
#     transformers_set = sorted(set(transformers_list))
#     for item in transformers_set:
#         # add node
#         self._dot.node(item, item+"\n")

#     # # add edges
#     for item in self._simple_node_pairs:
#         # add edge
#         self._dot.edge(item[0], item[1], 
#                         label="")
#     return self._dot


