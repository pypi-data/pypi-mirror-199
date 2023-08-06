from pysura.pysura_types.root_cmd import RootCmd
from pysura.pysura_types.google_pysura_env import *
import json
import os
from pydantic.error_wrappers import ValidationError
import logging
import random
from string import ascii_letters, digits


class GoogleRoot(RootCmd):

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.intro = "Welcome to Pysura for Google Architectures! Type help or ? to list commands."
        self.prompt = "(pysura_cli) >>> "

    @staticmethod
    def password(length: int = 64):
        return "".join(random.choices(ascii_letters + digits, k=length))

    @staticmethod
    def get_env(file_name: str = "env.json") -> GooglePysuraEnv:
        try:
            with open(file_name, "r") as f:
                return GooglePysuraEnv(**json.load(f))
        except FileNotFoundError:
            env = GooglePysuraEnv()
            with open(file_name, "w") as f:
                json.dump(env.dict(), f)
            return env

    @staticmethod
    def set_env(value: GooglePysuraEnv, file_name: str = "env.json"):
        with open(file_name, "w") as f:
            json.dump(value.dict(), f)

    def gcloud_list_typed_choice(self, command_str, prompt_str, default="name"):
        self.log(command_str, logging.DEBUG)
        response = os.popen(command_str).read()
        gcloud_list = json.loads(response)
        try:
            choice_list = [i[default] for i in gcloud_list]
        except KeyError:
            self.log(f"Invalid default: {default}")
            return
        try:
            if len(gcloud_list) > 0:
                choice = self.collect(prompt_str, choice_list)
                if choice not in choice_list:
                    self.log("Invalid choice.")
                    return
                return choice
            else:
                self.log("No items found.")
        except Exception as e:
            self.log(str(e), logging.ERROR)

    @staticmethod
    def get_env_names(cls):
        cls_name = cls.schema()["title"]
        attr_names = {
            "selected": None,
            "list": None
        }
        env_properties = GoogleRoot.get_env().schema()["properties"]
        for k, v in env_properties.items():
            if isinstance(v, dict) and cls_name == v.get("$ref", "").split("/")[-1]:
                attr_names["selected"] = k
            elif isinstance(v, dict) and "items" in v:
                if cls_name == v["items"].get("$ref", "").split("/")[-1]:
                    attr_names["list"] = k
        return attr_names

    def gcloud_list_choice(self, command_str, model):
        env_names = self.get_env_names(model)
        self.log(command_str, logging.DEBUG)
        if "--format" not in command_str:
            command_str += " --format=json"
        response = os.popen(command_str).read()
        gcloud_list = json.loads(response)
        choice = None
        if choice is None:
            for i, gcloud_dict in enumerate(gcloud_list):
                self.log(f"\n{i}\t{gcloud_dict.get('name', None)}:\n{json.dumps(gcloud_dict, indent=4)}")
            choice = self.collect("Select a number from the list above: ").strip()
            choice = int(choice)
        if choice is not None:
            env_item = gcloud_list[choice]
            try:
                env_item = model(**env_item)
            except ValidationError:
                self.log("The selected item has inconsistent metadata.")
                return self.gcloud_list_choice(command_str, model)
            env = self.get_env()
            env[env_names["selected"]] = env_item
            self.set_env(env)
            return env_item, gcloud_list

    def do_exit(self, _):
        """
        Exits the application.
        Usage: exit
        """
        self.log("Exiting...")
        exit(0)

    def do_quit(self, _):
        """
        Exits the application.
        Usage: quit
        """
        self.log("Exiting...")
        exit(0)

    def do_gcloud_login(self, check_logged_in=False):
        """
        Logs into gcloud.
        Usage: gcloud_login
        """
        if isinstance(check_logged_in, str):
            check_logged_in = False
        if check_logged_in:
            env = self.get_env()
            self.log("Checking if already logged into gcloud...")
            if env.gcloud_logged_in:
                self.log("Already logged into gcloud!")
                return
        self.log("Logging into gcloud...")
        cmd_str = "gcloud auth login"
        self.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        login_success = self.collect("Did you successfully login? (y/n)")
        if login_success.strip().lower() == "y":
            env = self.get_env()
            env.gcloud_logged_in = True
            self.set_env(env)
        else:
            self.user_input_no_loop(self.do_gcloud_login)

    def do_gcloud_link_billing_account(self, project_id=None):
        """
        Links a billing account to a project.
        Usage: gcloud_link_billing_account
        """
        env = self.get_env()
        if env.project is None:
            self.log("No project selected.")
            return
        if project_id is None or (isinstance(project_id, str) and len(project_id.strip()) == 0):
            project_id = env.project.name.split("/")[-1]
        billing_account, billing_accounts = self.gcloud_list_choice(
            "gcloud beta billing accounts list --format=json",
            GoogleBillingAccount)
        env.billing_account = billing_account
        env.billing_accounts = billing_accounts
        self.set_env(env)
        cmd_str = f"gcloud beta billing projects link {project_id} " \
                  f"--billing-account={billing_account.name.split('/')[-1]}"
        self.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)

    def do_gcloud_enable_services(self, _):
        env = self.get_env()
        if env.project is None:
            self.log("No project selected.")
            return
        self.log("Enabling services...")
        project_id = env.project.name.split("/")[-1]
        cmd_str = f"gcloud services enable servicenetworking.googleapis.com --project={project_id}"
        self.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable compute.googleapis.com --project={project_id}"
        self.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable sqladmin.googleapis.com --project={project_id}"
        self.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable vpcaccess.googleapis.com --project={project_id}"
        self.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable identitytoolkit.googleapis.com --project={project_id}"
        self.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable run.googleapis.com --project={project_id}"
        self.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable secretmanager.googleapis.com --project={project_id}"
        self.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services list --project={project_id} --format=json"
        self.log(cmd_str, level=logging.DEBUG)
        response = os.popen(cmd_str).read()
        services = json.loads(response)
        env.services = services
        self.set_env(env)

    def do_gcloud_choose_organization(self, _):
        """
        Chooses an organization.
        Usage: gcloud_choose_organization
        """
        self.log("Choosing organization...")
        org, orgs = self.gcloud_list_choice("gcloud organizations list --format=json", GoogleOrganization)
        env = self.get_env()
        env.organization = org
        env.organizations = orgs
        self.set_env(env)

    def do_gcloud_create_project(self, project_id=""):
        """
        Creates a gcloud project.
        Usage: gcloud_project_create
        """
        env = self.get_env()
        use_organization = self.collect("Do you want to use an organization? (y/n)")
        use_org = use_organization.strip().lower() == "y"
        if use_org:
            if env.organization is None:
                self.log("No organization selected.")
                return
        arg_len = len(project_id.strip())
        if arg_len == 0:
            project_name = self.collect("Enter a project name: ")
        else:
            project_name = project_id
        if arg_len > 0 or self.confirm_loop(project_name):
            cmd_str = f"gcloud projects create {project_name}"
            if use_org:
                assert env.organization is not None
                cmd_str += f" --organization={env.organization.name.split('/')[-1]}"
            self.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = f"gcloud projects list --format=json"
            self.log(cmd_str, level=logging.DEBUG)
            response = os.popen(cmd_str).read()
            projects = json.loads(response)
            project = None
            for p in projects:
                project_data = GoogleProject(**p)
                if project_data.name.split("/")[-1] == project_name:
                    project = GoogleProject(**p)
                    break
            assert project is not None
            cmd_str = f"gcloud config set project {project.name.split('/')[-1]}"
            self.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            env.project = project
            env.projects = projects
            self.set_env(env)
        else:
            self.user_input_no_loop(self.do_gcloud_create_project)

    def do_gcloud_choose_project(self, _):
        """
        Chooses a project.
        Usage: gcloud_choose_project
        """
        env = self.get_env()
        if not env.gcloud_logged_in:
            self.do_gcloud_login()
        self.log("Choosing project...")
        project, projects = self.gcloud_list_choice("gcloud projects list --format=json", GoogleProject)
        env.project = project
        env.projects = projects
        self.set_env(env)
        if project is not None:
            cmd_str = f"gcloud config set project {project.name.split('/')[-1]}"
            self.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)

    def do_gcloud_create_network(self, network_id=""):
        """
        Creates a Network.
        Usage: gcloud_network_create
        """
        env = self.get_env()
        if env.project is None:
            self.log("No project selected.")
            return
        arg_len = len(network_id.strip())
        if arg_len == 0:
            network_name = self.collect("Enter a network name: ")
        else:
            network_name = network_id
        if arg_len > 0 or self.confirm_loop(network_name):
            cmd_str = f"gcloud compute networks create {network_name}" \
                      f" --subnet-mode=auto" \
                      f" --project={env.project.name.split('/')[-1]}"
            self.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = f"gcloud compute networks list " \
                      f"--project={env.project.name.split('/')[-1]} " \
                      f"--format=json"
            gcloud_list = self.retry_loop(cmd_str, network_name)
            network_selected = None
            network_set = []
            for gcloud_item in gcloud_list:
                network = GoogleNetwork(
                    **gcloud_item
                )
                network_set.append(network)
                if network.name.split("/")[-1] == network_name:
                    network_selected = network

            if network_selected is None:
                self.log("Network not found.")
                return
            env.network = network_selected
            env.networks = network_set
            self.set_env(env)
        else:
            self.user_input_no_loop(self.do_gcloud_create_network)

    def do_gcloud_choose_network(self, _):
        """
        Chooses a Network.
        Usage: gcloud_network_choose
        """
        env = self.get_env()
        if env.project is None:
            self.log("No project selected.")
            return
        self.log("Choosing network...")
        network, networks = self.gcloud_list_choice(f"gcloud compute networks list "
                                                    f"--project={env.project.name.split('/')[-1]} "
                                                    f"--format=json", GoogleNetwork)
        env.network = network
        env.networks = networks
        self.set_env(env)

    def do_gcloud_create_address(self, address_id=""):
        """
        Creates an address.
        Usage: gcloud_address_create
        """
        env = self.get_env()
        if env.project is None:
            self.log("No project selected.")
            return
        if env.network is None:
            self.log("No network selected.")
            return
        arg_len = len(address_id.strip())
        if arg_len == 0:
            address_name = self.collect("Enter an address name: ")
        else:
            address_name = address_id
        if arg_len > 0 or self.confirm_loop(address_name):
            cmd_str = f"gcloud compute addresses create {address_name} " \
                      f"--global " \
                      f"--purpose=VPC_PEERING " \
                      f"--prefix-length=16 " \
                      f"--network={env.network.name.split('/')[-1]} " \
                      f"--project={env.project.name.split('/')[-1]}"
            self.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = f"gcloud compute addresses list " \
                      f"--project={env.project.name.split('/')[-1]} " \
                      f"--format=json"
            gcloud_list = self.retry_loop(cmd_str, address_name)
            address_selected = None
            address_set = []
            for gcloud_item in gcloud_list:
                address = GoogleAddress(
                    **gcloud_item
                )
                address_set.append(address)
                if address.name.split('/')[-1] == address_name:
                    address_selected = address
            if address_selected is None:
                self.log("Address not found.")
                return
            env.address = address_selected
            env.addresses = address_set
            self.set_env(env)
            if address_selected is None:
                self.log("Address not found.")
                return
        else:
            self.user_input_no_loop(self.do_gcloud_create_address)

    def do_gcloud_choose_address(self, _):
        """
        Chooses an address.
        Usage: gcloud_address_choose
        """
        env = self.get_env()
        if env.project is None:
            self.log("No project selected.")
            return
        if env.network is None:
            self.log("No network selected.")
            return
        self.log("Choosing address...")
        address, addresses = self.gcloud_list_choice(f"gcloud compute addresses list "
                                                     f"--project={env.project.name.split('/')[-1]} "
                                                     f"--format=json", GoogleAddress)
        env.address = address
        env.addresses = addresses
        self.set_env(env)

    def do_gcloud_create_vpc_peering(self, peering_id=""):
        """
        Creates a VPC Peering.
        Usage: gcloud_vpc_peering_create
        """
        env = self.get_env()
        if env.project is None:
            self.log("No project selected.")
            return
        if env.network is None:
            self.log("No network selected.")
            return
        if env.address is None:
            self.log("No address selected.")
            return

        arg_len = len(peering_id.strip())
        if arg_len == 0:
            peering_name = self.collect("Enter a peering name: ")
        else:
            peering_name = peering_id
        if arg_len > 0 or self.confirm_loop(peering_name):
            cmd_str = f"gcloud services vpc-peerings connect " \
                      f"--service=servicenetworking.googleapis.com " \
                      f"--ranges={env.address.name.split('/')[-1]} " \
                      f"--network={env.network.name.split('/')[-1]} " \
                      f"--project={env.project.name.split('/')[-1]}"
            self.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = f"gcloud services vpc-peerings list " \
                      f"--project={env.project.name.split('/')[-1]} " \
                      f"--network={env.network.name.split('/')[-1]} --format=json"
            gcloud_list = self.retry_loop(cmd_str, peering_name)
            peering_selected = None
            peering_set = []
            for peering in gcloud_list:
                peering_data = GoogleVpcPeering(
                    **peering
                )
                peering_set.append(peering_data)
                if peering_name in peering_data.reservedPeeringRanges:
                    peering_selected = peering_data
            if peering_selected is None:
                self.log("Peering not found.")
                return
            env.peering = peering_selected
            env.peerings = peering_set
            self.set_env(env)
        else:
            self.user_input_no_loop(self.do_gcloud_create_vpc_peering)

    def do_gcloud_choose_vpc_peering(self, _):
        """
        Chooses a VPC Peering.
        Usage: gcloud_vpc_peering_choose
        """
        env = self.get_env()
        if env.project is None:
            self.log("No project selected.")
            return
        if env.network is None:
            self.log("No network selected.")
            return
        if env.address is None:
            self.log("No address selected.")
            return
        self.log("Choosing peering...")
        peering, peerings = self.gcloud_list_choice(
            f"gcloud services vpc-peerings list "
            f"--project={env.project.name.split('/')[-1]} "
            f"--network={env.network.name.split('/')[-1]} --format=json",
            GoogleVpcPeering
        )
        env.peering = peering
        env.peerings = peerings
        self.set_env(env)

    def do_gcloud_create_firewall(self, firewall_id=""):
        """
        Creates a firewall.
        Usage: gcloud_firewall_create
        """
        env = self.get_env()
        if env.project is None:
            self.log("No project selected.")
            return
        if env.network is None:
            self.log("No network selected.")
            return
        if env.address is None:
            self.log("No address selected.")
            return
        if env.peering is None:
            self.log("No peering selected.")
            return

        arg_len = len(firewall_id.strip())
        if arg_len == 0:
            firewall_name = self.collect("Enter a firewall name: ")
        else:
            firewall_name = firewall_id
        if arg_len > 0 or self.confirm_loop(firewall_name):
            cmd_str = f"gcloud compute firewall-rules create {firewall_name}-allow-traffic  " \
                      f"--network={env.network.name.split('/')[-1]} " \
                      f"--allow=tcp,udp,icmp " \
                      f"--source-ranges=0.0.0.0/0 " \
                      f"--project={env.project.name.split('/')[-1]}"
            self.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = f"gcloud compute firewall-rules list " \
                      f"--project={env.project.name.split('/')[-1]} " \
                      f"--format=json"
            self.retry_loop(cmd_str, f"{firewall_name}-allow-traffic")
            cmd_str = f"gcloud compute firewall-rules create {firewall_name}-allow-internal  " \
                      f"--network={env.network.name.split('/')[-1]} " \
                      f"--allow=tcp:22,tcp:3389,icmp " \
                      f"--project={env.project.name.split('/')[-1]}"
            self.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = f"gcloud compute firewall-rules list " \
                      f"--project={env.project.name.split('/')[-1]} " \
                      f"--format=json"
            self.log(cmd_str, level=logging.DEBUG)
            gcloud_list = json.loads(os.popen(cmd_str).read())
            firewall_set = []
            for firewall in gcloud_list:
                firewall_data = GoogleFirewall(
                    **firewall
                )
                firewall_set.append(firewall_data)
            env.firewalls = firewall_set
            self.set_env(env)
        else:
            self.user_input_no_loop(self.do_gcloud_create_firewall)

    def do_gcloud_create_database(self, database_id=""):
        env = self.get_env()
        if env.project is None:
            self.log("No project selected.")
            return
        if env.network is None:
            self.log("No network selected.")
            return

        arg_len = len(database_id.strip())
        if arg_len == 0:
            db_name = self.collect("Enter a database name: ")
        else:
            db_name = database_id
        if arg_len == 0 and not self.confirm_loop(db_name):
            self.user_input_no_loop(self.do_gcloud_create_database)
            return
        cpu_number = self.collect("Enter the number of CPU's for the database number: ")
        memory_amount = self.collect("Enter the amount of memory for the database (MiB): ", ["2048",
                                                                                             "4096",
                                                                                             "8192",
                                                                                             "16384",
                                                                                             "24576",
                                                                                             "32768"])
        db_version = self.collect("Enter the database version (Supports POSTGRES_14, ):", ["POSTGRES_14"])
        cpu_number = str(int(cpu_number.strip()))
        memory_amount = f"{str(int(memory_amount.strip()))}MiB"
        zone = self.gcloud_list_typed_choice(f"gcloud compute zones list "
                                             f"--project={env.project.name.split('/')[-1]} "
                                             f"--format=json", "Enter a zone: ", "name")
        if zone is None:
            self.log("No zone selected.")
            return
        availability_types = ["regional", "zonal"]
        availability_type = self.collect("Enter the availability type: (regional/zonal)", availability_types)
        if availability_type not in availability_types:
            self.log("Invalid availability type.")
            return
        db_password = self.password()
        self.log(f"You are preparing to create a database with the following parameters: "
                 f"Name: {db_name}, CPU's: {cpu_number}, Memory: {memory_amount}, "
                 f"Version: {db_version}, Zone: {zone}, "
                 f"Network: {env.network.name.split('/')[-1]}, Project: {env.project.name.split('/')[-1]}, "
                 f"DatabasePassword: {db_password}")
        continue_flag = self.collect("Continue? (y/n): ", ["y", "n"])
        if continue_flag.strip().lower() != "y":
            self.log("Aborting...")
            return
        cmd_str = (
            f"gcloud beta sql instances create {db_name} "
            f"--project={env.project.name.split('/')[-1]} "
            f"--network=projects/{env.project.name.split('/')[-1]}/global/networks/{env.network.name.split('/')[-1]} "
            f"--root-password={db_password} "
            f"--zone={zone} "
            f"--cpu={cpu_number} "
            f"--memory={memory_amount} "
            f"--database-version={db_version} "
            f"--availability-type={availability_type} "
            f"--enable-google-private-path"
        )
        self.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        db = GoogleDatabase()
        cmd_str = f"gcloud sql instances list " \
                  f"--project={env.project.name.split('/')[-1]} " \
                  f"--format=json"
        gcloud_list = self.retry_loop(cmd_str, f"{db_name}")
        db_selected = None
        db_set = []
        for db_instance in gcloud_list:
            db_data = GoogleDatabase(
                **db_instance
            )
            db_set.append(db_data)
            if db_data.name.split('/')[-1] == db_name:
                db_selected = db_data

        if db_selected is None:
            self.log("Database not found.")
            return

        db_creds = DatabaseCredential()
        db_creds.database_id = db_name
        db_creds.password = db_password
        private_address = None
        for addr in db_selected.ipAddresses:
            if addr.type == "PRIVATE":
                private_address = addr.ipAddress
        if private_address is not None:
            db_creds.connect_url = f"postgres://" \
                                   f"postgres:{db_password}" \
                                   f"@/postgres?host=" \
                                   f"{private_address}"
        env.database = db_selected
        env.databases = db_set
        env.database_credential = db_creds
        self.set_env(env)

    def do_gcloud_create_serverless_connector(self, connector_id=""):
        """
        Creates a serverless connector.
        Usage: create_serverless_connector
        """
        env = self.get_env()
        if env.project is None:
            self.log("No project selected.")
            return
        if env.network is None:
            self.log("No network selected.")
            return
        if env.database is None:
            self.log("No database selected.")
            return

        range_choice = self.collect("Select a range: ", [f"10.{i}.0.0/28" for i in range(8, 100)])
        arg_len = len(connector_id.split())
        if arg_len == 0:
            connector_name = self.collect("Enter a connector name: ")
        else:
            connector_name = connector_id
        if arg_len == 0 and not self.confirm_loop(connector_name):
            self.user_input_no_loop(self.do_gcloud_create_serverless_connector)
            return
        cmd_str = f"gcloud compute networks vpc-access connectors create {connector_name} " \
                  f"--network={env.network.name.split('/')[-1]} " \
                  f"--region={env.database.region} " \
                  f"--range={range_choice} " \
                  f"--project={env.project.name.split('/')[-1]}"
        self.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud compute networks vpc-access connectors list " \
                  f"--project={env.project.name.split('/')[-1]} " \
                  f"--region={env.database.region} --format=json"
        gcloud_list = self.retry_loop(cmd_str, f"{connector_name}")
        connector_selected = None
        connector_set = []
        for connector in gcloud_list:
            connector_data = GoogleConnector(
                **connector
            )
            connector_set.append(connector_data)
            if connector_data.name.split("/")[-1] == connector_name:
                connector_selected = connector_data

        if connector_selected is None:
            self.log("Connector not found.")
            return
        env.connector = connector_selected
        env.connectors = connector_set
        self.set_env(env)

    def do_gcloud_choose_serverless_connector(self, _):
        """
        Chooses a serverless connector.
        Usage: choose_serverless_connector
        """
        env = self.get_env()
        if env.project is None:
            self.log("No project selected.")
            return
        if env.network is None:
            self.log("No network selected.")
            return
        if env.database is None:
            self.log("No database selected.")
            return

        cmd_str = f"gcloud compute networks vpc-access connectors list " \
                  f"--region={env.database.region} " \
                  f"--project={env.project.name.split('/')[-1]} --format=json"
        self.log(cmd_str, level=logging.DEBUG)
        response = os.popen(cmd_str).read()
        gcloud_list = json.loads(response)
        connector_selected = None
        connector_set = []
        for connector in gcloud_list:
            connector_data = GoogleConnector(
                **connector
            )
            connector_set.append(connector_data)
            if connector_data.name.split("/")[-1] == env.connector.name.split('/')[-1]:
                connector_selected = connector_data

        if connector_selected is None:
            self.log("Connector not found.")
            return

        env.connector = connector_selected
        env.connectors = connector_set
        self.set_env(env)

    def do_gcloud_deploy_hasura(self, _):
        env = self.get_env()
        if env.project is None:
            self.log("No project selected.")
            return
        if env.connector is None:
            self.log("No connector selected.")
            return
        if env.hasura is None:
            account_choices = json.loads(os.popen(f"gcloud iam service-accounts list "
                                                  f"--project={env.project.name.split('/')[-1]} "
                                                  f"--format=json").read())
            account_id = None
            for i, account in enumerate(account_choices):
                if "Compute Engine default service account" in account["displayName"]:
                    account_id = account["email"]
                    break
            if account_id is None:
                self.log("No service account found.")
                return
            cmd_log_str = (f"gcloud projects add-iam-policy-binding {env.project.name.split('/')[-1]} "
                           f"--member=serviceAccount:{account_id} "
                           f"--role=roles/cloudbuild.builds.builder"
                           )
            self.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            cmd_log_str = (f"gcloud projects add-iam-policy-binding {env.project.name.split('/')[-1]} "
                           f"--member=serviceAccount:{account_id} "
                           f"--role=roles/run.admin"
                           )
            self.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            cmd_log_str = "docker pull --platform=linux/amd64 hasura/graphql-engine:latest"
            self.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            cmd_log_str = f"docker tag hasura/graphql-engine:latest " \
                          f"gcr.io/{env.project.name.split('/')[-1]}/hasura:latest"
            self.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            cmd_log_str = f"docker push gcr.io/{env.project.name.split('/')[-1]}/hasura:latest"
            self.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            hasura_secret = self.password()
            timeout = self.collect("Timeout (seconds)", ["60s", "300s", "600s", "900s", "1200s", "3600s"])
            cpu = self.collect("CPU (cores)", ["1", "2", "4", "8", "16", "32", "64"])
            memory = self.collect("Memory", ["256Mi", "512Mi", "1Gi", "2Gi", "4Gi", "8Gi", "16Gi", "32Gi"])
            max_instances = self.collect("Max instances: ")
            hasura = Hasura(
                HASURA_GRAPHQL_CORS_DOMAIN="*",
                HASURA_GRAPHQL_ENABLED_CORS="true",
                HASURA_GRAPHQL_ENABLE_CONSOLE="true",
                HASURA_GRAPHQL_ADMIN_SECRET=hasura_secret,
                HASURA_GRAPHQL_DATABASE_URL=env.database_credential.connect_url,
                HASURA_GRAPHQL_METADATA_DATABASE_URL=env.database_credential.connect_url,
                vpc_connector=env.connector.name.split('/')[-1],
                timeout=timeout,
                project_id=env.project.name.split('/')[-1],
                cpu=cpu,
                memory=memory,
                min_instances="1",
                max_instances=max_instances
            )
            env.hasura = hasura
            self.set_env(env)
        hasura = env.hasura
        with open("env.yaml", "w") as f:
            f.write(f"""HASURA_GRAPHQL_DATABASE_URL: '{hasura.HASURA_GRAPHQL_DATABASE_URL}'
HASURA_GRAPHQL_ADMIN_SECRET: '{hasura.HASURA_GRAPHQL_ADMIN_SECRET}
HASURA_GRAPHQL_METADATA_DATABASE_URL: '{hasura.HASURA_GRAPHQL_METADATA_DATABASE_URL}'
HASURA_GRAPHQL_ENABLED_CORS: '{hasura.HASURA_GRAPHQL_ENABLED_CORS}'
HASURA_GRAPHQL_ENABLE_CONSOLE: '{hasura.HASURA_GRAPHQL_ENABLE_CONSOLE}'
HASURA_GRAPHQL_CORS_DOMAIN: '{hasura.HASURA_GRAPHQL_CORS_DOMAIN}'
""")
        deploy_command = (f"gcloud run deploy hasura "
                          f"--image=gcr.io/{env.project.name.split('/')[-1]}/hasura:latest "
                          f"--env-vars-file=env.yaml "
                          f"--min-instances=1 "
                          f"--max-instances=10 "
                          f"--cpu=1 "
                          f"--memory=2048Mi "
                          f"--vpc-connector={env.connector.name.split('/')[-1]} "
                          f"--port=8080 "
                          f"--command='graphql-engine' "
                          f"--args='serve' "
                          f"--timeout=600s "
                          f"--platform=managed "
                          f"--allow-unauthenticated "
                          f"--no-cpu-throttling "
                          f"--project={env.project.name.split('/')[-1]} ")
        self.log(deploy_command, level=logging.DEBUG)
        os.system(deploy_command)
        os.remove("env.yaml")

    def do_gcloud_interactive(self, _):
        """
        Starts an interactive gcloud shell.
        Usage: gcloud_interactive
        """
        self.log("Starting gcloud interactive shell...")
        cmd_str = "gcloud beta interactive"
        self.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)

    def do_setup_hasura(self, _):
        env = self.get_env()
        if env.gcloud_logged_in is False:
            self.do_gcloud_login()
        if env.organization is None:
            self.do_gcloud_choose_organization(None)
        hasura_project_name = self.collect("Hasura project name: ")
        if self.confirm_loop(hasura_project_name):
            if env.project is None:
                self.do_gcloud_create_project(project_id=hasura_project_name)
            if env.billing_account is None:
                self.do_gcloud_link_billing_account()
            if env.services is None:
                self.do_gcloud_enable_services(None)
            if env.network is None:
                self.do_gcloud_create_network(network_id=hasura_project_name)
            if env.address is None:
                self.do_gcloud_create_address(address_id=hasura_project_name)
            if env.peering is None:
                self.do_gcloud_create_vpc_peering(peering_id=hasura_project_name)
            if env.firewalls is None:
                self.do_gcloud_create_firewall(firewall_id=hasura_project_name)
            if env.database_credential is None:
                self.do_gcloud_create_database(database_id=hasura_project_name)
            if env.connector is None:
                self.do_gcloud_create_serverless_connector(connector_id=hasura_project_name)
            self.do_gcloud_deploy_hasura(None)


def cli():
    cmd = GoogleRoot()
    cmd.cmdloop()


if __name__ == "__main__":
    cli()
