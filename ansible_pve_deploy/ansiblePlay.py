import json
import shutil
from collections import namedtuple
import ansible
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C


# Ansible part of script
class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        self.json = json.dumps({host.name: result._result}, indent=4)
        return self

class ansiblePlay(object):
    

    def ansibleRun(self, _module, _host, _qm, _args, _ansible_hosts_file):

        # since API is constructed for CLI it expects certain options to always be set, named tuple 'fakes' the args parsing options object
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'private_key_file', 'become', 'become_method', 'become_user', 'check', 'diff'])
        options = Options(connection='ssh', module_path=['/to/mymodules'], forks=10, private_key_file=None, become=False, become_method=None, become_user=None, check=False, diff=False)
        # initialize needed objects
        loader = DataLoader() # Takes care of finding and reading yaml, json and ini files
        passwords = dict(vault_pass='secret')
        results_callback = ResultCallback()
        inventory = InventoryManager(loader=loader, sources=_ansible_hosts_file)
        variable_manager = VariableManager(loader=loader, inventory=inventory)

        

        play_source =  dict(
            name = "Ansible Play",
            hosts = _host,
            gather_facts = 'no',
            tasks = [
                dict(action=dict(module=_module + _qm , args= _args) ),
                ]
            )

        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)


        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=passwords,
                #stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
            )
            
            result = tqm.run(play) # most interesting data for a play is actually sent to the callback's methods
        finally:
            # we always need to cleanup child procs and the structres we use to communicate with them
            if tqm is not None:
                tqm.cleanup()

            # Remove ansible tmpdir
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
        return results_callback

    def ansibleRunJson(self, _module, _host, _qm, _args, _ansible_hosts_file):

        # since API is constructed for CLI it expects certain options to always be set, named tuple 'fakes' the args parsing options object
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'private_key_file', 'become', 'become_method', 'become_user', 'check', 'diff'])
        options = Options(connection='ssh', module_path=['/to/mymodules'], forks=10, private_key_file=None, become=False, become_method=None, become_user=None, check=False, diff=False)
        # initialize needed objects
        loader = DataLoader() # Takes care of finding and reading yaml, json and ini files
        passwords = dict(vault_pass='secret')
        results_callback = ResultCallback()
        inventory = InventoryManager(loader=loader, sources=_ansible_hosts_file)
        variable_manager = VariableManager(loader=loader, inventory=inventory)

        

        play_source =  dict(
            name = "Ansible Play",
            hosts = _host,
            gather_facts = 'no',
            tasks = [
                dict(action=dict(module=_module + _qm , args= _args) ),
                ]
            )

        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)


        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=passwords,
                stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
            )
            
            result = tqm.run(play) # most interesting data for a play is actually sent to the callback's methods
        finally:
            # we always need to cleanup child procs and the structres we use to communicate with them
            if tqm is not None:
                tqm.cleanup()

            # Remove ansible tmpdir
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
        return results_callback


    def ansibleRunBecome(self, _module, _host, _qm, _args, _ansible_hosts_file, _ansible_password):

        # since API is constructed for CLI it expects certain options to always be set, named tuple 'fakes' the args parsing options object
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'private_key_file', 'become', 'become_method', 'become_user', 'check', 'diff'])
        options = Options(connection='ssh', module_path=['/to/mymodules'], forks=10, private_key_file=None, become=True, become_method='sudo', become_user='root', check=False, diff=False)
        # initialize needed objects
        loader = DataLoader() # Takes care of finding and reading yaml, json and ini files
        passwords = dict(vault_pass='')
        results_callback = ResultCallback()
        inventory = InventoryManager(loader=loader, sources=_ansible_hosts_file)
        variable_manager = VariableManager(loader=loader, inventory=inventory)
        variable_manager.extra_vars = {'ansible_become_password' : _ansible_password}


        play_source =  dict(
            name = "Ansible Play",
            hosts = _host,
            gather_facts = 'no',
            tasks = [
                dict(action=dict(module=_module + _qm , args= _args) ),
                ]
            )

        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)


        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=passwords,
                #stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
            )
            result = tqm.run(play) # most interesting data for a play is actually sent to the callback's methods
            return result    
        finally:
            # we always need to cleanup child procs and the structres we use to communicate with them
            if tqm is not None:
                tqm.cleanup()

            # Remove ansible tmpdir
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)