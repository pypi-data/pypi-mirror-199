from tpes.environment import Environment
from tpes.data.instance import Instance
from tpes.instance_parser import InstanceParser, JSONInstanceParser
from tpes.instance_management import InstanceFactory, InstanceStateMachine, InstanceWriter, JSONInstanceWriter, TransitionRequest
from tpes.views.items import *
from tpes.data.workflow import Workflow
from tpes.views.workflow_details import WorkflowDetails
from tpes.workflow_parser import BPMNParser, XMLParser
import os.path

def get_workflow(path: str) -> Workflow:
        parser = BPMNParser(XMLParser(path))
        return parser.parse()

def get_instance_state_machine(instance_path: str) -> InstanceStateMachine:
        parser = JSONInstanceParser(instance_path)
        instance: Instance = parser.parse()
        return InstanceStateMachine(instance)

class CommandExecutor:
    def read(self, workflow: (str, "Workflow given to be displayed")):
        workflow_obj = get_workflow(workflow)
        return WorkflowDetails(TextItem(workflow), ListItem(workflow_obj.nodes), ListItem(workflow_obj.connections), ListItem(workflow_obj.data_objects))
    def show(self, workflow: str, id: str):
        workflow_obj = get_workflow(workflow)
        return workflow_obj.find_node(id)
    def next(self, id: str, workflow: str, *, show_ids_only: bool = False):
        workflow_obj = get_workflow(workflow)
        mynode = workflow_obj.find_node(id)
        if mynode is not None:
            if show_ids_only:
                return "\n".join([n.id for n in workflow_obj.get_next(mynode)])
            else:
                return ListItem(workflow_obj.get_next(mynode))
        else:
            return None
    def start(self, instance: str, workflow: str, *, parent_instance: str = None):
        instance_path = instance
        workflow_path = workflow
        workflow = get_workflow(workflow_path)
        instance_name = os.path.basename(instance_path)
        if instance_name.endswith(".json"):
            instance_name = instance_name[:-5]
        factory = InstanceFactory(workflow, instance_name, {}, None)
        instance:Instance = factory.parse()
        instance.path = instance_path
        print("Parent path: %s" % parent_instance)
        if parent_instance is not None:
            print("Path is not none")
            instance.parent = get_instance_state_machine(parent_instance).instance
        writer = JSONInstanceWriter()
        writer.write(instance)
        env = Environment()
        for do in instance.workflow.data_objects:
            print("Producing " + do.title)
            env.produce_document(instance, do.title)
        return instance 
    def state(self, instance: str, *, show_all: bool = False, show_ids_only: bool = False):
        instance_path = instance
        if show_all:
            return get_instance_state_machine(instance_path).instance
        else:
            if not show_ids_only:
                return ListItem(get_instance_state_machine(instance_path).instance.states)
            else:
                return "\n".join([
                    state.id for state in get_instance_state_machine(instance).instance.states
                ])
    def next_states(self, instance: str):
        sm = get_instance_state_machine(instance)
        return {
            state.id: sm.instance.workflow.get_next(state) for state in sm.instance.states
        }
    def info(self, instance: str):
        i = get_instance_state_machine(instance).instance
        if i.parent is not None:
            print("Parent available")
            i.parent = i.parent.name
        return i
    def follow(self, instance: str, *, save: bool = False):
        sm = get_instance_state_machine(instance)
        tasks = sm.advance(sm.instance.tasks)
        if save:
            sm.instance.tasks += tasks
            writer = JSONInstanceWriter()
            writer.write(sm.instance)
        return ListItem([x[0] for x in tasks])
    
    def resolve(self, instance: str, state: str):
        sm = get_instance_state_machine(instance)
        state = sm.instance.workflow.find_node(state)
        transition = sm.next(state)
        sm.instance.states = [s for s in sm.instance.states if s != state]
        writer = JSONInstanceWriter()
        if transition.request == TransitionRequest.CREATE_CHILD_INSTANCES:
            print("Create child instances and then continue.")
            print("Do you want to continue? (y/n)")
            answer = str(input(">> "))
            if answer == "y":
                sm.instance.states += transition.new_states
                writer.write(sm.instance)
        elif transition.request == TransitionRequest.SELECT_ONE:
            print("Select one of the following next states:")
            for i, s in enumerate(transition.new_states):
                print("%d: %s %s" % (i+1, s.type, s.title))
            answer = int(input(">> "))
            sm.instance.states += [transition.new_states[answer - 1]]
            writer.write(sm.instance)
        elif transition.request == TransitionRequest.SELECT_SUNSET:
            print("Select subset of the following tasks:")
            for i, s in enumerate(transition.new_states):
                print("%d: %s %s" % (i+1, s.type, s.title))
            answer = [int(x) -1 for x in input(">> ").split(" ")]
            for x in answer:
                sm.instance.states.append(transition.new_states[x])
            writer.write(sm.instance)
        else:
            print("Manual intervention required.")
            print("Enter IDs of nodes in workflow you want to replace this node with.")
            answer = input(">> ").split(" ")
            for a in answer:
                sm.instance.states.append(sm.instance.workflow.find_node(a))
            writer.write(sm.instance)
        return ListItem(sm.instance.states)
    def todo(self, instance: str, *, group_by: str =""):
        sm = get_instance_state_machine(instance)
        result = [] 
        for task, h in sm.instance.tasks:
            result.append(task.title + (" - %fh" % sm.instance.evaluate(task, "time")))
        return "\n".join(result)
        
