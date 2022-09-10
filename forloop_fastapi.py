from typing import Optional, Any, List, Dict, AnyStr

from fastapi import FastAPI

from pydantic import BaseModel

description = """
This API helps you to use Forloop.ai anywhere. 🚀
"""


app = FastAPI(title="Forloop.ai API",
    description=description,
    version="0.8.0",
    )


from src.node_context_manager import node_context_manager

import uvicorn

from src.pipeline_function_handlers import pipeline_function_handler_dict



class APINode(BaseModel):
    pos:List[int]=[0,0]
    typ:str="Custom"
    params:Dict[str, Any]
    project_key:str=""
    
    
class DeleteNode(BaseModel):
    project_key:str=""
        
class APIPipeline(BaseModel):
    name:str
    nodes_uids:List[int]
    active_nodes_uids:int
    

@app.get("/api/v1/nodes")
def get_nodes():
    return {"nodes": node_context_manager.nodes}


@app.post("/api/v1/nodes")
def new_node(node : APINode):
    forloop_node=node_context_manager.new_node(node.pos,node.typ,node.params,node.project_key)
    print("API NEW NODE",forloop_node,forloop_node.uid,forloop_node.pos,forloop_node.typ,forloop_node.params,forloop_node.project_key)
    return {
        "node_uid":forloop_node.uid,
        "pos":forloop_node.pos,
        "typ":forloop_node.typ,
        "params":forloop_node.params,
        "project_key":forloop_node.project_key
        }


@app.delete("/api/v1/node/{node_uid}")
def delete_node(node_uid: Optional[int]=None):  
    node_context_manager.delete_node_by_uid(node_uid)  
    return {"ok":True}

@app.delete("/api/v1/nodes")
def delete_nodes(delete_node: DeleteNode):  
    project_key=delete_node.project_key
    node_context_manager.nodes=[x for x in node_context_manager.nodes if x.project_key!=project_key]
    return {"ok":True}

@app.put("/api/v1/move_node/{node_uid}")
def move_node(node_uid: Optional[int]=None, new_pos:List[int]=[0,0], new_pos2:List[int]=[0,0],): # new_pos2 here is for a reason -> it would not match the Pydantic model    
    node_context_manager.move_node_by_uid(node_uid, new_pos)  
    return {"ok":True}



#UpdateNodeModel

#pos:List[int]=[0,0], typ:AnyStr="Custom", params:Dict[str,Any]={}
@app.put("/api/v1/update_node/{node_uid}")
def update_node(node_uid: Optional[int]=None, item:APINode=None): # new_pos2 here is for a reason -> it would not match the Pydantic model    
    """
    AnyStr was chosen in order to put it in the request body - explanation:
    The function parameters will be recognized as follows:
    If the parameter is also declared in the path, it will be used as a path parameter.
    If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
    If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.
    """    
    print(item)
    print(item.dict())
    node_context_manager.update_node_by_uid(node_uid, item.pos, item.typ, item.params)  
    return {"ok":True}




@app.post("/api/v1/direct_execute_node/{node_uid}")
def direct_execute_node(node_uid):  
    node=[x for x in node_context_manager.nodes if x.uid==node_uid][0]
    typ=node.typ
    pipeline_function_handler_dict[typ]
    return {}


@app.get("/api/v1/export_node_code/{node_uid}")
def export_node_code(node_uid): 
    
    matching_nodes=[x for x in node_context_manager.nodes if x.uid==int(node_uid)]
    if len(matching_nodes)==1:
        node=matching_nodes[0]
        typ=node.typ
        pipeline_function_handler=pipeline_function_handler_dict[typ]
        code=pipeline_function_handler.export_code()
        imports=pipeline_function_handler.export_imports()
        #print(code)
        #TODO: To be implemented
        return {"imports":imports,"code":code}
    else:
        return {"imports":None,"code":None}


@app.post("/api/v1/pipelines")
def new_pipeline(pipeline : APIPipeline):
    forloop_pipeline=node_context_manager.new_pipeline(pipeline.name,pipeline.nodes_uid,pipeline.active_nodes_uids) #TODO: To be implemented
    return {
        }

@app.get("/api/v1/pipelines")
def get_pipelines():
    return {"nodes": node_context_manager.pipelines}

@app.delete("/api/v1/pipeline/{pipeline_uid}")
def delete_pipeline(pipeline_uid: Optional[int]=None):  
    node_context_manager.delete_pipeline_by_uid(pipeline_uid)  
    return {"ok":True}

@app.post("/api/v1/direct_execute_pipeline/{pipeline_uid}")
def direct_execute_pipeline(pipeline_uid):  
    #TODO: To be implemented
    return {}



@app.get("/api/v1/export_pipeline_code/{pipeline_uid}")
def export_pipeline_code(pipeline_uid):  
    
    #TODO: To be implemented
    return {}



def run_api():
    uvicorn.run(app)
