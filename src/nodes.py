from dataclasses import dataclass, field
from typing import ClassVar, Any, Dict, List


from src.node_option_form import NodeOptionForm
from src.item_detail_form import NodeDetailForm

from src.pipeline_function_handlers import pipeline_function_handler_dict #TODO: Refactor out
from src.function_handlers.variable_handler import ForloopStoredVariable,variable_handler


@dataclass
class Node:
    pos: List[Any]
    typ: str
    params: Dict[str, Dict[str, Any]] = field(compare=False, default_factory=dict, repr=False)
    project_key: str=""  
    
    # "params": {"x": {"variable": "click_x", "value": "200"}, {"y": {"variable": None, "value": "100"}}}
    node_detail_form: NodeDetailForm = field(default=None)
    node_option_form: NodeOptionForm = field(default=None)
    uid: int = field(init=False)
    instance_counter: ClassVar[int] = 0
    

    def __post_init__(self):
        self.__class__.instance_counter += 1
        self.uid = self.instance_counter
        
            

    def __hash__(self):
        return hash((self.typ, self.uid))

    def __str__(self):
        params = ' '.join(map(str, self.get_params().values()))
        return f'{self.typ}({params})' if params else self.typ

    def __call__(self):
        self.execute()
    
    def execute(self):
        try:
            handler = pipeline_function_handler_dict[self.typ]
        except KeyError:
            raise NotImplementedError(f'Node type {self.typ} is not implemented yet.')
        params = self.get_params().values()
        #print("PARAMS",params)
        
        if hasattr(handler,"direct_execute"):
            #print("PARAMS ", params)
            result=handler.direct_execute(*params)
        else:
            result=handler.execute(list(params))
    
        return result
        

    def get_params(self):
        kwargs = {}
        #print("self.params",self.params)
        for key, values in self.params.items():
            variable = values.get('variable')
            if variable is None:
                var_value = values.get('value')
            else:
                var_value = variable_handler.get(variable)
                # if var_value is None:
                #     logger.warning(f'Variable {variable} is not stored or has a value of "None"')
                var_value = var_value.value if isinstance(var_value, ForloopStoredVariable) else values.get('value')
            kwargs[key] = var_value
        # return list(kwargs.values())
        return kwargs
