from pysura.pysura_types.root_cmd import RootCmd
from pysura.pysura_types.google_pysura_env import *
import json
import os
from pydantic.error_wrappers import ValidationError
import logging
import random
from string import ascii_letters, digits
import time


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

    @staticmethod
    def user_input_no_loop(func):
        try_again = GoogleRoot.collect("Try again? (y/n)")
        if try_again.strip().lower() == "y":
            func()

    @staticmethod
    def confirm_loop(confirm_str):
        confirm = GoogleRoot.collect("Retype to confirm: ")
        if confirm.strip() != confirm_str.strip():
            GoogleRoot.log("Cancelled.")
            return False
        return True

    @staticmethod
    def gcloud_list_typed_choice(command_str, prompt_str, default="name"):
        GoogleRoot.log(command_str, logging.DEBUG)
        response = os.popen(command_str).read()
        gcloud_list = json.loads(response)
        choice_list = [i[default] for i in gcloud_list]
        if len(choice_list) > 0:
            RootCmd.log(str(choice_list))
            choice = GoogleRoot.collect(prompt_str, choice_list)
            if choice not in choice_list:
                GoogleRoot.log("Invalid choice.")
                return
            return choice
        else:
            GoogleRoot.log("No items found.")

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

    @staticmethod
    def gcloud_list_choice(command_str, model):
        env_names = GoogleRoot.get_env_names(model)
        GoogleRoot.log(command_str, logging.DEBUG)
        if "--format" not in command_str:
            command_str += " --format=json"
        response = os.popen(command_str).read()
        gcloud_list = json.loads(response)
        choice = None
        try:
            _ = gcloud_list[0]["name"]
            choice = GoogleRoot.gcloud_list_typed_choice(command_str,
                                                         "Select a name from the list above: ",
                                                         default="name")
            for i, gcloud_dict in enumerate(gcloud_list):
                if gcloud_dict["name"] == choice:
                    choice = i
                    break
        except KeyError:
            GoogleRoot.log("No items found. Falling back to index.")
        except IndexError:
            GoogleRoot.log("No items found.  Falling back to index.")
        except TypeError:
            GoogleRoot.log("No items found.  Falling back to index.")
        if choice is None:
            for i, gcloud_dict in enumerate(gcloud_list):
                GoogleRoot.log(f"\n{i}: {gcloud_dict['name']}")
            choice = GoogleRoot.collect("Select a number from the list above: ").strip()
            choice = int(choice)
        if choice is not None:
            env_item = gcloud_list[choice]
            try:
                env_item = model(**env_item)
            except ValidationError:
                GoogleRoot.log("The selected item has inconsistent metadata.")
                return GoogleRoot.gcloud_list_choice(command_str, model)
            env = GoogleRoot.get_env()
            env[env_names["selected"]] = env_item
            GoogleRoot.set_env(env)
            return env_item, gcloud_list

    @staticmethod
    def do_exit(_):
        """
        Exits the application.
        Usage: exit
        """
        GoogleRoot.log("Exiting...")
        exit(0)

    @staticmethod
    def retry_loop(cmd_str, name):
        for i in range(5):
            try:
                GoogleRoot.log(cmd_str, level=logging.DEBUG)
                response = os.popen(cmd_str).read()
                response = json.loads(response)
                if len(response) == 0:
                    raise Exception(f"No {name} found.")
                for r in response:
                    if r["name"].split("/")[-1] == name:
                        return response
                raise Exception(f"No {name} found.")
            except Exception as e:
                GoogleRoot.log(f"Error: {e}")
                try:
                    GoogleRoot.log(cmd_str, level=logging.DEBUG)
                    response = os.popen(cmd_str).read()
                    response = json.loads(response)
                    if len(response) == 0:
                        raise Exception(f"No {name} found.")
                    for r in response:
                        if r["network"].split("/")[-1] == name:
                            return response
                    raise Exception(f"No {name} found.")
                except Exception as e:
                    GoogleRoot.log(f"Error: {e}")
                    GoogleRoot.log(f"Retrying in {3 * i} seconds...")
                    time.sleep(3 * i)
        return None

    @staticmethod
    def do_quit(_):
        """
        Exits the application.
        Usage: quit
        """
        GoogleRoot.log("Exiting...")
        exit(0)

    @staticmethod
    def do_gcloud_login(check_logged_in=False):
        """
        Logs into gcloud.
        Usage: gcloud_login
        """
        if isinstance(check_logged_in, str):
            check_logged_in = False
        if check_logged_in:
            env = GoogleRoot.get_env()
            GoogleRoot.log("Checking if already logged into gcloud...")
            if env.gcloud_logged_in:
                GoogleRoot.log("Already logged into gcloud!")
                return
        GoogleRoot.log("Logging into gcloud...")
        cmd_str = "gcloud auth login"
        GoogleRoot.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        login_success = GoogleRoot.collect("Did you successfully login? (y/n)")
        if login_success.strip().lower() == "y":
            env = GoogleRoot.get_env()
            env.gcloud_logged_in = True
            GoogleRoot.set_env(env)
        else:
            GoogleRoot.user_input_no_loop(GoogleRoot.do_gcloud_login)

    @staticmethod
    def do_gcloud_link_billing_account(project_id=None):
        """
        Links a billing account to a project.
        Usage: gcloud_link_billing_account
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            GoogleRoot.log("No project selected.")
            return
        if project_id is None or (isinstance(project_id, str) and len(project_id.strip()) == 0):
            project_id = env.project.name.split("/")[-1]
        billing_account, billing_accounts = GoogleRoot.gcloud_list_choice(
            "gcloud beta billing accounts list --format=json",
            GoogleBillingAccount)
        env.billing_account = billing_account
        env.billing_accounts = billing_accounts
        GoogleRoot.set_env(env)
        cmd_str = f"gcloud beta billing projects link {project_id} " \
                  f"--billing-account={billing_account.name.split('/')[-1]}"
        GoogleRoot.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)

    @staticmethod
    def do_gcloud_enable_services(_):
        env = GoogleRoot.get_env()
        if env.project is None:
            GoogleRoot.log("No project selected.")
            return
        GoogleRoot.log("Enabling services...")
        project_id = env.project.name.split("/")[-1]
        cmd_str = f"gcloud services enable servicenetworking.googleapis.com --project={project_id}"
        GoogleRoot.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable compute.googleapis.com --project={project_id}"
        GoogleRoot.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable sqladmin.googleapis.com --project={project_id}"
        GoogleRoot.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable vpcaccess.googleapis.com --project={project_id}"
        GoogleRoot.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable identitytoolkit.googleapis.com --project={project_id}"
        GoogleRoot.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable run.googleapis.com --project={project_id}"
        GoogleRoot.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable secretmanager.googleapis.com --project={project_id}"
        GoogleRoot.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services list --project={project_id} --format=json"
        GoogleRoot.log(cmd_str, level=logging.DEBUG)
        response = os.popen(cmd_str).read()
        services = json.loads(response)
        env.services = services
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_choose_organization(_):
        """
        Chooses an organization.
        Usage: gcloud_choose_organization
        """
        GoogleRoot.log("Choosing organization...")
        org, orgs = GoogleRoot.gcloud_list_choice("gcloud organizations list --format=json", GoogleOrganization)
        env = GoogleRoot.get_env()
        env.organization = org
        env.organizations = orgs
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_create_project(project_id=""):
        """
        Creates a gcloud project.
        Usage: gcloud_project_create
        """
        env = GoogleRoot.get_env()
        use_organization = GoogleRoot.collect("Do you want to use an organization? (y/n)")
        use_org = use_organization.strip().lower() == "y"
        if use_org:
            if env.organization is None:
                GoogleRoot.log("No organization selected.")
                return
        arg_len = len(project_id.strip())
        if arg_len == 0:
            project_name = GoogleRoot.collect("Enter a project name: ")
        else:
            project_name = project_id
        if arg_len > 0 or GoogleRoot.confirm_loop(project_name):
            cmd_str = f"gcloud projects create {project_name}"
            if use_org:
                assert env.organization is not None
                cmd_str += f" --organization={env.organization.name.split('/')[-1]}"
            GoogleRoot.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = f"gcloud projects list --format=json"
            GoogleRoot.log(cmd_str, level=logging.DEBUG)
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
            GoogleRoot.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            env.project = project
            env.projects = projects
            GoogleRoot.set_env(env)
        else:
            GoogleRoot.user_input_no_loop(GoogleRoot.do_gcloud_create_project)

    @staticmethod
    def do_gcloud_choose_project(_):
        """
        Chooses a project.
        Usage: gcloud_choose_project
        """
        env = GoogleRoot.get_env()
        if not env.gcloud_logged_in:
            GoogleRoot.do_gcloud_login()
        GoogleRoot.log("Choosing project...")
        project, projects = GoogleRoot.gcloud_list_choice("gcloud projects list --format=json", GoogleProject)
        env.project = project
        env.projects = projects
        GoogleRoot.set_env(env)
        if project is not None:
            cmd_str = f"gcloud config set project {project.name.split('/')[-1]}"
            GoogleRoot.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)

    @staticmethod
    def do_gcloud_create_network(network_id=""):
        """
        Creates a Network.
        Usage: gcloud_network_create
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            GoogleRoot.log("No project selected.")
            return
        arg_len = len(network_id.strip())
        if arg_len == 0:
            network_name = GoogleRoot.collect("Enter a network name: ")
        else:
            network_name = network_id
        if arg_len > 0 or GoogleRoot.confirm_loop(network_name):
            cmd_str = f"gcloud compute networks create {network_name}" \
                      f" --subnet-mode=auto" \
                      f" --project={env.project.name.split('/')[-1]}"
            GoogleRoot.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = f"gcloud compute networks list " \
                      f"--project={env.project.name.split('/')[-1]} " \
                      f"--format=json"
            gcloud_list = GoogleRoot.retry_loop(cmd_str, network_name)
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
                GoogleRoot.log("Network not found.")
                return
            env.network = network_selected
            env.networks = network_set
            GoogleRoot.set_env(env)
        else:
            GoogleRoot.user_input_no_loop(GoogleRoot.do_gcloud_create_network)

    @staticmethod
    def do_gcloud_choose_network(_):
        """
        Chooses a Network.
        Usage: gcloud_network_choose
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            GoogleRoot.log("No project selected.")
            return
        GoogleRoot.log("Choosing network...")
        network, networks = GoogleRoot.gcloud_list_choice(f"gcloud compute networks list "
                                                          f"--project={env.project.name.split('/')[-1]} "
                                                          f"--format=json", GoogleNetwork)
        env.network = network
        env.networks = networks
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_create_address(address_id=""):
        """
        Creates an address.
        Usage: gcloud_address_create
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            GoogleRoot.log("No project selected.")
            return
        if env.network is None:
            GoogleRoot.log("No network selected.")
            return
        arg_len = len(address_id.strip())
        if arg_len == 0:
            address_name = GoogleRoot.collect("Enter an address name: ")
        else:
            address_name = address_id
        if arg_len > 0 or GoogleRoot.confirm_loop(address_name):
            cmd_str = f"gcloud compute addresses create {address_name} " \
                      f"--global " \
                      f"--purpose=VPC_PEERING " \
                      f"--prefix-length=16 " \
                      f"--network={env.network.name.split('/')[-1]} " \
                      f"--project={env.project.name.split('/')[-1]}"
            GoogleRoot.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = f"gcloud compute addresses list " \
                      f"--project={env.project.name.split('/')[-1]} " \
                      f"--format=json"
            gcloud_list = GoogleRoot.retry_loop(cmd_str, address_name)
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
                GoogleRoot.log("Address not found.")
                return
            env.address = address_selected
            env.addresses = address_set
            GoogleRoot.set_env(env)
            if address_selected is None:
                GoogleRoot.log("Address not found.")
                return
        else:
            GoogleRoot.user_input_no_loop(GoogleRoot.do_gcloud_create_address)

    @staticmethod
    def do_gcloud_choose_address(_):
        """
        Chooses an address.
        Usage: gcloud_address_choose
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            GoogleRoot.log("No project selected.")
            return
        if env.network is None:
            GoogleRoot.log("No network selected.")
            return
        GoogleRoot.log("Choosing address...")
        address, addresses = GoogleRoot.gcloud_list_choice(f"gcloud compute addresses list "
                                                           f"--project={env.project.name.split('/')[-1]} "
                                                           f"--format=json", GoogleAddress)
        env.address = address
        env.addresses = addresses
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_create_vpc_peering(peering_id=""):
        """
        Creates a VPC Peering.
        Usage: gcloud_vpc_peering_create
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            GoogleRoot.log("No project selected.")
            return
        if env.network is None:
            GoogleRoot.log("No network selected.")
            return
        if env.address is None:
            GoogleRoot.log("No address selected.")
            return

        arg_len = len(peering_id.strip())
        if arg_len == 0:
            peering_name = GoogleRoot.collect("Enter a peering name: ")
        else:
            peering_name = peering_id
        if arg_len > 0 or GoogleRoot.confirm_loop(peering_name):
            cmd_str = f"gcloud services vpc-peerings connect " \
                      f"--service=servicenetworking.googleapis.com " \
                      f"--ranges={env.address.name.split('/')[-1]} " \
                      f"--network={env.network.name.split('/')[-1]} " \
                      f"--project={env.project.name.split('/')[-1]}"
            GoogleRoot.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = f"gcloud services vpc-peerings list " \
                      f"--project={env.project.name.split('/')[-1]} " \
                      f"--network={env.network.name.split('/')[-1]} --format=json"
            gcloud_list = GoogleRoot.retry_loop(cmd_str, peering_name)
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
                GoogleRoot.log("Peering not found.")
                return
            env.peering = peering_selected
            env.peerings = peering_set
            GoogleRoot.set_env(env)
        else:
            GoogleRoot.user_input_no_loop(GoogleRoot.do_gcloud_create_vpc_peering)

    @staticmethod
    def do_gcloud_choose_vpc_peering(_):
        """
        Chooses a VPC Peering.
        Usage: gcloud_vpc_peering_choose
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            GoogleRoot.log("No project selected.")
            return
        if env.network is None:
            GoogleRoot.log("No network selected.")
            return
        if env.address is None:
            GoogleRoot.log("No address selected.")
            return
        GoogleRoot.log("Choosing peering...")
        peering, peerings = GoogleRoot.gcloud_list_choice(
            f"gcloud services vpc-peerings list "
            f"--project={env.project.name.split('/')[-1]} "
            f"--network={env.network.name.split('/')[-1]} --format=json",
            GoogleVpcPeering
        )
        env.peering = peering
        env.peerings = peerings
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_create_firewall(firewall_id=""):
        """
        Creates a firewall.
        Usage: gcloud_firewall_create
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            GoogleRoot.log("No project selected.")
            return
        if env.network is None:
            GoogleRoot.log("No network selected.")
            return
        if env.address is None:
            GoogleRoot.log("No address selected.")
            return
        if env.peering is None:
            GoogleRoot.log("No peering selected.")
            return

        arg_len = len(firewall_id.strip())
        if arg_len == 0:
            firewall_name = GoogleRoot.collect("Enter a firewall name: ")
        else:
            firewall_name = firewall_id
        if arg_len > 0 or GoogleRoot.confirm_loop(firewall_name):
            cmd_str = f"gcloud compute firewall-rules create {firewall_name}-allow-traffic  " \
                      f"--network={env.network.name.split('/')[-1]} " \
                      f"--allow=tcp,udp,icmp " \
                      f"--source-ranges=0.0.0.0/0 " \
                      f"--project={env.project.name.split('/')[-1]}"
            GoogleRoot.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = f"gcloud compute firewall-rules list " \
                      f"--project={env.project.name.split('/')[-1]} " \
                      f"--format=json"
            GoogleRoot.retry_loop(cmd_str, f"{firewall_name}-allow-traffic")
            cmd_str = f"gcloud compute firewall-rules create {firewall_name}-allow-internal  " \
                      f"--network={env.network.name.split('/')[-1]} " \
                      f"--allow=tcp:22,tcp:3389,icmp " \
                      f"--project={env.project.name.split('/')[-1]}"
            GoogleRoot.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = f"gcloud compute firewall-rules list " \
                      f"--project={env.project.name.split('/')[-1]} " \
                      f"--format=json"
            GoogleRoot.log(cmd_str, level=logging.DEBUG)
            gcloud_list = json.loads(os.popen(cmd_str).read())
            firewall_set = []
            for firewall in gcloud_list:
                firewall_data = GoogleFirewall(
                    **firewall
                )
                firewall_set.append(firewall_data)
            env.firewalls = firewall_set
            GoogleRoot.set_env(env)
        else:
            GoogleRoot.user_input_no_loop(GoogleRoot.do_gcloud_create_firewall)

    @staticmethod
    def do_gcloud_create_database(database_id=""):
        env = GoogleRoot.get_env()
        if env.project is None:
            GoogleRoot.log("No project selected.")
            return
        if env.network is None:
            GoogleRoot.log("No network selected.")
            return

        arg_len = len(database_id.strip())
        if arg_len == 0:
            db_name = GoogleRoot.collect("Enter a database name: ")
        else:
            db_name = database_id
        if arg_len == 0 and not GoogleRoot.confirm_loop(db_name):
            GoogleRoot.user_input_no_loop(GoogleRoot.do_gcloud_create_database)
            return
        cpu_number = GoogleRoot.collect("Enter the number of CPU's for the database number: ")
        memory_amount = GoogleRoot.collect("Enter the amount of memory for the database (MiB): ", ["2048",
                                                                                                   "4096",
                                                                                                   "8192",
                                                                                                   "16384",
                                                                                                   "24576",
                                                                                                   "32768"])
        db_version = GoogleRoot.collect("Enter the database version (Supports POSTGRES_14, ):", ["POSTGRES_14"])
        cpu_number = str(int(cpu_number.strip()))
        memory_amount = f"{str(int(memory_amount.strip()))}MiB"
        zone = GoogleRoot.gcloud_list_typed_choice(f"gcloud compute zones list "
                                                   f"--project={env.project.name.split('/')[-1]} "
                                                   f"--format=json", "Enter a zone: ", "name")
        if zone is None:
            GoogleRoot.log("No zone selected.")
            return
        availability_types = ["regional", "zonal"]
        availability_type = GoogleRoot.collect("Enter the availability type: (regional/zonal)", availability_types)
        if availability_type not in availability_types:
            GoogleRoot.log("Invalid availability type.")
            return
        db_password = GoogleRoot.password()
        GoogleRoot.log(f"You are preparing to create a database with the following parameters: "
                       f"Name: {db_name}, CPU's: {cpu_number}, Memory: {memory_amount}, "
                       f"Version: {db_version}, Zone: {zone}, "
                       f"Network: {env.network.name.split('/')[-1]}, Project: {env.project.name.split('/')[-1]}, "
                       f"DatabasePassword: {db_password}")
        continue_flag = GoogleRoot.collect("Continue? (y/n): ", ["y", "n"])
        if continue_flag.strip().lower() != "y":
            GoogleRoot.log("Aborting...")
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
        GoogleRoot.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        db = GoogleDatabase()
        cmd_str = f"gcloud sql instances list " \
                  f"--project={env.project.name.split('/')[-1]} " \
                  f"--format=json"
        gcloud_list = GoogleRoot.retry_loop(cmd_str, f"{db_name}")
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
            GoogleRoot.log("Database not found.")
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
        env.database = db
        env.databases = db_set
        env.database_credential = db_creds
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_create_serverless_connector(connector_id=""):
        """
        Creates a serverless connector.
        Usage: create_serverless_connector
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            GoogleRoot.log("No project selected.")
            return
        if env.network is None:
            GoogleRoot.log("No network selected.")
            return
        if env.database is None:
            GoogleRoot.log("No database selected.")
            return

        range_choice = GoogleRoot.collect("Select a range: ", [f"10.{i}.0.0/28" for i in range(8, 100)])
        arg_len = len(connector_id.split())
        if arg_len == 0:
            connector_name = GoogleRoot.collect("Enter a connector name: ")
        else:
            connector_name = connector_id
        if arg_len == 0 and not GoogleRoot.confirm_loop(connector_name):
            GoogleRoot.user_input_no_loop(GoogleRoot.do_gcloud_create_serverless_connector)
            return
        cmd_str = f"gcloud compute networks vpc-access connectors create {connector_name} " \
                  f"--network={env.network.name.split('/')[-1]} " \
                  f"--region={env.database.region} " \
                  f"--range={range_choice} " \
                  f"--project={env.project.name.split('/')[-1]}"
        GoogleRoot.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud compute networks vpc-access connectors list " \
                  f"--project={env.project.name.split('/')[-1]} " \
                  f"--region={env.database.region} --format=json"
        gcloud_list = GoogleRoot.retry_loop(cmd_str, f"{connector_name}")
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
            GoogleRoot.log("Connector not found.")
            return
        env.connector = connector_selected
        env.connectors = connector_set
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_choose_serverless_connector(_):
        """
        Chooses a serverless connector.
        Usage: choose_serverless_connector
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            GoogleRoot.log("No project selected.")
            return
        if env.network is None:
            GoogleRoot.log("No network selected.")
            return
        if env.database is None:
            GoogleRoot.log("No database selected.")
            return

        cmd_str = f"gcloud compute networks vpc-access connectors list " \
                  f"--region={env.database.region} " \
                  f"--project={env.project.name.split('/')[-1]} --format=json"
        GoogleRoot.log(cmd_str, level=logging.DEBUG)
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
            GoogleRoot.log("Connector not found.")
            return

        env.connector = connector_selected
        env.connectors = connector_set
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_deploy_hasura(_):
        env = GoogleRoot.get_env()
        if env.project is None:
            GoogleRoot.log("No project selected.")
            return
        if env.connector is None:
            GoogleRoot.log("No connector selected.")
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
                GoogleRoot.log("No service account found.")
                return
            cmd_log_str = (f"gcloud projects add-iam-policy-binding {env.project.name.split('/')[-1]} "
                           f"--member=serviceAccount:{account_id} "
                           f"--role=roles/cloudbuild.builds.builder"
                           )
            GoogleRoot.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            cmd_log_str = (f"gcloud projects add-iam-policy-binding {env.project.name.split('/')[-1]} "
                           f"--member=serviceAccount:{account_id} "
                           f"--role=roles/run.admin"
                           )
            GoogleRoot.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            cmd_log_str = "docker pull --platform=linux/amd64 hasura/graphql-engine:latest"
            GoogleRoot.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            cmd_log_str = f"docker tag hasura/graphql-engine:latest " \
                          f"gcr.io/{env.project.name.split('/')[-1]}/hasura:latest"
            GoogleRoot.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            cmd_log_str = f"docker push gcr.io/{env.project.name.split('/')[-1]}/hasura:latest"
            GoogleRoot.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            hasura_secret = GoogleRoot.password()
            timeout = GoogleRoot.collect("Timeout (seconds)", ["60s", "300s", "600s", "900s", "1200s", "3600s"])
            cpu = GoogleRoot.collect("CPU (cores)", ["1", "2", "4", "8", "16", "32", "64"])
            memory = GoogleRoot.collect("Memory", ["256Mi", "512Mi", "1Gi", "2Gi", "4Gi", "8Gi", "16Gi", "32Gi"])
            max_instances = GoogleRoot.collect("Max instances: ")
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
            GoogleRoot.set_env(env)
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
        GoogleRoot.log(deploy_command, level=logging.DEBUG)
        os.system(deploy_command)
        os.remove("env.yaml")

    @staticmethod
    def do_gcloud_interactive(_):
        """
        Starts an interactive gcloud shell.
        Usage: gcloud_interactive
        """
        GoogleRoot.log("Starting gcloud interactive shell...")
        cmd_str = "gcloud beta interactive"
        GoogleRoot.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)

    @staticmethod
    def do_setup_hasura(_):
        env = GoogleRoot.get_env()
        if env.gcloud_logged_in is False:
            GoogleRoot.do_gcloud_login()
        if env.organization is None:
            GoogleRoot.do_gcloud_choose_organization(None)
        hasura_project_name = GoogleRoot.collect("Hasura project name: ")
        if GoogleRoot.confirm_loop(hasura_project_name):
            if env.project is None:
                GoogleRoot.do_gcloud_create_project(project_id=hasura_project_name)
            if env.billing_account is None:
                GoogleRoot.do_gcloud_link_billing_account()
            if env.services is None:
                GoogleRoot.do_gcloud_enable_services(None)
            if env.network is None:
                GoogleRoot.do_gcloud_create_network(network_id=hasura_project_name)
            if env.address is None:
                GoogleRoot.do_gcloud_create_address(address_id=hasura_project_name)
            if env.peering is None:
                GoogleRoot.do_gcloud_create_vpc_peering(peering_id=hasura_project_name)
            if env.firewalls is None:
                GoogleRoot.do_gcloud_create_firewall(firewall_id=hasura_project_name)
            if env.database_credential is None:
                GoogleRoot.do_gcloud_create_database(database_id=hasura_project_name)
            if env.connector is None:
                GoogleRoot.do_gcloud_create_serverless_connector(connector_id=hasura_project_name)
            GoogleRoot.do_gcloud_deploy_hasura(None)


def cli():
    cmd = GoogleRoot()
    cmd.cmdloop()


if __name__ == "__main__":
    cli()
