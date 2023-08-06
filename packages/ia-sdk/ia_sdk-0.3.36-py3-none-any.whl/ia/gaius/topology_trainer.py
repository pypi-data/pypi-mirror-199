from ia.gaius.agent_client import AgentClient
from ia.gaius.utils import create_gdf
from inspect import signature

class TopologyTrainer():
    def __init__(self, agent: AgentClient, ingress_config: dict) -> None:
        """Initialize TopologyTrainer class

        Args:
            agent (AgentClient): GAIuS Agent
            ingress_config (dict): configuration for functions used, configs,
                nodes to observe on

        Raises:
            KeyError: when necessary field in ingress_config is missing
            Exception: When functions provided do not have *explicitly*
            correct parameters
        """
        self.agent = agent
        self.ingress_config = ingress_config
         
        if 'nodes' not in ingress_config:
            raise KeyError("nodes key missing from ingress config")
        if 'functions' not in ingress_config:
            raise KeyError("functions key missing from ingress config")
        if 'function_configs' not in ingress_config:
            raise KeyError("function_configs key missing from ingress config")

        self.ingress_nodes = self.ingress_config['nodes']
        accepted_keys = ['data', 'config']
        for node, ingress_function in self.ingress_config['functions'].items():
            sig = signature(ingress_function)
            parameter_keys = list(sig.parameters.keys())
            if not (all([key in accepted_keys for key in parameter_keys]) and len(parameter_keys) == len(accepted_keys)):
                raise Exception(f'function for node {node} has invalid parameters: {parameter_keys}, expected: {accepted_keys}')

        self.functions = self.ingress_config['functions']
        self.function_configs = self.ingress_config['function_configs']
        self.persistent_state = {k:None for k in self.functions}

        agent.connect()
        agent.set_ingress_nodes(nodes=self.ingress_config['nodes'])

        print(f'initialized TopologyTrainer')

        pass

    def __str__(self) -> str:
        return f'<TopologyTrainer for agent:{self.agent.__str__()}, IngressNodes={self.ingress_nodes}>'

    def observe(self, data):
        """Apply functions from ingress_config dictionary, then observe on
        corresponding ingress nodes

        Args:
            data: data before any modifications take place
        """
        print(f'initial data: {data}')
        for node in self.ingress_nodes:
            observation_gdf = self.functions[node](data=data, config=self.function_configs[node])
            print(f'{node}:{observation_gdf = }')
            self.agent.observe(data=observation_gdf, nodes=[node])

    def reset_agent(self):
        self.agent.clear_all_memory()
        self.persistent_state = {k:None for k in self.functions}

# example functions to be used as values in functions dict
def strings_only(data, config):
    """Observe only the strings from the gdf provided. No config needed"""
    try:
        return create_gdf(strings=data['strings'])
    except Exception as e:
        print(f'error in strings_only: {str(e)}')
        return create_gdf()

def vectors_only(data, config):
    """Observe only the vectors from the gdf provided. No config needed"""

    try:
        return create_gdf(vectors=data['vectors'])
    except Exception as e:
        print(f'error in vectors_only: {str(e)}')
        return create_gdf()

def emotives_only(data, config):
    """Observe only the strings from the gdf provided. No config needed"""

    try:
        return create_gdf(strings=data['emotives'])
    except Exception as e:
        print(f'error in emotives_only: {str(e)}')
        return create_gdf()

def emotives_as_strings(data, config):
    """Take emotives data and pass them in the strings field
    as KEY|VALUE data

    Args:
        data: expected gdf
        config (None): N/A

    Returns:
        dict: GDF
    """
    strings = []
    for k, v in data['emotives'].items():
        strings.append(f'{k}|{v}')
    return create_gdf(strings=strings)

def observe_nth_element(data, config):
    """Parse out the nth event from a sequence and return.
    Event number determined by 'n' field inside config dict

    Args:
        data (list): sequence of gdf events
        config (dict): configuration object

    Returns:
        dict: single event to be observed
    """
    return data[config['n']]
