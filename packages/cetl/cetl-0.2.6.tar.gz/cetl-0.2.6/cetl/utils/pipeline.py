from sklearn.pipeline import Pipeline as sklearn_pipeline
from collections import defaultdict
import copy
from flask import send_file
import tempfile
import os
import re
from cetl.functional_modules.parallel_transformer import parallelTransformer
from cetl.utils.builder import (build_transformer_from_cfg, get_register, FUNCTIONAL_TRANSFORMERS)
from .dot_node import update_node, recursive_build_digraph, add_dot_node, init_digraph, append_node_text
from .file_mgt import get_datetime_str


def _name_estimators(estimators):
    """Generate names for estimators."""

    names = [
        estimator if isinstance(estimator, str) else type(estimator).__name__.lower()
        for estimator in estimators
    ]
    namecount = defaultdict(int)
    for est, name in zip(estimators, names):
        namecount[name] += 1

    for k, v in list(namecount.items()):
        if v == 1:
            del namecount[k]

    for i in reversed(range(len(estimators))):
        name = names[i]
        if name in namecount:
            names[i] += "-%d" % namecount[name]
            namecount[name] -= 1

    return list(zip(names, estimators))
        
def make_pipeline(*steps, memory=None, verbose=False):
    """
    Examples
    -----------
    >>> from core.utils.pipeline import build_pipeline
    >>> build_pipeline(addNewColumn(), drop_columns())
    Pipeline(transformers=[ 'addNewColumn', addNewColumn(),
                            'drop_columns', drop_columns()])
    """
    # print(steps)
    return Pipeline(_name_estimators(steps), memory=memory, verbose=verbose)



def recursive_build_pipeline_from_cfg(  cfg, 
                                        node_name_set,
                                        node_pairs, 
                                        node_name,
                                        latest_node, 
                                        index, 
                                        parallel_index, 
                                        nodename2transformer, 
                                        pipeline_settings,
                                        kafka_media):
    """
    Examples
    -----------
    global_index = 0
    latest_node = ""
    node_pairs = []

    pipeline, node_pairs, latest_node, index = recursive_build_pipeline_from_cfg(cfg, node_pairs, latest_node, global_index)
    """

    assert "pipeline" in cfg
    
    steps = []


    for trans_cfg in cfg["pipeline"]:
        trans_name = trans_cfg.get("type")  if "type" in trans_cfg else ""
        trans_name = "pipeline" if "pipeline" in trans_cfg else trans_name
        breakpoint = trans_cfg.pop("breakpoint") if "breakpoint" in trans_cfg else 0

        
        if trans_name == "parallelTransformer":         
            
            ########################## adding intermediate node for parallelTransformer
            parallel_name = "parallel"
            parallel_index +=1
            default_parallel_label = "parallelTransformer"
            parallel_node_name = f"{parallel_name}_no.{parallel_index}"
            

            transformers_list = []
            parallel_latest_node = []
            parallel_node_pairs = {}
            latest_nodes = None
            if isinstance(latest_node,str):
                #convert the _previous_node to a list
                latest_nodes= [latest_node for i in range(len(trans_cfg["transformers"]))]
                pre_node_names = [node_name for i in range(len(trans_cfg["transformers"]))]
            elif isinstance(latest_node, list):
                latest_nodes = latest_node
                pre_node_names = node_name
            else:
                assert False, "latest_node is not str or list"

            parallel_dict_index = [i for i in range(len(latest_nodes))]
            # print(parallel_dict_index, latest_nodes, trans_cfg)
            for i, node_name, latest_node, sub_trans_cfg in zip(parallel_dict_index, 
                                                                pre_node_names, 
                                                                latest_nodes, 
                                                                trans_cfg["transformers"]):
 
                if "type" in sub_trans_cfg:
                    sub_trans_name = sub_trans_cfg.get("type") #get the transformer type
                    ############################### dealling with previous transformer is also parallelTransformer
                    assert sub_trans_name!="parallelTransformer", "parallel is not acceptable in parallelTransfomer"
                    ######################### END

                    #add note pair
                    index = index + 1
                    sub_breakpoint = sub_trans_cfg.pop("breakpoint") if "breakpoint" in sub_trans_cfg else 0
                    description = sub_trans_cfg.pop("description") if "description" in sub_trans_cfg else ""
                    module_type = sub_trans_cfg.pop("module_type") if "module_type" in sub_trans_cfg else ""
                    TRANSFORMERS = get_register(module_type, pipeline_settings.default_type)
                    # print(TRANSFORMERS)
                    transformer = build_transformer_from_cfg(sub_trans_cfg, TRANSFORMERS)
                    transformer.pre_node_name = node_name
                    transformer.index = index
                    transformer.node_name = f"{str(index)}.{sub_trans_name}"
                    # transformer.__name__
                    transformer.description = description
                    transformer.breakpoint = sub_breakpoint
                    transformer.print_task_result = pipeline_settings.print_task_result
                    transformer.exchange_media = pipeline_settings.exchange_media
                    transformer.kafka_media = kafka_media
                    transformers_list.append(transformer)
                    # update nodename2transformer
                    nodename2transformer[transformer.node_name] = transformer
                    # update steps list
                    previous_node, _latest_node = update_node(latest_node, transformer.node_name)
                    parallel_node_pairs[f"process_no.{str(i)}"]=(previous_node, _latest_node)
                    node_name_set.add(_latest_node)
                    parallel_latest_node.append(_latest_node)


                elif "pipeline" in sub_trans_cfg:
                    transformer, \
                    node_name_set, \
                    _node_pairs, \
                    node_name, \
                    _latest_node, \
                    index, \
                    parallel_index, \
                    nodename2transformer = recursive_build_pipeline_from_cfg(   sub_trans_cfg, 
                                                                                node_name_set, 
                                                                                [], 
                                                                                node_name,
                                                                                latest_node, 
                                                                                index, 
                                                                                parallel_index, 
                                                                                nodename2transformer,
                                                                                pipeline_settings,
                                                                                kafka_media)
                    transformers_list.append(transformer)
                    parallel_node_pairs[f"process_no.{str(i)}"]=_node_pairs
                    parallel_latest_node.append(_latest_node)


            # updaet latest_node                                                
            previous_node, latest_node = update_node(latest_nodes, parallel_latest_node)
            # update node_pairs
            node_pairs.append(parallel_node_pairs)
            # add steps
            # module_type = trans_cfg.pop("module_type") if "module_type" in trans_cfg else ""
            # TRANSFORMERS = get_register(module_type)
            # print(transformers_list)
            parallel_transformer = build_transformer_from_cfg(trans_cfg, 
                                                              FUNCTIONAL_TRANSFORMERS, 
                                                              transformers_list)
            parallel_transformer.breakpoint = breakpoint
            parallel_transformer.print_task_result = pipeline_settings.print_task_result
            parallel_transformer.node_name = parallel_node_name
            steps.append(parallel_transformer)
            # update nodename2transformer
            nodename2transformer[parallel_node_name] = parallel_transformer


            
        elif trans_name=="pipeline":
            # recursive function help update node_pairs, latest_node and index
            _pipeline, \
            node_name_set, \
            _node_pairs, \
            node_name, \
            latest_node, \
            index, \
            parallel_index, \
            nodename2transformer= recursive_build_pipeline_from_cfg(    trans_cfg, 
                                                                        node_name_set, 
                                                                        [], 
                                                                        node_name,
                                                                        latest_node,
                                                                        index, 
                                                                        parallel_index, 
                                                                        nodename2transformer,
                                                                        pipeline_settings,
                                                                        kafka_media)
            # update steps
            node_pairs.append(_node_pairs)
            steps.append(_pipeline)
        
        else:
            index = index + 1
            pre_node_name = node_name
            node_name = f"{str(index)}.{trans_name}"
            # breakpoint=trans_cfg.pop("breakpoint") if "breakpoint" in trans_cfg else 0
            description = trans_cfg.pop("description") if "description" in trans_cfg else ""
            module_type = trans_cfg.pop("module_type") if "module_type" in trans_cfg else ""
            TRANSFORMERS = get_register(module_type, pipeline_settings.default_type)
            transformer = build_transformer_from_cfg(trans_cfg, TRANSFORMERS)
            transformer.index = index
            transformer.node_name = node_name
            transformer.description = description
            transformer.breakpoint = breakpoint
            transformer.print_task_result = pipeline_settings.print_task_result
            transformer.exchange_media = pipeline_settings.exchange_media
            transformer.kafka_media = kafka_media
            
            # update steps list
            steps.append(transformer)
            # update nodename2transformer
            nodename2transformer[node_name] = transformer
            # set pre_node_name
            transformer.pre_node_name = pre_node_name
            # update node_pairs
            if isinstance(latest_node, str):
                node_pairs.append((latest_node, node_name))
            elif isinstance(latest_node, list):
                for item in latest_node:
                    node_pairs.append((item, node_name))
            node_name_set.add(node_name)
            #update latest_node
            latest_node = node_name

    # remove empty node in node pair
    # simple_node_pairs = [item for item in simple_node_pairs if item[0]!=""]
    node_name_set = set([node_name for node_name in node_name_set if node_name!=""])


    return make_pipeline(*steps), \
            node_name_set, \
            node_pairs, \
            node_name, \
            latest_node, \
            index, \
            parallel_index, \
            nodename2transformer
            

def create_tranformers_dict(transformers):
    id2transformer = {}
    nodename2transformer = {}
    for transformer in transformers:
        id2transformer[transformer.index] = transformer
        nodename2transformer[transformer.node_name] = transformer

    return id2transformer, nodename2transformer


# when build_pipeline, it will return Pipeline
class Pipeline(sklearn_pipeline):
    def __init__(self, 
                 steps, 
                 *, 
                 memory=None,
                 verbose=False,
                 pipe_start=1,
                 pipe_stop=None):
        
        self.steps = steps
        self.memory = memory
        self.verbose = verbose
        self.pipe_start = pipe_start
        self.pipe_stop = pipe_stop
        self.delete_kafka_topic = 1
        self.kafka_media=None
        
    
    def _islice(self, target_list, start, end):
        total = len(target_list)
        assert end <=total, "end is higher total elements"
        
        selected_elements=None
        
        if start>0 and end ==-1:
            selected_elements = target_list[start-1:]
        elif start<0 and end==-1:
            selected_elements = target_list[start:]
        elif start>0 and end >0:
            selected_elements = target_list[start-1:end]
        elif start<0 and end <0:
            selected_elements = target_list[start:end+1]
        elif start>0 and end <0:
            selected_elements = target_list[start-1:end+1]
            
        return selected_elements

    
    def _iter(self):
        # print("running _iter #########################")
        if self.pipe_stop ==None:
            self.pipe_stop = len(self.steps)
        for idx, (name, trans) in enumerate(self._islice(self.steps, self.pipe_start, self.pipe_stop)):
            yield idx, name, trans
        
        
    def select_transformers(self, pipe_start=None, pipe_stop=None):
        self.pipe_start = pipe_start
        self.pipe_stop = pipe_stop
        new = copy.deepcopy(self)
        
        new.steps = self._islice(self.steps, self.pipe_start, self.pipe_stop)

        new.steps[0][1].is_first_trans = 1
        new.steps[-1][1].is_last_trans = 1
        
        return new

    def _can_transform(self):
        return self._final_estimator == "passthrough" or hasattr(
            self._final_estimator, "transform"
        )


    def transform(self, X):
        Xt = X

        # to be coding
        # creating kafka topic with tempname

        for idx, _, transformer in self._iter():
            
            # print(type(transformer), "#####################")
            Xt = transformer.transform(Xt)
            

            if hasattr(transformer, "breakpoint"):
                if transformer.breakpoint:
                    # print(transform.node_name, "has breakpoint", transform.breakpoint)
                    datetime_str = get_datetime_str(format="%Y-%m-%d %H:%M:%S")
                    print(f"{datetime_str} stop with breakpoint at {transformer.node_name}") if transformer.print_task_result else ""
                    return Xt
        
        # to be coding
        if self.delete_kafka_topic:
            # delete kafka topic
            pass 

        return Xt
    


class pipeline_settings():
    def __init__(self, cfg):

        self.pipeline_settings = cfg.pop("pipeline_settings") if "pipeline_settings" in cfg else {"print_cfg":0, "print_task_result":0}
        self.print_cfg, self.print_task_result = self.get_pipeline_settings_from_cfg()
        self.exchange_media = self.pipeline_settings["exchange_media"] if "exchange_media" in self.pipeline_settings else "default"
        self.delete_kafka_topic = self.pipeline_settings["delete_kafka_topic"] if "delete_kafka_topic" in self.pipeline_settings else 1
        self.bootstrap_servers = self.pipeline_settings["bootstrap_servers"] if "bootstrap_servers" in self.pipeline_settings else []
        self.default_type = self.pipeline_settings["module_type"] if "module_type" in self.pipeline_settings else ""
        print(f"The default module type for this pipeline is set as {self.default_type}")
    
    def get_pipeline_settings_from_cfg(self):
        
        print_cfg = self.pipeline_settings.pop("print_cfg") if "print_cfg" in self.pipeline_settings else 0
        print_task_result = self.pipeline_settings.pop("print_task_result") if "print_task_result" in self.pipeline_settings else 0

        return print_cfg, print_task_result
        

class DataPipeline:
    """
    usage
    --------------
    pipe = DataPipeline(cfg)
    pipe.transformer()

    UI Editing
    --------------
    self.generate_node_text()
    """
    def __init__(self, cfg):
        #------------------------- pipeline_settings 
        self._pipeline_settings = pipeline_settings(cfg)
        self._print_cfg, \
        self._print_task_result = self._pipeline_settings.get_pipeline_settings_from_cfg()

        if self._print_cfg:
            print("".join(["-" for i in range(80)]), "pipeline configuration", "".join(["-" for i in range(80)]))
            print(cfg)
            print("".join(["-" for i in range(80)]), "----------------------", "".join(["-" for i in range(80)]))


        self.kafka_media = None
        if self._pipeline_settings.exchange_media=="kafka":
            if self._pipeline_settings.bootstrap_servers:
                from .kafka_media import kafkaMedia
                # print("self._pipeline_settings.bootstrap_servers", self._pipeline_settings.bootstrap_servers)
                self.kafka_media = kafkaMedia(bootstrap_servers=self._pipeline_settings.bootstrap_servers, topic="pipeline")
                self.kafka_media.__enter__()
                # print(self.kafka_media.producer, "#############################")


        self._cfg = cfg
        self._node_name_set=set()
        self._node_pairs = []
        self._latest_node = ""
        self._index = 0
        self._parallel_index=0
        self._dot = None
        self._nodename2transformer={}
        if self._cfg:
            self._pipeline = self.build_pipeline_from_cfg()
            self.steps = self._pipeline.steps
        else:
            self._pipeline=None
            self.steps=[]

        self.limit = 40 #text line limit of characters in node
        # self.nodes_text = init_nodes_text(self._nodename2transformer)

    def __enter__(self, ):
        # tran = paramiko.Transport((self.host, int(self.port)))
        # tran.connect(username=self.username, password=self.password)
        # self.transport = tran

        # try:        
        #     sftp = paramiko.SFTPClient.from_transport(self.transport)
        #     self.sftp = sftp
        #     return self
        # except:
        #     self.transport.close()
            # raise
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        # self.sftp.close()
        # self.transport.close()
        pass

    def build_pipeline_from_cfg(self):

        
        _pipeline, \
        self._node_name_set, \
        self._node_pairs, \
        _note_name, \
        self._latest_node, \
        index, \
        parallel_index, \
        self._nodename2transformer= recursive_build_pipeline_from_cfg(  self._cfg, 
                                                                        self._node_name_set,
                                                                        self._node_pairs, 
                                                                        "",
                                                                        self._latest_node, 
                                                                        self._index,
                                                                        self._parallel_index,
                                                                        self._nodename2transformer,
                                                                        self._pipeline_settings,
                                                                        self.kafka_media)

        # setting first and last trans
        if _pipeline.steps:
            _pipeline.steps[0][1].is_first_trans = 1
            _pipeline.steps[-1][1].is_last_trans = 1

        return _pipeline


    def build_digraph(self):
        """
        Tutorial: https://graphviz.readthedocs.io/en/stable/examples.html
        Note: graphviz.Graph have no direction, so no arrowhead

        Variable Dependencies:
            - self._node_pairs
            - self._nodename2transformer
            - self._node_name_set
        """

        # init the digraph object
        self._dot = init_digraph()

        # setting digraph attributes
        self._dot.attr('node', 
                        shape="rect", 
                        style="filled", 
                        fillcolor="skyblue4", 
                        color="white", 
                        fontcolor="white")


        # create node for digraph
        add_dot_node(self, self._nodename2transformer, self._node_name_set)
            
            

        # create edges
        self._pre_dot, \
        self._dot, \
        parallel_index, \
        pipeline_index = recursive_build_digraph(self._dot, self._dot, self._node_pairs, 0, 0)


        return self



    def save_png(self, out_file):
        if out_file:
            ext = "." + out_file.split(".")[-1]
            out_file = out_file.replace(ext, "")
            # print(out_file)
            self._dot.render(out_file).replace("\\", "/")
    

    def output_graph(self):
        with tempfile.NamedTemporaryFile(suffix=".png") as f:
            # print(f.name)
            dirname = os.path.dirname(f.name)
            base_name = os.path.basename(f.name)
            filename = base_name.replace(".png", "")
            self._dot.render(os.path.join(dirname, filename)).replace("\\", "/")
            return f.name
        
        return ""

    def send_api_graph(self):
        with tempfile.NamedTemporaryFile(suffix=".png") as f:
            # print(f.name)
            dirname = os.path.dirname(f.name)
            base_name = os.path.basename(f.name)
            filename = base_name.replace(".png", "")
            self._dot.render(os.path.join(dirname, filename)).replace("\\", "/")
            return send_file(f.name, as_attachment=True, attachment_filename=base_name)

    def transform(self, input):
        return self._pipeline.transform(input)


def recursive_build_node_from_steps(steps, 
                                    node_name_set, 
                                    node_pairs, 
                                    node_name,
                                    latest_node, 
                                    index, 
                                    parallel_index, 
                                    nodename2transformer,
                                    pipeline_settings,
                                    kafka_media):

    for step_tuple in steps:

        trans_name = step_tuple[0]
        transformer = step_tuple[1]


        if isinstance(transformer, parallelTransformer):

            parallel_name = "parallel"
            parallel_index +=1
            parallel_node_name = f"{parallel_name}_no.{parallel_index}"

            transformers_list = []
            parallel_latest_node = []
            parallel_node_pairs = {}
            latest_nodes = None

            # prepare latest_nodes
            if isinstance(latest_node, str):
                latest_nodes = [latest_node for i in range(len(transformer.transformers))]
                pre_node_names = [node_name for i in range(len(transformer.transformers))]
            elif isinstance(latest_node, list):
                latest_nodes = latest_node
                pre_node_names = node_name
            else:
                assert False, "latest_node is not str or list"

            parallel_dict_index = [i for i in range(len(latest_nodes))]

            # dealing the transformers inside the parallelTransformer
            for i, node_name, latest_node, sub_transformer in zip( parallel_dict_index, 
                                                        pre_node_names,
                                                        latest_nodes, 
                                                        transformer.transformers):

                ###################################### dealing with pipeline
                if isinstance(sub_transformer, DataPipeline):
                    node_name_set, \
                    _node_pairs, \
                    node_name, \
                    latest_node, \
                    index, \
                    parallel_index, \
                    nodename2transformer = recursive_build_node_from_steps( sub_transformer.steps,
                                                                            node_name_set,
                                                                            node_pairs, 
                                                                            latest_node, 
                                                                            index, 
                                                                            parallel_index, 
                                                                            nodename2transformer,
                                                                            pipeline_settings,
                                                                            kafka_media)
                    node_pairs.append(_node_pairs)

                else:
                ####################################### dealing with real transformer
                    index = index + 1
                    description = sub_transformer.description if sub_transformer.description else ""
                    sub_transformer.pre_node_name = node_name
                    sub_transformer.index = index
                    _tuple = _name_estimators([sub_transformer])
                    sub_transformer.node_name = f"{str(index)}.{_tuple[0][0]}"
                    sub_transformer.description = description
                    sub_transformer.print_task_result = pipeline_settings.print_task_result
                    sub_transformer.exchange_media = pipeline_settings.exchange_media
                    sub_transformer.kafka_media = kafka_media
                    transformers_list.append(sub_transformer)
                    # update nodename2transformer
                    nodename2transformer[sub_transformer.node_name] = sub_transformer
                    # update steps list
                    previous_node, _latest_node = update_node(latest_node, sub_transformer.node_name)
                    parallel_node_pairs[f"process_no.{str(i)}"] = (previous_node, _latest_node)
                    node_name_set.add(_latest_node)
                    parallel_latest_node.append(_latest_node)



            ################################################# dealing with the parallelTransformer
            # update latest_node
            previous_node, latest_node = update_node(latest_node, parallel_latest_node)
            # update node_pairs
            node_pairs.append(parallel_node_pairs)
            nodename2transformer[parallel_node_name] = transformer

        elif isinstance(transformer, DataPipeline):
            node_name_set, \
            _node_pairs, \
            node_name, \
            latest_node, \
            index, \
            parallel_index, \
            nodename2transformer = recursive_build_node_from_steps( sub_transformer.steps,
                                                                    node_name_set,
                                                                    [], 
                                                                    latest_node, 
                                                                    index, 
                                                                    parallel_index, 
                                                                    nodename2transformer,
                                                                    pipeline_settings,
                                                                    kafka_media)
            node_pairs.append(_node_pairs)
        
        else:

            index = index + 1
            pre_node_name = node_name
            description = transformer.description if transformer.description else ""
            transformer.index = index
            transformer.node_name = f"{str(index)}.{trans_name}"
            transformer.description = description
            transformer.print_task_result = pipeline_settings.print_task_result
            transformer.exchange_media = pipeline_settings.exchange_media
            transformer.kafka_media = kafka_media

            # update nodename2transformer
            nodename2transformer[transformer.node_name] = transformer
            # set pre_node_name
            transformer.pre_node_name = pre_node_name
            # update node_pairs
            if isinstance(latest_node, str):
                node_pairs.append((latest_node, transformer.node_name))
            elif isinstance(latest_node, list):
                for item in latest_node:
                    node_pairs.append((item, transformer.node_name))

            # add current node name to the node_name_set
            node_name_set.add(transformer.node_name)

            #update latest_node
            latest_node = transformer.node_name
        
    node_name_set = set([node_name for node_name in node_name_set if node_name!=""])

    return node_name_set, node_pairs, latest_node, index, parallel_index, nodename2transformer

def build_pipeline(*steps):

    
    steps_tuples = _name_estimators(steps)

    self = DataPipeline("")
    # self.limit = 40 #text line limit of characters in node

    self._node_name_set, \
    self._node_pairs, \
    self._latest_node, \
    _, \
    _, \
    self._nodename2transformer = recursive_build_node_from_steps(   steps_tuples,
                                                                    self._node_name_set,
                                                                    self._node_pairs, 
                                                                    "",
                                                                    self._latest_node, 
                                                                    self._index,
                                                                    self._parallel_index,
                                                                    self._nodename2transformer,
                                                                    self._pipeline_settings,
                                                                    self.kafka_media)

    # self.nodes_text = init_nodes_text(self._nodename2transformer)

    self._pipeline = make_pipeline(*steps)
    
    return self