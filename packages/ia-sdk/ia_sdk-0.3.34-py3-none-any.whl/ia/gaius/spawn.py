#!/usr/bin/env python3
import multiprocessing
from optparse import OptionParser
import os,sys
import docker
from sty import fg, bg
from ia.gaius.genome_info import Genome
import json
import logging as logger
import configparser
import socket
import platformdirs as plat
import shutil
import uuid
from ia.gaius.agent_client import AgentClient

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

ASSETS = {'network': {},
          'agent': None,
          'genome': None,
          'interfaces': {},
          'cp-containers': {},
          'mp-containers': {},
          'applications': {} ## These are connected containers as applications. Ex. JIA notebooks.
          }

def define_network(agent_name):
    networks = {}
    for n in docker_client.networks.list():
        networks[docker_client.networks.get(n.short_id).name] = n.short_id

    i = 0
    net_name = f"{agent_name}-{i}"
    while net_name in networks.keys():
        logger.info(f"    {fg.yellow}{net_name} already exists. Incrementing.{fg.rs}")
        i += 1
        net_name = f"{agent_name}-{i}"
    net = docker_client.networks.create(net_name)
    logger.info(f"{fg.green} Created {net.name} with id: {net.short_id} {fg.rs}")
    return net_name, net

def parse_genome(genome):

    targets_map = {} ## values are target IDs for each key
    sources_map = {} ## values are source IDs of each key

    if 'edges' not in genome.topology['elements']:
        logger.warn("No connections.")
    else:
        for edge in genome.topology['elements']['edges']:
            d = edge['data']
            if d['source'] not in targets_map:
                if d['source'].startswith("action"):
                    continue
                targets_map[d['source']] = [d['target']]
            else:
                if d['source'].startswith("action"):
                    continue
                targets_map[d['source']].append(d['target'])
            if d['target'] not in sources_map:
                if d['target'].startswith("action"):
                    continue
                sources_map[d['target']] = [d['source']]
            else:
                if d['target'].startswith("action"):
                    continue
                sources_map[d['target']].append(d['source'])

    targets_map = eval( f"{targets_map}".replace(", 'P1_ID': ['action1_ID', 'action2_ID']", ""))

    as_inputs = {pid: [] for pid in genome.primitives.keys() }
    is_input = []

    for pid, p in genome.primitives.items():
        logger.debug(f"{pid} ({p['name']}):")
        logger.debug(f"    {p['sources']}")
        if p['sources'] == ['observables']:
            as_inputs[pid] = []
        else:
            for mid in p['manipulatives']:
                if mid.startswith("action"):
                    continue
                logger.debug(f"   {mid} {genome.manipulatives[mid]['name']} {genome.manipulatives[mid]['genes']['sources']['value']}")
                if genome.manipulatives[mid]['genes']['sources']['value'] == ['observables']:
                    as_inputs[pid].append(mid)
                    is_input.append(mid)

    logger.debug('as_inputs', as_inputs)
    logger.debug('is_input', is_input)


    logger.debug(targets_map)
    ## for any manipulative that is an observables (i.e. in is_input list),
    ## remove that manipulative from targets of other manipulatives:
    for _id, targets in targets_map.items():
        for mid in is_input:
            logger.debug(f"Need to pop: {mid} from {targets}")
            while mid in targets:
                logger.debug(f"popping...{mid} from {_id}")
                targets_map[_id].pop(targets.index(mid))

    # print("PROCESSING OBSERVABLES MANIPULATIVES")
    for mid, x in genome.manipulatives.items():
        if ['observables'] == x['genes']['sources']['value']:
            sources_map[mid] = [x['primitive']]


    logger.debug("sources_map:")
    for k,v in sources_map.items():
        logger.debug(f"{k}:")
        for t in v:
            if t.startswith('action'):
                v.pop(v.index(t))
            else:
                logger.debug(f"    <---{t}")

    logger.debug("targets_map:")
    for k,v in targets_map.items():
        logger.debug(f"{k}:")
        for t in v:
            if t.startswith('action'):
                v.pop(v.index(t))
            else:
                logger.debug(f"    --->{t}")

    logger.debug("as_inputs:")
    for k,v in as_inputs.items():
        logger.debug(f"{k}:")
        for t in v:
            if t.startswith('action'):
                v.pop(v.index(t))
            else:
                logger.debug(f"    --->({t})")

    return sources_map, targets_map, as_inputs


def check_container_conflicts(p_ids, running_container_names):
    docker_client = docker.from_env()
    logger.info(f'checking container conflicts')
    for _id in p_ids:
        logger.debug(f'{_id=}')
        if _id in running_container_names:
            x = input(f"{bg.red}{fg.white} Conflicting containers! {_id} already exists.{bg.rs}{fg.rs} Okay to replace? Y/N: ")
            if x.lower() == 'y':
                c = docker_client.containers.get(_id)
                c.stop()
                c.remove()
            else:
                logger.debug(f"{bg.yellow}{fg.white} Aborting!{fg.rs}{bg.rs}")
                sys.exit()
    return

def startit(genome_file, BOTTLE_HOSTNAME=None,
                         REGISTRY=None,
                         VERSION=None,
                         API_KEY=None,
                         LOG_LEVEL=None,
                         NETWORK=None,
                         BIND_PORTS=None,
                         user_id = None,
                         agent_id = None):
    if user_id is None:
        raise Exception('no user id provided')
    if agent_id is None:
        raise Exception('no agent_id provided')
    docker_client = docker.from_env()
    container_extension = '-' + user_id + '-' +  agent_id

    logger.debug(f'{genome_file = }')
    try:
        with open(genome_file, 'r') as f:

            # read data into genome_json
            genome_json = f.read()
            _g = json.loads(genome_json)
            # convert json to python dictionary

    except OSError:
        try:
            genome_json = genome_file
            _g = json.loads(genome_file)
        except json.decoder.JSONDecodeError:
            logger.warn(f'Failed to retreive genome, {genome_file=}')
            sys.exit(-1)
    _g['description'] = 'cleared description'
    for d in _g['elements']['nodes']:
        if 'description' in d['data'].keys():
            logger.debug(f"Removing: {d['data']['description']}")
            d['data']['description'] = ''
    genome = Genome(_g)


    if not NETWORK:
        NETWORK="g2network"

    net_name = NETWORK + container_extension
    ## Does this network already exist?
    net_name_exists = False
    for n in docker_client.networks.list():
        if n.name == net_name:
            net_name_exists = True
            net = n
    if net_name_exists:
        logger.warn(f"error, {net_name} already exists!")
    else:
        net = docker_client.networks.create(net_name)
        logger.debug(f"{fg.green} Created {net.name} with id: {net.short_id} {fg.rs}")
    logger.debug(net_name)
    logger.debug(net)
    ASSETS['network'][net_name] = net

    sources_map, targets_map, as_inputs = parse_genome(genome)

    running_container_names = [c.name for c in docker_client.containers.list()]
    p_ids = list(genome.manipulative_map.keys() ) + list(genome.primitive_map.values()) + ['gaius-api']
    p_ids = [f'{_id}{container_extension}' for _id in p_ids]
    check_container_conflicts(p_ids, running_container_names)


    logger.debug("Starting Manipulative nodes...")
    for _id, m in genome.manipulative_map.items():
        if _id.startswith('action'): ## Needed for old testing topologies.
                continue
        manipulatives_genes = json.dumps(genome.manipulatives[_id])
        if _id in sources_map:
            sources = json.dumps(sources_map[_id])
        else:
            sources = json.dumps([])
        if _id in targets_map:
            targets = json.dumps(targets_map[_id])
        else:
            targets = json.dumps([])

        ASSETS['mp-containers'][_id] = docker_client.containers.run(name=_id + container_extension,
            image=f"{REGISTRY}manipulative-processor:{VERSION}",
            network=net_name,
            detach=True,
            init=True,
            hostname=_id,
            # publish_all_ports=True,
            restart_policy={"Name": "unless-stopped"},
            environment={'LOG_LEVEL': LOG_LEVEL,
                         'API_KEY': API_KEY,
                         'HOSTNAME': _id,
                         'MANIFEST': manipulatives_genes,
                         'SOURCES': sources,
                         'TARGETS': targets}
            )

    logger.debug("Starting Cognitive Processor nodes...")
    for p, _id in genome.primitive_map.items():
        primitive_genes = json.dumps(genome.primitives[_id])
        if _id in sources_map:
            sources = json.dumps(sources_map[_id])
        else:
            sources = json.dumps([])
        if _id in targets_map:
            targets = json.dumps(targets_map[_id])
        else:
            targets = json.dumps([])
        if _id in as_inputs:
            inputs = json.dumps(as_inputs[_id])
        else:
            inputs = json.dumps([])

        image=f"{REGISTRY}cognitive-processor:{VERSION}"
        logger.debug(f"{image=}")
        ASSETS['cp-containers'][_id] = docker_client.containers.run(name=_id + container_extension,
            image=f"{REGISTRY}cognitive-processor:{VERSION}",
            network=net_name,
            detach=True,
            init=True,
            hostname=_id,
            # publish_all_ports=True,
            restart_policy={"Name": "unless-stopped"},
            environment={'LOG_LEVEL': LOG_LEVEL,
                        'API_KEY': API_KEY,
                        'HOSTNAME': _id,
                        'MANIFEST': primitive_genes,
                        'SOURCES': sources,
                        'AS_INPUTS': inputs,
                        'TARGETS': targets}
                )
        # except (remote_exceptions.HTTPError, docker.errors.APIError):
        #     print("CONFLICT FOUND!")
        #     #  409 Client Error: Conflict for url:

    logger.debug("Starting GAIuS-API interface node...")

    port_connects={}

    port_offset=0
    port_base = 8000
    port_limit = 8200
    if(BIND_PORTS):
        port_list = []
        for each in docker_client.containers.list():
            for ports in each.ports.values():
                if(ports is not None):
                    for port in ports:
                        # print(port)
                        port_list.append(int(port['HostPort']))
        # print(str(port_list))
        while port_base + port_offset < port_limit:
            if port_base + port_offset not in port_list:
                if 44300 + port_offset not in port_list:
                    port_connects={'80/tcp': port_base+port_offset, '443/tcp': 44300+port_offset}
                    # print(port_connects)
                    break;
            else:
                port_offset += 1

        if port_base + port_offset == port_limit:
            logger.debug(f'failed to assign ports: reached port limit')
            sys.exit(-1)







    # f'''{8000+int(options.agent_id)}/tcp''': 80, f'''{44300+int(options.agent_id)}/tcp'''

    ASSETS['interfaces']['gaius-api' + container_extension] = docker_client.containers.run(name='gaius-api' + container_extension,
            image=f"{REGISTRY}gaius-api:{VERSION}",
            network=net_name,
            detach=True,
            init=True,
            # publish_all_ports=True,
            ports=port_connects,
            restart_policy={"Name": "unless-stopped"},
            environment={'LOG_LEVEL': LOG_LEVEL,
                         'API_KEY': API_KEY,
                         'HOSTNAME': BOTTLE_HOSTNAME,
                         'GENOME': genome_json,
                         'PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION': "cpp"}
            )

    # print summary
    logger.debug(f'''{fg.green}GAIuS Agent started on docker network {fg.blue}{str(net_name)}{fg.rs}''')
    if(BIND_PORTS):
        logger.debug(f'''{fg.green} Ports {fg.blue}{str(port_connects)}{fg.green} are exposed to the host{fg.rs}''')
    else:
        logger.debug(f'''{fg.green}Ports were not exposed for this agent. re-run command with {fg.blue}--bind-ports{fg.green} to expose ports{fg.rs}''')
    return net_name, port_connects


def stopContainer(id):
    try:
        docker_client = docker.from_env()
        logger.info(f'''stopping container {id}''')
        c = docker_client.containers.get(id)
        c.stop()
        c.remove()
        logger.info(f'''container {id} removed{fg.rs}''')
    except:
        logger.debug(f'''{fg.red}container {id} did not exist... continuing{fg.rs}''')



def stopit(genome_file, user_id=None, agent_id=None):

    if user_id is None:
        raise Exception('no user id provided')
    if agent_id is None:
        raise Exception('no agent_id provided')

    container_extension = '-' + user_id + '-' +  agent_id

    docker_client = docker.from_env()

    # read data into genome_json
    genome_json = genome_file

    # convert json to python dictionary
    try:
        with open(genome_file, 'r') as f:

            # read data into genome_json
            genome_json = f.read()
            _g = json.loads(genome_json)
            # convert json to python dictionary

    except Exception:
        logger.info(f'failed to load genome from file, trying from raw string')
        try:
            genome_json = genome_file
            _g = json.loads(genome_file)
        except json.decoder.JSONDecodeError:
            logger.warn(f'Failed to retreive genome from file or from raw string, exiting')
            sys.exit(-1)
    _g['description'] = 'cleared description'
    for d in _g['elements']['nodes']:
        if 'description' in d['data'].keys():
            logger.debug(f"Removing: {d['data']['description']}")
            d['data']['description'] = ''
    genome = Genome(_g)

    ids = list(genome.primitive_map.values()) + list(genome.manipulative_map.keys())
    ids.append('gaius-api')


    ids = ['{0}{1}'.format(id, container_extension) for id in ids]
    multiPool = multiprocessing.Pool()
    multiPool.map(stopContainer, ids)

    try:
        logger.debug("pruning docker system")
        docker_client.containers.prune()
        docker_client.networks.prune()
    except:
        logger.warn("unable to prune docker")
        sys.exit(-1)

    os.popen("yes | docker system prune")
    return

def execute_agent(BOTTLE_HOSTNAME   = None,
                  REGISTRY            = 'registry.digitalocean.com/intelligent-artifacts',
                  VERSION             = 'latest',
                  API_KEY             = None,
                  LOG_LEVEL           = 'DEBUG',
                  ENVIRONMENT         = None,
                  NETWORK             = None,
                  BIND_PORTS          = True,
                  GENOME              = None,
                  AGENT_ID            = None,
                  USER_ID             = None,
                  KILL                = False
                  ):

    if GENOME is None:
        raise Exception('No genome provided')

    if not os.path.exists(f"{os.path.expanduser('~')}/.gaius"):
        os.mkdir(f"{os.path.expanduser('~')}/.gaius")

    config = configparser.ConfigParser()
    user_dir = os.path.expanduser('~')

    if not ENVIRONMENT:
        logger.debug("environment not provided! Defaulting to 'local'.")
        env = 'local'
    else:
        env = ENVIRONMENT

    if not API_KEY:
        API_KEY = 'ABCD-1234'

    if not NETWORK:
        NETWORK = 'g2network'

    configuration = {
                    'BOTTLE_HOSTNAME': BOTTLE_HOSTNAME,
                    'REGISTRY': REGISTRY,
                    'VERSION': VERSION,
                    'API_KEY': API_KEY,
                    'LOG_LEVEL': LOG_LEVEL,
                    'NETWORK': NETWORK,
                    'BIND_PORTS': BIND_PORTS,
                    'user_id' : USER_ID,
                    'agent_id' : AGENT_ID,
                    }

    genome_file = GENOME

    if KILL:
        stopit(genome_file, user_id=USER_ID, agent_id=AGENT_ID)
        return -1

    network, ports = startit(genome_file, **configuration)
    
    return ports


def start_agent(json_obj):
    '''Start an agent from a genome passed as JSON

    fields => example:

        genome => json representation of genome
        user_id => alexlukens
        agent_id => agent1
        version => "latest"

    '''
    genome = json_obj['genome']
    user_id = json_obj['user_id']
    agent_id = json_obj['agent_id']
    kill = json_obj['kill']
    network = json_obj['network']

    version='latest'
    if 'version' in json_obj:
        version = json_obj['version']

    # check to see if agent with same name already running
    agent_name = 'gaius-api' + "-" + user_id + "-" + agent_id

    ports = execute_agent(REGISTRY='registry.digitalocean.com/intelligent-artifacts/',
                          BIND_PORTS=True,
                          AGENT_ID=agent_id,
                          USER_ID=user_id,
                          KILL=kill,
                          API_KEY='ABCD-1234',
                          GENOME=json.dumps(genome),
                          VERSION=version,
                          NETWORK=network)

    logger.debug(f'started agent with ports {ports}')

    if not kill:
        if ports == -1:
            raise Exception('Failed to start agent')

    agent_info =  {"name": '',
                   "domain": agent_name,
                   "api_key":"ABCD-1234",
                   "secure": False}
    # print(output)
    return agent_info, ports



def options():
    global options
    parser = OptionParser(version="%prog "+__version__, usage=doc)
    parser.add_option("-g", "--genome", dest="filename",
                        help="Genome file location", metavar="FILE")

    parser.add_option("--api-key", dest="API_KEY", default='ABCD-1234',
                        help="""Secret API key.
                        Default = 'ABCD-1234'
                                """)

    parser.add_option("--log-level", dest="LOG_LEVEL", default='DEBUG',
                        help="""Log level.
                        Default = DEBUG
                        Options:
                            CRITICAL
                            ERROR
                            WARNING
                            INFO
                            DEBUG
                                """)

    parser.add_option("-n", "--network", dest="NETWORK",
                        help="""Network in which all nodes will communicate.
                        Default = 'g2network'
                                """)
    parser.add_option("--bind-ports", action="store_true", dest="BIND_PORTS", default=False,
                        help="""To enable multiple agents running on single system, port are not bound by default.
                        Specify this option to explicitly bind agent to ports (required to run tests on agent).
                            HTTP port: 8000 + agent_id
                            HTTPS port: 44300 + agent_id
                            """)

    parser.add_option("-b", "--gaius-api-name", dest="BOTTLE", default='gaius-api',
                        help="""Bottle name
                        Default = 'BOTTLE'
                                """)

    parser.add_option("-H", "--hostname", dest="BOTTLE_HOSTNAME", default='localhost',
                        help="""Bottle name
                        Default = 'BOTTLE'
                                """)

    parser.add_option("-r", "--registry", dest="REGISTRY", default='registry.digitalocean.com/intelligent-artifacts/',
                        help="""Container registry
                        Default = 'registry.digitalocean.com/intelligent-artifacts/'

                        Set to '' if you want to use only local containers.
                                """)

    parser.add_option("--container-version", dest="VERSION", default='latest',
                        help="""Version of container images. Same used for all.
                        Default = 'latest'
                        """)

    parser.add_option("-e", "--environment", dest="ENVIRONMENT", default='local',
                        help="""Environment where we're running.
                        Uses config file located at ~/.gaius/setup.ini
                        No need to provide most of the other options when using this.
                        Options taken from the setup.ini file instead.

                        Default = 'local'

                        Ex. 'local' - for local agents using the 'latest' containers
                            'dev'  - to use development containers

                            More to come.
                        """)

    parser.add_option("-d", "--debug",
                        action="store_true", dest="debug", default=False,
                        help="print debug information")

    parser.add_option("--kill",
                        action="store_true", dest="kill", default=False,
                        help="Kill all agent's containers.")

    parser.add_option("--agent-id",
                        dest="agent_id", default="1",
                        help="""A string that uniquely identifies the agent and network. Appended to container and network names
                             Default=1""")
    (options, args) = parser.parse_args()

    if not options.filename:
        logger.warn("Need a genome file location! Pass with -g or --genome arg.")
        sys.exit(1)

    if len(options.REGISTRY) > 0 and not options.REGISTRY.endswith('/'):
        options.REGISTRY += '/'

class AgentInfo:
    def __init__(self, user_id: str, agent_id: str, agent_name: str, genome_name: str = None, genome_file: str = None, agent_config = None, location: str = 'local', LOG_LEVEL=logger.INFO):
        """Wrapper class for Agent information. Used to start/stop agents, and save config information to a central location

        Args:
            user_id (str): User id attached to docker contaienrs spawned using AgentInfo
            agent_id (str): Agent id attached to docker containers spawned using AgentInfo
            agent_name (str): Descriptive, user-friendly name to refer to agent by
            genome_name (str, optional): If genome already in centralized location, refer to it by its name
            genome_file (str, optional): To copy outside genome into genome store, provide filepath here
            agent_config (_type_, optional): Stores AgentConfig details once agent is spawned.
            location (str, optional): In future will support spawning at several locations (local, private cloud, DigitalOcean, etc). Defaults to 'local'.
            LOG_LEVEL (_type_, optional): Used to control verbosity of messages in agent spawn script. Defaults to logging.INFO.
        """
        logger.basicConfig(level=logger.INFO)
        self.data_dir = plat.user_data_dir(appname="IA_SDK_AgentManager", appauthor="IntelligentArtifacts")
        self.genome_dir = f'{self.data_dir}/genomes'
        self.agents_dir = f'{self.data_dir}/agents'
        
        if genome_name:
           self.genome_name =  genome_name
        else:
            self.genome_name = os.path.basename(genome_file)
            if os.path.exists(f'{self.genome_dir}/{self.genome_name}'):
                logger.warn(f'copying genome to genome dir would overwrite current genome {os.path.basename(genome_file)}, using genome already present')
            else:
                shutil.copyfile(src=genome_file, dst=f'{self.genome_dir}/{self.genome_name}')

        self.genome_file =  f'{self.genome_dir}/{self.genome_name}'
        self.user_id = user_id
        self.agent_id = agent_id
        self.location = location
        self.agent_name = agent_name
        self.agent_config = agent_config
        
    def check_running(self):
        """Check if we can access the agent

        Returns:
            bool: True for success, False for failure
        """
        if self.location == 'local':

            agent = AgentClient(bottle_info=self.agent_config)
            try:
                agent.connect()
            except Exception:
                return False

            return True

        else:
            raise Exception(f'unknown location {self.location}')
    
    def delete_config_file(self):
        """Kill agent and delete config information from agents directory
        """
        self.kill_agent()
        if os.path.exists(f'{self.agents_dir}/{self.agent_name}'):
            os.remove(f'{self.agents_dir}/{self.agent_name}')
        return f"deleted {self.agents_dir}/{self.agent_name}"
        
    def save_config_file(self):
        """Store config information for agent in agents directory, based on agent name
        """
        with open(f'{self.agents_dir}/{self.agent_name}', 'w') as f:
            json.dump(obj=self.toJSON(), fp=f)

        print(f'saved to {self.agents_dir}/{self.agent_name}')
        return '{self.agents_dir}/{self.agent_name}'
    
    def kill_agent(self):
        """Attempt to kill a running agent
        """
        stopit(self.genome_file, user_id=self.user_id, agent_id=self.agent_id)
    
    def start_agent(self):
        """Start a new agent using information provided in constructor
        """
        json_obj = self.toJSON()
        with open(self.genome_file, 'r') as f:
            json_obj['genome'] = json.load(f)
        json_obj['kill'] = False
        json_obj['network'] = None
        self.agent_config, ports = start_agent(json_obj=json_obj)
        print(f'updating config file with new agent config: {self.agent_config}')
        self.save_config_file()
    
    def get_docker_networks(self):
        """Get names of networks this agent is a part of (uses gaius-api-{user_id}-{agent_id})

        Raises:
            Exception: More that one container found with same name

        Returns:
            _type_: list of networks
        """
        docker_client = docker.from_env()
        gapi_container = docker_client.containers.list(filters={'name':f'gaius-api-{self.user_id}-{self.agent_id}'})
        if len(gapi_container) == 1:
            gapi_container = gapi_container[0]
            return list(gapi_container.attrs['NetworkSettings']['Networks'].keys())
        elif len(gapi_container) > 1:
            self.delete_config_file()
            raise Exception('too many docker containers with same GAIuS API name')
        else:
            raise Exception('gaius-api container not found, start agent first')
        
    
    def connect_jia(self):
        """Connect agent to jia (add jia to the agent's network)
        """
        docker_client = docker.from_env()
        jias = docker_client.containers.list(filters={'ancestor':'registry.digitalocean.com/intelligent-artifacts/jia:0.1.15'})
        nets = self.get_docker_networks()
        nets = docker_client.networks.list(names=nets)
        if len(jias) == 0:
            print("No JIA notebooks found! Skipping...")
        elif len(jias) == 1:
            print(f'connecting single jia')
            jia = docker_client.containers.get(jias[0].short_id) #.attrs['Config']['Name']
            for net in nets:
                net.reload()
                if jia.id in [cont.id for cont in net.containers]:
                    print(f'jia already connected to network {net.name}')
                    continue
                net.connect(jia)
                print(f"Connecting JIA id: {jia.name} on {net.name}")
        elif len(jias) > 1:
            def connect_jia_func():
                print("More than one JIA found. Please select which to connect:")
                for c, i in enumerate(jias):
                    x = int(input(f"    {i}: {c} {c.name} connect? Y/N - "))
                    if x.lowercase() == 'y':
                        for net in nets:
                            net.reload()
                            if c.id in [cont.id for cont in net.containers]:
                                print(f'jia already connected to network {net.name}')
                                continue
                            net.connect(cjia)
                            print(f"Connecting JIA id: {c.name} on {net.name}")
                    else:
                        print("Invalid entry. Try again...")
    
    def get_agent_client(self):
        """Retreive AgentClient object from started agent

        Returns:
            ia.gaius.agent_client.AgentClient
        """
        if self.agent_config == None:
            raise Exception('agent_config information empty, must start agent first')
        return AgentClient(bottle_info=self.agent_config)
    
    def toJSON(self):
        """Dump config information to a JSON object (dict)

        Returns:
            dict: config information
        """
        return {'genome_name': self.genome_name,
                'genome_file': self.genome_file,
                'agent_id': self.agent_id,
                'user_id': self.user_id,
                'agent_name': self.agent_name,
                'location': self.location,
                'agent_config': self.agent_config
                }
    
    @classmethod
    def fromFile(cls, filepath: str):
        """Construct AgentInfo object from file

        Args:
            filepath (str): path to file to load

        Returns:
            AgentInfo: AgentInfo object created from the file
        """
        with open(filepath, 'r') as f:
            json_obj = json.load(f)
        
        return cls.fromJSON(json_obj=json_obj)
    
    @classmethod
    def fromJSON(cls, json_obj):
        """Construct AgentInfo from JSON object

        Args:
            json_obj (dict): Contains fields necessary for constructing AgentInfo

        Returns:
            AgentInfo: AgentInfo object created from JSON object
        """
        return cls(**json_obj)


class AgentManager:
    def __init__(self):
        """Initialize AgentManager object (setup dirs, etc.)
        
        This object can be used to spawn Agents using the start_agent() method.
        """
        self.data_dir = plat.user_data_dir(appname="IA_SDK_AgentManager", appauthor="IntelligentArtifacts")
        self.genome_dir = f'{self.data_dir}/genomes'
        self.agents_dir = f'{self.data_dir}/agents'
        self.config_file = f'{self.data_dir}/config.json'
        
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        print(f'user data location: {self.data_dir}')
        
        if not os.path.exists(self.genome_dir):
            os.mkdir(self.genome_dir)
            
        if not os.path.exists(self.agents_dir):
            os.mkdir(self.agents_dir)
        
        self.update_current_agents()
        
    def start_agent(self, genome_file=None, genome_name=None, user_id: str = 'jia', agent_id: str = '1', agent_name: str = f'agent-{uuid.uuid4().hex[:8]}'):
        self.update_current_agents()
        for agent_name, agent in self.current_agents.items():
            if agent.agent_id == agent_id and agent.user_id == user_id:
                raise Exception(f'Agent({agent_name}) with user_id {user_id} and agent_id {agent_id} already exists, please choose other ids')
        
        agent = AgentInfo(agent_id=agent_id, user_id=user_id, genome_file=genome_file, genome_name=genome_name, agent_name=agent_name)
        agent.start_agent()
        self.update_current_agents()
        print(f'started agent {agent.agent_name}')
        return agent
    
    def get_all_agent_status(self):
        agent_status = {}
        for agent_name, agent in self.current_agents.items():
            agent_status[agent_name] = agent.check_running()

        return agent_status
        
    def delete_agent(self, agent_name):
        result = self.current_agents[agent_name].delete_config_file()
        del self.current_agents[agent_name]
        self.update_current_agents()
        return result
    
    def list_genomes(self):
        return os.listdir(self.genome_dir)
    
    def delete_genome(self, genome_name):
        genome_path = os.path.join(self.genome_dir, genome_name)
        print(f'will remove genome {genome_path}')
        os.remove(genome_path)
        return
    
    def get_genome(self, genome_name):
        genome_path = os.path.join(self.genome_dir, genome_name)
        
        if genome_name not in self.list_genomes():
            raise Exception(f'{genome_name} not in genome dir: {self.list_genomes()}')
        with open(genome_path, 'r') as f:
            return json.load(f)
        
    
    def update_current_agents(self):
        # retrieve all agent files
        self.current_agents = os.listdir(self.agents_dir)
        
        # get full paths of agent files
        self.current_agents = [os.path.join(self.agents_dir, agent) for agent in self.current_agents]
        
        # instantiate AgentInfo classes
        self.current_agents = [AgentInfo.fromFile(agent) for agent in self.current_agents]
        
        # make current agents into a dict by agent_name
        self.current_agents = {agent.agent_name : agent for agent in self.current_agents}
        
    def remediate_dead_agents(self):
        
        agent_status = self.get_all_agent_status()
        
        killed_agents = []
        for agent_name, alive in agent_status.items():
            if not alive:
                print(f'{agent_name} is not alive, cleaning up')
                self.delete_agent(agent_name)
                killed_agents.append(agent_name)
        
        print(f'{killed_agents=}')


if __name__ == '__main__':
    if not os.path.exists(f"{os.path.expanduser('~')}/.gaius"):
        os.mkdir(f"{os.path.expanduser('~')}/.gaius")
    options()

    config = configparser.ConfigParser()
    user_dir = os.path.expanduser('~')
    if not os.path.exists(f"{user_dir}/.gaius/setup.ini"):
        print("No setup.ini found! Switching to default values if args not provided. See --help for info.")
        ## Default values provided by OptionParser
        BOTTLE_HOSTNAME = options.BOTTLE_HOSTNAME
        REGISTRY = options.REGISTRY
        VERSION = options.VERSION
        API_KEY = options.API_KEY
        LOG_LEVEL = options.LOG_LEVEL
        NETWORK = options.NETWORK
        BIND_PORTS = options.BIND_PORTS
        

    else:
        if not options.ENVIRONMENT:
            print("environment not provided! Defaulting to 'local'.")
            env = 'local'
        else:
            env = options.ENVIRONMENT
        config.read(f"{user_dir}/.gaius/setup.ini")
        if options.BOTTLE_HOSTNAME:
            BOTTLE_HOSTNAME = options.BOTTLE_HOSTNAME
        else:
            BOTTLE_HOSTNAME = config.get(env, "BOTTLE_HOSTNAME")

        # if options.REGISTRY:
        REGISTRY = options.REGISTRY
        # else:
        #     REGISTRY = config.get(env, "REGISTRY")

        # if options.VERSION:
        VERSION = options.VERSION
        # else:
        #     VERSION = config.get(env, "VERSION")
        BIND_PORTS = options.BIND_PORTS

        if options.API_KEY:
            API_KEY = options.API_KEY
        else:
            API_KEY = config.get(env, "API_KEY")

        if options.LOG_LEVEL:
            LOG_LEVEL = options.LOG_LEVEL
        else:
            LOG_LEVEL = config.get(env, "LOG_LEVEL")

        if options.NETWORK:
            NETWORK = options.NETWORK
        else:
            try:
                NETWORK = config.get(env, "NETWORK")
            except configparser.NoOptionError:
                NETWORK = 'g2network'

    USER_ID = os.environ["USER"]
    AGENT_ID = options.agent_id
    configuration = {
                    'BOTTLE_HOSTNAME': BOTTLE_HOSTNAME,
                    'REGISTRY': REGISTRY,
                    'VERSION': VERSION,
                    'API_KEY': API_KEY,
                    'LOG_LEVEL': LOG_LEVEL,
                    'NETWORK': NETWORK,
                    'BIND_PORTS': BIND_PORTS,
                    'user_id' : USER_ID,
                    'agent_id' : AGENT_ID,
                    }

    genome_file = options.filename
    docker_client = docker.from_env()
    if options.kill:
        stopit(genome_file, user_id=USER_ID, agent_id=AGENT_ID)
        sys.exit()

    network = startit(genome_file, **configuration)