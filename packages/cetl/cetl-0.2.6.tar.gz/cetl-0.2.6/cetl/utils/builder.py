from .registry import Registry
import pandas as pd
DataFrame = pd.DataFrame
# pd.set_option('display.max_columns', None)

FUNCTIONAL_TRANSFORMERS = Registry("functional")
PANDAS_TRANSFORMERS = Registry("pandas")
JSON_TRANSFORMERS = Registry("json")
SPARK_TRANSFORMERS = Registry("spark")
TEST_TRANSFORMERS = Registry("test")
DB_MAPPERS = Registry("src_db_mappers")
DB_MODELS = Registry("db_models")
ALL_MODULES = {}
context_name="task_data"
default_module_type = "pandas"

def add_register(register=None):
    """usage
    from cetl.utils.register import Registry
    from cetl.utils.builder import add_register
    FILE_TRANSFORMERS = Registry("customer")
    add_register(register=FILE_TRANSFORMERS)
    """
    # get the register name
    register_name = register._name

    # check whether the register name already exist
    if register_name in ALL_MODULES:
        raise ValueError(f"The register name, {register_name} already exists")

    # add to ALL_MODULES
    ALL_MODULES[register_name] = register


for register in [   FUNCTIONAL_TRANSFORMERS,
                    PANDAS_TRANSFORMERS, 
                    JSON_TRANSFORMERS, 
                    SPARK_TRANSFORMERS, 
                    TEST_TRANSFORMERS,
                    DB_MAPPERS,
                    DB_MODELS]:

    add_register(register=register)



def get_register(module_type, default_type=None):
    # print("module_type:", module_type)
    TRANSFORMERS=None
    # module_type is like "pandas", "json" or "spark"
    # print("what is the content of all_modules", ALL_MODULES)

    if module_type=="":
        if not default_type:
            TRANSFORMERS = ALL_MODULES[default_module_type]
            return TRANSFORMERS
        else:
            TRANSFORMERS = ALL_MODULES[default_type]

    if module_type in ALL_MODULES:
        TRANSFORMERS = ALL_MODULES[module_type]
        return TRANSFORMERS
    else:
        print("ALL_MODULES", ALL_MODULES.keys())
        print(f"module_type, {module_type} is not recognized by cetl")
        assert False



def build_transformer_from_cfg(cfg, registry, parallel_transformers=None):
    args = cfg.copy()
    transformer_type = args.pop("type")
    
    if transformer_type not in registry.module_dict:
        print("current registry is ", registry._name)
        raise ValueError(f"transformer_type {transformer_type} not exists")

    cls_obj = registry.module_dict[transformer_type]
        
    
    transformer=None
    if transformer_type=="parallelTransformer":
        transformer = cls_obj(parallel_transformers)
        
    else:
        transformer = cls_obj(**args)

    return transformer