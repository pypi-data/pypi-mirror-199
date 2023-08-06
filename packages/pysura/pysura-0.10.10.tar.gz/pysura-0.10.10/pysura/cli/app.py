from pysura.pysura_types.root_cmd import RootCmd
from pysura.pysura_types.google_pysura_env import *
import json
import os
from pysura.pysura_types.pysura_std import PysuraStd
from pydantic.error_wrappers import ValidationError
import logging
import sys
import random
from string import ascii_letters, digits

root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt="%(asctime)s %(filename)-25s %(levelname)-5s %(message)s",
                              datefmt="%Y-%m-%d %I:%H:%M")
handler.setFormatter(formatter)
root.addHandler(handler)


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
        PysuraStd.log(f"Dumping data:\n{value.json()}", level=logging.DEBUG)
        with open(file_name, "w") as f:
            json.dump(value.dict(), f)

    @staticmethod
    def user_input_no_loop(func):
        try_again = PysuraStd.collect("Try again? (y/n)")
        if try_again.strip().lower() == "y":
            func()

    @staticmethod
    def confirm_loop(confirm_str):
        confirm = PysuraStd.collect("Retype to confirm: ")
        if confirm.strip() != confirm_str.strip():
            PysuraStd.log("Cancelled.")
            return False
        return True

    @staticmethod
    def gcloud_list_typed_choice(command_str, prompt_str, default="NAME"):
        PysuraStd.log(command_str, logging.DEBUG)
        response = os.popen(command_str).read()
        gcloud_list = json.loads(response)
        choice_list = [i[default] for i in gcloud_list]
        if len(choice_list) > 0:
            choice = PysuraStd.collect(prompt_str, choice_list)
            if choice not in choice_list:
                PysuraStd.log("Invalid choice.")
                return
            return choice
        else:
            PysuraStd.log("No items found.")

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
        PysuraStd.log(command_str, logging.DEBUG)
        if "--format" not in command_str:
            command_str += " --format=json"
        response = os.popen(command_str).read()
        gcloud_list = json.loads(response)
        for i, gcloud_dict in enumerate(gcloud_list):
            PysuraStd.log(f"{i}: {gcloud_dict}")
        choice = PysuraStd.collect("Select a number from the list above: ").strip()
        choice = int(choice)
        env_item = gcloud_list[choice]
        print(gcloud_list[choice])
        try:
            env_item = model(**env_item)
        except ValidationError:
            PysuraStd.log("The selected item has inconsistent metadata.")
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
        PysuraStd.log("Exiting...")
        exit(0)

    @staticmethod
    def do_quit(_):
        """
        Exits the application.
        Usage: quit
        """
        PysuraStd.log("Exiting...")
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
            PysuraStd.log("Checking if already logged into gcloud...")
            if env.gcloud_logged_in:
                PysuraStd.log("Already logged into gcloud!")
                return
        PysuraStd.log("Logging into gcloud...")
        cmd_str = "gcloud auth login"
        PysuraStd.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        login_success = PysuraStd.collect("Did you successfully login? (y/n)")
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
            PysuraStd.log("No project selected.")
            return
        if project_id is None or (isinstance(project_id, str) and len(project_id.strip()) == 0):
            project_id = env.project.name.split("/")[-1]
        billing_account, billing_accounts = GoogleRoot.gcloud_list_choice(
            "gcloud beta billing accounts list --format=json",
            GoogleBillingAccount)
        env.billing_account = billing_account
        GoogleRoot.set_env(env)
        cmd_str = f"gcloud beta billing projects link {project_id} " \
                  f"--billing-account={billing_account.billing_account_id}"
        PysuraStd.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)

    @staticmethod
    def do_gcloud_enable_services(_):
        env = GoogleRoot.get_env()
        if env.project is None:
            PysuraStd.log("No project selected.")
            return
        PysuraStd.log("Enabling services...")
        project_id = env.project.name.split("/")[-1]
        cmd_str = f"gcloud services enable servicenetworking.googleapis.com --project={project_id}"
        PysuraStd.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable compute.googleapis.com --project={project_id}"
        PysuraStd.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable sqladmin.googleapis.com --project={project_id}"
        PysuraStd.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable vpcaccess.googleapis.com --project={project_id}"
        PysuraStd.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable identitytoolkit.googleapis.com --project={project_id}"
        PysuraStd.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable run.googleapis.com --project={project_id}"
        PysuraStd.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud services enable secretmanager.googleapis.com --project={project_id}"
        PysuraStd.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)

    @staticmethod
    def do_gcloud_choose_organization(_):
        """
        Chooses an organization.
        Usage: gcloud_choose_organization
        """
        PysuraStd.log("Choosing organization...")
        org, orgs = GoogleRoot.gcloud_list_choice("gcloud organizations list --format=json", GoogleOrganization)
        env = GoogleRoot.get_env()
        env.organization = org
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_create_project(_):
        """
        Creates a gcloud project.
        Usage: gcloud_project_create
        """
        env = GoogleRoot.get_env()
        use_organization = PysuraStd.collect("Do you want to use an organization? (y/n)")
        use_org = use_organization.strip().lower() == "y"
        if use_org:
            if env.organization is None:
                PysuraStd.log("No organization selected.")
                return
        project_name = PysuraStd.collect("Enter a project name: ")
        if GoogleRoot.confirm_loop(project_name):
            cmd_str = f"gcloud projects create {project_name}"
            if use_org:
                assert env.organization is not None
                cmd_str += f" --organization={env.organization.name.split('/')[-1]}"
            PysuraStd.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = f"gcloud projects list --format=json"
            PysuraStd.log(cmd_str, level=logging.DEBUG)
            response = os.popen(cmd_str).read()
            projects = json.loads(response)
            project = None
            for p in projects:
                project_data = GoogleProject(**p)
                if project_data.name.split("/")[-1] == project_name:
                    project = GoogleProject(p)
                    break
            env.project = project
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
        PysuraStd.log("Choosing project...")
        project, projects = GoogleRoot.gcloud_list_choice("gcloud projects list --format=json", GoogleProject)
        env.project = project
        GoogleRoot.set_env(env)
        if project is not None:
            cmd_str = f"gcloud config set project {project.project_id}"
            PysuraStd.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)

    @staticmethod
    def do_gcloud_create_network(_):
        """
        Creates a Network.
        Usage: gcloud_network_create
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            PysuraStd.log("No project selected.")
            return
        network_name = PysuraStd.collect("Enter a network name: ")
        if GoogleRoot.confirm_loop(network_name):
            cmd_str = f"gcloud compute networks create {network_name}" \
                      f" --subnet-mode=auto" \
                      f" --project={env.project.name.split('/')[-1]}"
            PysuraStd.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = "gcloud compute networks list --format=json"
            PysuraStd.log(cmd_str, level=logging.DEBUG)
            response = os.popen(cmd_str).read()
            gcloud_list = json.loads(response)
            network_selected = None
            network_set = []
            for gcloud_item in gcloud_list:
                network = GoogleNetwork(
                    network_id=gcloud_item["NAME"],
                    subnet_mode=gcloud_item["SUBNET_MODE"],
                    bgp_routing_mode=gcloud_item["BGP_ROUTING_MODE"],
                    ipv4_range=gcloud_item["IPV4_RANGE"],
                    gateway_ipv4=gcloud_item["GATEWAY_IPV4"]
                )
                network_set.append(network)
                if network == network_name:
                    network_selected = network

                if network_selected is None:
                    PysuraStd.log("Network not found.")
                    return
                env.network = network_selected
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
            PysuraStd.log("No project selected.")
            return
        PysuraStd.log("Choosing network...")
        network, networks = GoogleRoot.gcloud_list_choice("gcloud compute networks list --format=json", GoogleNetwork)
        env.network = network
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_create_address(_):
        """
        Creates an address.
        Usage: gcloud_address_create
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            PysuraStd.log("No project selected.")
            return
        if env.network is None:
            PysuraStd.log("No network selected.")
            return
        address_name = PysuraStd.collect("Enter an address name: ")
        if GoogleRoot.confirm_loop(address_name):
            cmd_str = f"gcloud compute addresses create {address_name} " \
                      f"--global " \
                      f"--purpose=VPC_PEERING " \
                      f"--prefix-length=16 " \
                      f"--network={env.network.name.split('/')[-1]} " \
                      f"--project={env.project.name.split('/')[-1]}"
            PysuraStd.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = "gcloud compute addresses list --format=json"
            PysuraStd.log(cmd_str, level=logging.DEBUG)
            response = os.popen(cmd_str).read()
            gcloud_list = json.loads(response)
            address_selected = None
            address_set = []
            for gcloud_item in gcloud_list:
                address = GoogleAddress(
                    address_id=gcloud_item["NAME"],
                    address=gcloud_item["ADDRESS/RANGE"],
                    address_type=gcloud_item["TYPE"],
                    purpose=gcloud_item["PURPOSE"],
                    network=gcloud_item["NETWORK"],
                    region=gcloud_item["REGION"],
                    subnet=gcloud_item["SUBNET"],
                    status=gcloud_item["STATUS"]
                )
                address_set.append(address)
                if address.name.split('/')[-1] == address_name:
                    address_selected = address
            env.address = address_selected
            GoogleRoot.set_env(env)
            if address_selected is None:
                PysuraStd.log("Address not found.")
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
            PysuraStd.log("No project selected.")
            return
        if env.network is None:
            PysuraStd.log("No network selected.")
            return
        PysuraStd.log("Choosing address...")
        address, addresses = GoogleRoot.gcloud_list_choice("gcloud compute addresses list --format=json", GoogleAddress)
        env.address = address
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_create_vpc_peering(_):
        """
        Creates a VPC Peering.
        Usage: gcloud_vpc_peering_create
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            PysuraStd.log("No project selected.")
            return
        if env.network is None:
            PysuraStd.log("No network selected.")
            return
        if env.address is None:
            PysuraStd.log("No address selected.")
            return
        peering_name = PysuraStd.collect("Enter a peering name: ")
        if GoogleRoot.confirm_loop(peering_name):
            cmd_str = f"gcloud services vpc-peerings connect " \
                      f"--service=servicenetworking.googleapis.com " \
                      f"--ranges={env.address.address} " \
                      f"--network={env.network.name.split('/')[-1]} " \
                      f"--project={env.project.name.split('/')[-1]}"
            PysuraStd.log(cmd_str, level=logging.DEBUG)
            os.system(cmd_str)
            cmd_str = f"gcloud services vpc-peerings list --network={env.network.name.split('/')[-1]} --format=json"
            PysuraStd.log(cmd_str, level=logging.DEBUG)
            response = os.popen(cmd_str).read()
            gcloud_list = json.loads(response)
            peering_selected = None
            peering_set = []
            for peering in gcloud_list:
                peering_data = GooglePeering(
                    network=peering["network"],
                    peering=peering["peering"],
                    reserved_peering_ranges=peering["reservedPeeringRanges"],
                    service=peering["service"]
                )
                peering_set.append(peering_data)
                if peering_name in peering_data["reservedPeeringRanges"]:
                    peering_selected = peering_data
            env.peering = peering_selected
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
            PysuraStd.log("No project selected.")
            return
        if env.network is None:
            PysuraStd.log("No network selected.")
            return
        if env.address is None:
            PysuraStd.log("No address selected.")
            return
        PysuraStd.log("Choosing peering...")
        peering, peerings = GoogleRoot.gcloud_list_choice(
            f"gcloud services vpc-peerings list --network={env.network.name.split('/')[-1]} --format=json",
            GooglePeering
        )
        env.peering = peering
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_create_database(_):
        env = GoogleRoot.get_env()
        if env.project is None:
            PysuraStd.log("No project selected.")
            return
        if env.network is None:
            PysuraStd.log("No network selected.")
            return

        db_name = PysuraStd.collect("Enter a database name: ")
        if not GoogleRoot.confirm_loop(db_name):
            GoogleRoot.user_input_no_loop(GoogleRoot.do_gcloud_create_database)
            return
        cpu_number = PysuraStd.collect("Enter the number of CPU's for the database number: ")
        memory_amount = PysuraStd.collect("Enter the amount of memory for the database (MiB): ", ["2048",
                                                                                                  "4096",
                                                                                                  "8192",
                                                                                                  "16384",
                                                                                                  "24576",
                                                                                                  "32768"])
        db_version = PysuraStd.collect("Enter the database version (Supports POSTGRES_14, ):", ["POSTGRES_14"])
        cpu_number = str(int(cpu_number.strip()))
        memory_amount = f"{str(int(memory_amount.strip()))}MiB"
        zone = GoogleRoot.gcloud_list_typed_choice("gcloud compute zones list --format=json", "Enter a zone: ", "NAME")
        if zone is None:
            PysuraStd.log("No zone selected.")
            return
        availability_types = ["regional", "zonal"]
        availability_type = PysuraStd.collect("Enter the availability type: (regional/zonal)", availability_types)
        if availability_type not in availability_types:
            PysuraStd.log("Invalid availability type.")
            return
        db_password = GoogleRoot.password()
        PysuraStd.log(f"You are preparing to create a database with the following parameters: "
                      f"Name: {db_name}, CPU's: {cpu_number}, Memory: {memory_amount}, "
                      f"Version: {db_version}, Zone: {zone}, "
                      f"Network: {env.network.name.split('/')[-1]}, Project: {env.project.name.split('/')[-1]}, "
                      f"DatabasePassword: {db_password}")
        continue_flag = PysuraStd.collect("Continue? (y/n): ", ["y", "n"])
        if continue_flag.strip().lower() != "y":
            PysuraStd.log("Aborting...")
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
        PysuraStd.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        db = GoogleDatabase()
        db.database_id = db_name
        db.version = db_version
        db.zone = zone
        cmd_str = "gcloud sql instances list --format=json"
        PysuraStd.log(cmd_str, level=logging.DEBUG)
        response = os.popen(cmd_str).read()
        gcloud_list = json.loads(response)
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
            PysuraStd.log("Database not found.")
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
        env.database_credential = db_creds
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_create_serverless_connector(_):
        """
        Creates a serverless connector.
        Usage: create_serverless_connector
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            PysuraStd.log("No project selected.")
            return
        if env.network is None:
            PysuraStd.log("No network selected.")
            return
        if env.database is None:
            PysuraStd.log("No database selected.")
            return

        range_choice = PysuraStd.collect("Select a range: ", [f"10.{i}.0.0/28" for i in range(8, 100)])
        connector_name = PysuraStd.collect("Enter a connector name: ")
        if not GoogleRoot.confirm_loop(connector_name):
            GoogleRoot.user_input_no_loop(GoogleRoot.do_gcloud_create_serverless_connector)
            return
        cmd_str = f"gcloud compute networks vpc-access connectors create {connector_name} " \
                  f"--network={env.network.name.split('/')[-1]} " \
                  f"--region={env.database.region} " \
                  f"--range={range_choice} "
        PysuraStd.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)
        cmd_str = f"gcloud compute networks vpc-access connectors list --region={env.database.region} --format=json"
        PysuraStd.log(cmd_str, level=logging.DEBUG)
        response = os.popen(cmd_str).read()
        gcloud_list = json.loads(response)
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
            PysuraStd.log("Connector not found.")
            return

        env.connector = connector_selected
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_choose_serverless_connector(_):
        """
        Chooses a serverless connector.
        Usage: choose_serverless_connector
        """
        env = GoogleRoot.get_env()
        if env.project is None:
            PysuraStd.log("No project selected.")
            return
        if env.network is None:
            PysuraStd.log("No network selected.")
            return
        if env.database is None:
            PysuraStd.log("No database selected.")
            return

        cmd_str = f"gcloud compute networks vpc-access connectors list --region={env.database.region} --format=json"
        PysuraStd.log(cmd_str, level=logging.DEBUG)
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
            PysuraStd.log("Connector not found.")
            return

        env.connectors = connector_set
        env.connector = connector_selected
        GoogleRoot.set_env(env)

    @staticmethod
    def do_gcloud_deploy_hasura(_):
        env = GoogleRoot.get_env()
        if env.project is None:
            PysuraStd.log("No project selected.")
            return
        if env.connector is None:
            PysuraStd.log("No connector selected.")
            return
        if env.hasura is None:
            account_choices = json.loads(os.popen("gcloud iam service-accounts list --format=json").read())
            account_id = None
            for i, account in enumerate(account_choices):
                if "Compute Engine default service account" in account["displayName"]:
                    account_id = account["email"]
                    break
            if account_id is None:
                PysuraStd.log("No service account found.")
                return
            cmd_log_str = (f"gcloud projects add-iam-policy-binding {env.project.name.split('/')[-1]} "
                           f"--member=serviceAccount:{account_id} "
                           f"--role=roles/cloudbuild.builds.builder"
                           )
            PysuraStd.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            cmd_log_str = (f"gcloud projects add-iam-policy-binding {env.project.name.split('/')[-1]} "
                           f"--member=serviceAccount:{account_id} "
                           f"--role=roles/run.admin"
                           )
            PysuraStd.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            cmd_log_str = "docker pull --platform=linux/amd64 hasura/graphql-engine:latest"
            PysuraStd.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            cmd_log_str = f"docker tag hasura/graphql-engine:latest " \
                          f"gcr.io/{env.project.name.split('/')[-1]}/hasura:latest"
            PysuraStd.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            cmd_log_str = f"docker push gcr.io/{env.project.name.split('/')[-1]}/hasura:latest"
            PysuraStd.log(cmd_log_str, level=logging.DEBUG)
            os.system(cmd_log_str)
            hasura_secret = GoogleRoot.password()
            timeout = PysuraStd.collect("Timeout (seconds)", ["60s", "300s", "600s", "900s", "1200s", "3600s"])
            cpu = PysuraStd.collect("CPU (cores)", ["1", "2", "4", "8", "16", "32", "64"])
            memory = PysuraStd.collect("Memory", ["256Mi", "512Mi", "1Gi", "2Gi", "4Gi", "8Gi", "16Gi", "32Gi"])
            max_instances = PysuraStd.collect("Max instances: ")
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
                          f"--no-cpu-throttling")
        PysuraStd.log(deploy_command, level=logging.DEBUG)
        os.system(deploy_command)
        os.remove("env.yaml")

    @staticmethod
    def do_gcloud_interactive(_):
        """
        Starts an interactive gcloud shell.
        Usage: gcloud_interactive
        """
        PysuraStd.log("Starting gcloud interactive shell...")
        cmd_str = "gcloud beta interactive"
        PysuraStd.log(cmd_str, level=logging.DEBUG)
        os.system(cmd_str)

    @staticmethod
    def do_setup_hasura(_):
        GoogleRoot.do_gcloud_login(check_logged_in=True)
        GoogleRoot.do_gcloud_choose_organization(None)
        GoogleRoot.do_gcloud_create_project(None)
        GoogleRoot.do_gcloud_link_billing_account(None)
        GoogleRoot.do_gcloud_enable_services(None)
        GoogleRoot.do_gcloud_create_network(None)
        GoogleRoot.do_gcloud_create_address(None)
        GoogleRoot.do_gcloud_create_vpc_peering(None)
        GoogleRoot.do_gcloud_create_database(None)
        GoogleRoot.do_gcloud_create_serverless_connector(None)
        GoogleRoot.do_gcloud_deploy_hasura(None)


def cli():
    cmd = GoogleRoot()
    cmd.cmdloop()


if __name__ == "__main__":
    cli()
