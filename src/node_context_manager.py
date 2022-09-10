from src.nodes import Node
#from src.gui_layout_context import glc
import src.flog as flog

from src.pipeline_function_handlers import pipeline_function_handler_dict


class NodeContextManager:
    """Singleton manager handling backend of existing nodes and pipelines - in future will force the frontend to draw its information"""
    def __init__(self):
        self.nodes=[]
        self.edges=[]
        self.pipelines=[]
        

    def get_node_by_uid(self,node_uid):
        matching_nodes=[node for node in self.nodes if node.uid==node_uid]
        assert len(matching_nodes)<=1
        if len(matching_nodes)==1:
            return(matching_nodes[0])
        elif len(matching_nodes)==0:
            flog.info("Node was not found, couldn't be deleted")
            return(None)
        else:
            flog.info("Multiple nodes with duplicate uid exist")
            return(None)

    def new_node(self,pos=[0,0],typ="Custom",params={},project_key=""):
        node=Node(pos,typ,params,project_key=project_key)
        print("NODE",node,node.pos,node.typ,node.params)
        self.nodes.append(node)
        return(node)
        
    
    def delete_node(self,node):
        index=self.nodes.index(node)
        self.nodes.pop(index)
        
        
    def move_node(self,node,new_pos):
        index=self.nodes.index(node)
        self.nodes[index].pos=new_pos
        

    def update_node(self,node,pos,typ,params):
        index=self.nodes.index(node)
        self.nodes[index].pos=pos
        self.nodes[index].typ=typ
        self.nodes[index].params=params
        
            
        
    def delete_node_by_uid(self,node_uid):
        node=self.get_node_by_uid(node_uid)
        try:
            self.delete_node(node)
        except Exception as e:
            print("Node couldn't be deleted",e)
    
            
    def move_node_by_uid(self,node_uid,new_pos):
        node=self.get_node_by_uid(node_uid)
        try:
            self.move_node(node,new_pos)
        except Exception as e:
            print("Node couldn't be moved",e)
    
    def update_node_by_uid(self,node_uid, pos, typ, params):
        node=self.get_node_by_uid(node_uid)
        try:
            self.update_node(node,pos,typ,params)
        except Exception as e:
            print("Node couldn't be updated",e)
    
    
    def export_node_code_by_uid(self,node_uid):
        node=self.get_node_by_uid(node_uid)
        typ=node.typ
        handler=pipeline_function_handler_dict[typ]
        exported_code=handler.export_code()
        
        return(exported_code)
        
    
        
    def reset_pipeline_grid(self):
        self.nodes=[]
        self.edges=[]
    

node_context_manager=NodeContextManager()
#glc.node_context_manager=NodeContextManager()
