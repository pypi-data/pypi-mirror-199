import collections

import pkg_resources
from dbdemos.packager import Packager

from .conf import DBClient, DemoConf, Conf, ConfTemplate, merge_dict, DemoNotebook
from .installer_report import InstallerReport
from .tracker import Tracker
from .notebook_parser import NotebookParser
from .installer_workflows import InstallerWorkflow
from .installer_repos import InstallerRepo
from pathlib import Path
import time
import json
import re
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import urllib
import threading

class Installer:
    def __init__(self, username = None, pat_token = None, workspace_url = None, cloud = "AWS", org_id: str = None):
        self.cloud = cloud
        self.dbutils = None
        if username is None:
            username = self.get_current_username()
        if workspace_url is None:
            workspace_url = self.get_current_url()
        if pat_token is None:
            pat_token = self.get_current_pat_token()
        if org_id is None:
            org_id = self.get_org_id()
        conf = Conf(username, workspace_url, org_id, pat_token)
        self.tracker = Tracker(org_id, self.get_uid())
        self.db = DBClient(conf)
        self.report = InstallerReport(self.db.conf.workspace_url)
        self.installer_workflow = InstallerWorkflow(self)
        self.installer_repo = InstallerRepo(self)


    #TODO replace with https://github.com/mlflow/mlflow/blob/master/mlflow/utils/databricks_utils.py#L64 ?
    def get_dbutils(self):
        if self.dbutils is None:
            from pyspark.sql import SparkSession
            spark = SparkSession.getActiveSession()
            if spark.conf.get("spark.databricks.service.client.enabled") == "true":
                from pyspark.dbutils import DBUtils
                self.dbutils = DBUtils(spark)
            else:
                import IPython
                self.dbutils = IPython.get_ipython().user_ns["dbutils"]
        return self.dbutils

    def get_current_url(self):
        try:
            return "https://"+self.get_dbutils().notebook.entry_point.getDbutils().notebook().getContext().browserHostName().get()
        except:
            return "local"

    def get_org_id(self):
        try:
            return self.get_dbutils().notebook.entry_point.getDbutils().notebook().getContext().tags().apply('orgId')
        except:
            return "local"

    def get_uid(self):
        try:
            return self.get_dbutils().notebook.entry_point.getDbutils().notebook().getContext().tags().apply('userId')
        except:
            return "local"

    def get_current_folder(self):
        try:
            current_notebook = self.get_dbutils().notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
            return current_notebook[:current_notebook.rfind("/")]
        except:
            return "local"

    def get_workspace_id(self):
        try:
            return self.get_dbutils().notebook.entry_point.getDbutils().notebook().getContext().workspaceId().get()
        except:
            return "local"

    def get_current_pat_token(self):
        try:
            token = self.get_dbutils().notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
        except:
            return "local"
        if len(token) == 0:
            raise Exception("Couldn't get a token to call Databricks API to create demo resources. " +
                            "This is likely due to legacy cluster being used with admin protection for “No isolation shared” https://docs.databricks.com/administration-guide/account-settings/no-isolation-shared.html (account level setting)." +
                            "\nPlease use a cluser with Access mode set to Isolation to Single User or Shared instead and re-run your dbdemos command.")
        return token

    def get_current_username(self):
        try:
            return self.get_dbutils().notebook.entry_point.getDbutils().notebook().getContext().tags().apply('user')
        except:
            return "local"

    def get_current_cloud(self):
        try:
            hostname = self.get_dbutils().notebook.entry_point.getDbutils().notebook().getContext().browserHostName().get()
        except:
            print(f"WARNING: Can't get cloud from dbutils. Fallback to default local cloud {self.cloud}")
            return self.cloud
        if "gcp" in hostname:
            return "GCP"
        elif "azure" in hostname:
            return "AZURE"
        else:
            return "AWS"


    def check_demo_name(self, demo_name):
        demo_availables = self.get_demos_available()
        # TODO: where should we store the bundle, as .zip in the wheel and extract them locally?
        if demo_name not in demo_availables:
            demos = '\n  - '.join(demo_availables)
            raise Exception(f"The demo {demo_name} doesn't exist. \nDemos currently available: \n  - {demos}")

    def get_demos_available(self):
        return set(pkg_resources.resource_listdir("dbdemos", "bundles"))

    def get_demo_conf(self, demo_name:str, demo_folder: str = ""):
        demo = self.get_resource(f"bundles/{demo_name}/conf.json")
        conf_template = ConfTemplate(self.db.conf.username, demo_name, demo_folder)
        return DemoConf(demo_name, json.loads(conf_template.replace_template_key(demo)))

    def get_resource(self, path):
        return pkg_resources.resource_string("dbdemos", path).decode('UTF-8')

    def test_standard_pricing(self):
        w = self.db.get("2.0/sq/config/warehouses", {"limit": 1})
        if "error_code" in w and w["error_code"] == "FEATURE_DISABLED":
            raise Exception(f"ERROR: DBSQL isn't available in this workspace. Only Premium workspaces are supported - {w}")


    def install_demo(self, demo_name, install_path, overwrite=False, update_cluster_if_exists = True, skip_dashboards = False, start_cluster = True):
        # first get the demo conf.
        if install_path is None:
            install_path = self.get_current_folder()
        elif install_path.startswith("./"):
            install_path = self.get_current_folder()+"/"+install_path[2:]
        elif not install_path.startswith("/"):
            install_path = self.get_current_folder()+"/"+install_path
        if install_path.endswith("/"):
            install_path = install_path[:-1]
        print(f"Installing demo {demo_name} under {install_path}...")
        self.check_demo_name(demo_name)
        demo_conf = self.get_demo_conf(demo_name, install_path+"/"+demo_name)
        self.tracker.track_install(demo_conf.category, demo_name)
        self.get_current_username()
        cluster_id, cluster_name = self.load_demo_cluster(demo_name, demo_conf, update_cluster_if_exists, start_cluster)
        pipeline_ids = self.load_demo_pipelines(demo_name, demo_conf)
        dashboards = [] if skip_dashboards else self.install_dashboards(demo_conf, install_path)
        repos = self.installer_repo.install_repos(demo_conf)
        workflows = self.installer_workflow.install_workflows(demo_conf)
        notebooks = self.install_notebooks(demo_name, install_path, demo_conf, cluster_name, cluster_id, pipeline_ids, dashboards, workflows, repos, overwrite)
        job_id, run_id = self.installer_workflow.start_demo_init_job(demo_conf)
        for pipeline in pipeline_ids:
            if pipeline["run_after_creation"]:
                self.db.post(f"2.0/pipelines/{pipeline['uid']}/updates", { "full_refresh": True })

        self.report.display_install_result(demo_name, demo_conf.description, demo_conf.title, install_path, notebooks, job_id, run_id, cluster_id, cluster_name, pipeline_ids, dashboards, workflows)

    def install_dashboards(self, demo_conf: DemoConf, install_path):
        if "dashboards" in pkg_resources.resource_listdir("dbdemos", "bundles/"+demo_conf.name):
            print(f'    Installing dashboards')
            def install_dash(dashboard):
                return self.install_dashboard(demo_conf, install_path, dashboard)
            dashboards = pkg_resources.resource_listdir("dbdemos", "bundles/" + demo_conf.name + "/dashboards")
            #filter out new import/export api:
            dashboards = filter(lambda n: Packager.DASHBOARD_IMPORT_API not in n, dashboards)
            # Parallelize dashboard install, 3 by 3.
            with ThreadPoolExecutor(max_workers=3) as executor:
                return [n for n in executor.map(install_dash, dashboards)]
        return []

    def install_dashboard(self, demo_conf, install_path, dashboard):
        definition = json.loads(self.get_resource("bundles/" + demo_conf.name + "/dashboards/" + dashboard))
        id = dashboard[:dashboard.rfind(".json")]
        dashboard_name = definition['dashboard']['name']
        print(f"     Installing dashboard {dashboard_name} - {id}...")
        from dbsqlclone.utils import dump_dashboard
        from dbsqlclone.utils.client import Client
        client = Client(self.db.conf.workspace_url, self.db.conf.pat_token)
        existing_dashboard = self.get_dashboard_by_name(dashboard_name)
        if existing_dashboard is not None:
            existing_dashboard = dump_dashboard.get_dashboard_definition_by_id(client, existing_dashboard['id'])
            # If we can't change the ownership, we'll have to create a new dashboard.
            could_change_owner_changed = self.change_dashboard_ownership(existing_dashboard)
            # Can't change ownership, we won't be able to override the dashboard. Create a new one with your name.
            if not could_change_owner_changed:
                name = self.db.conf.username[:self.db.conf.username.rfind('@')]
                name = re.sub("[^A-Za-z0-9]", '_', name)
                dashboard_name = dashboard_name + " - " + name
                #TODO: legacy import/export
                definition['name'] = dashboard_name
                #definition['dashboard']['name'] = dashboard_name
                print(
                    f"     Could not change ownership. Searching dashboard with current username instead: {dashboard_name}")
                existing_dashboard = self.get_dashboard_by_name(dashboard_name)
                if existing_dashboard is not None:
                    existing_dashboard = dump_dashboard.get_dashboard_definition_by_id(client, existing_dashboard['id'])
        # Create the folder where to save the queries
        path = f'{install_path}/dbdemos_dashboards/{demo_conf.name}'
        f = self.db.post("2.0/workspace/mkdirs", {"path": path})
        if "error_code" in f:
            raise Exception(f"ERROR - wrong install path, can't save dashboard here: {f}")
        folders = self.db.get("2.0/workspace/list", {"path": Path(path).parent.absolute()})
        if "error_code" in folders:
            raise Exception(f"ERROR - wrong install path, can't save dashboard here: {folders}")
        parent_folder_id = None
        for f in folders["objects"]:
            if f["object_type"] == "DIRECTORY" and f["path"] == path:
                parent_folder_id = f["object_id"]
        if parent_folder_id is None:
            print(f"ERROR: couldn't find dashboard folder {path}. Do you have permission?")

        # ------- LEGACY IMPORT/EXPORT DASHBOARD - TO BE REPLACED ONCE IMPORT/EXPORT API IS PUBLIC PREVIEW
        from dbsqlclone.utils.client import Client
        from dbsqlclone.utils import load_dashboard, clone_dashboard
        client = Client(self.db.conf.workspace_url, self.db.conf.pat_token, permissions= [
            {"user_name": self.db.conf.username, "permission_level": "CAN_MANAGE"},
            {"group_name": "users", "permission_level": "CAN_EDIT"}
        ])
        try:
            endpoint = self.get_or_create_endpoint(self.db.conf.name)
            if endpoint is None:
                print(
                    "ERROR: couldn't create or get a SQL endpoint for dbdemos. Do you have permission? Trying to import the dashboard without endoint (import will pick the first available if any)")
            else:
                client.data_source_id = endpoint['id']
            if existing_dashboard is not None:
                load_dashboard.clone_dashboard_without_saved_state(definition, client, existing_dashboard['id'], parent=f'folders/{parent_folder_id}')
                return {"id": id, "name": dashboard_name, "installed_id": existing_dashboard['id']}
            else:
                state = load_dashboard.clone_dashboard(definition, client, {}, parent=f'folders/{parent_folder_id}')
                return {"id": id, "name": dashboard_name, "installed_id": state["new_id"]}
        except Exception as e:
            print(f"    ERROR loading dashboard {dashboard_name} - {str(e)}")
            raise e
            return {"id": id, "name": dashboard_name, "error": str(e), "existing_dashboard": existing_dashboard['id']}

        """
        # ------- NEW IMPORT/EXPORT API
        data = {
            'import_file_contents': definition,
            'parent': f'folders/{parent_folder_id}'
        }
        endpoint_id = self.get_or_create_endpoint()
        if endpoint_id is None:
            print(
                "ERROR: couldn't create or get a SQL endpoint for dbdemos. Do you have permission? Trying to import the dashboard without endoint (import will pick the first available if any)")
        else:
            data['warehouse_id'] = endpoint_id
        if existing_dashboard is not None:
            data['overwrite_dashboard_id'] = existing_dashboard
            data['should_overwrite_existing_queries'] = True
        
        TODO: import / export public preview delayed. Instead we'll fallback to manual import/export
        i = self.db.post(f"2.0/preview/sql/dashboards/import", data)
        if "id" in i:
            # Change definition for all users to be able to use the dashboard & the queries.
            permissions = {"access_control_list": [
                {"user_name": self.db.conf.username, "permission_level": "CAN_MANAGE"},
                {"group_name": "users", "permission_level": "CAN_EDIT"}
            ]}
            permissions = self.db.post("2.0/preview/sql/permissions/dashboards/" + i["id"], permissions)
            existing_dashboard_definition = self.db.get(f"2.0/preview/sql/dashboards/{existing_dashboard}/export")
            if "queries" in existing_dashboard_definition:
                for q in existing_dashboard_definition["queries"]:
                    self.db.post(f"2.0/preview/sql/permissions/query/{q['id']}", permissions)
            print(f"     Dashboard {definition['dashboard']['name']} installed. Permissions set to {permissions}")
            self.db.post("2.0/preview/sql/dashboards/" + i["id"], {"run_as_role": "viewer"})
            return {"id": id, "name": definition['dashboard']['name'], "installed_id": i["id"]}
        else:
            print(f"    ERROR loading dashboard {definition['dashboard']['name']}: {i}, {existing_dashboard}")
            return {"id": id, "name": definition['dashboard']['name'], "error": i, "installed_id": existing_dashboard}"""

    # Try to change ownership to be able to override the dashboard. Only admin can override ownership.
    # Return True if we've been able to change ownership, false otherwise
    def change_dashboard_ownership(self, existing_dashboard):
        owner = self.db.post(f"2.0/preview/sql/permissions/dashboard/{existing_dashboard['id']}/transfer", {"new_owner": self.db.conf.username})
        if 'error_code' in owner or ('message' in owner and (owner['message'] != 'Success' and not owner['message'].startswith("This object already belongs"))):
            print(f"       WARN: Couldn't update ownership of dashboard {existing_dashboard['id']} to current user. Will create a new one.")
            return False
        # Get existing dashboard definition and change all its query ownership
        # TODO legacy import/export
        # existing_dashboard_definition = self.db.get(f"2.0/preview/sql/dashboards/{existing_dashboard_id}/export")
        # if "message" in existing_dashboard_definition:
        #     print(f"WARN: Error getting existing dashboard details - id {existing_dashboard['id']}: {existing_dashboard_definition}. Will create a new one.")
        #    return False
        # else:
        # Try to update all individual query ownership
        for q in existing_dashboard["queries"]:
            owner = self.db.post(f"2.0/preview/sql/permissions/query/{q['id']}/transfer", {"new_owner": self.db.conf.username})
            if 'error_code' in owner:
                print(f"       WARN: Couldn't update ownership of query {q['id']} to current user. Will create a new dashboard.")
                return False
        return True

    def get_dashboard_by_name(self, name):
        def get_dashboard(page):
            page_size = 250
            ds = self.db.get("2.0/preview/sql/dashboards", params = {"page_size": page_size, "page": page})
            for d in ds['results']:
                if d['name'] == name and 'moved_to_trash_at' not in d:
                    return d
            if len(ds["results"]) >= page_size:
                return get_dashboard(page+1)
            return None
        return get_dashboard(1)

    def get_demo_datasource(self):
        data_sources = self.db.get("2.0/preview/sql/data_sources")
        for source in data_sources:
            if source['name'] == "dbdemos-shared-endpoint":
                return source
        #Try to fallback to an existing shared endpoint.
        for source in data_sources:
            if "shared-sql-endpoint" in source['name'].lower():
                return source
        for source in data_sources:
            if "shared" in source['name'].lower():
                return source
        return None

    def get_or_create_endpoint(self, username, endpoint_name = "dbdemos-shared-endpoint"):
        ds = self.get_demo_datasource()
        if ds is not None:
            return ds
        def get_definition(serverless, name):
            return {
                "name": name,
                "cluster_size": "Small",
                "min_num_clusters": 1,
                "max_num_clusters": 1,
                "tags": {
                    "project": "dbdemos"
                },
                "spot_instance_policy": "COST_OPTIMIZED",
                "enable_photon": "true",
                "enable_serverless_compute": serverless,
                "channel": { "name": "CHANNEL_NAME_CURRENT" }
            }
        def try_create_endpoint(serverless):
            w = self.db.post("2.0/sql/warehouses", json=get_definition(serverless, endpoint_name))
            if "message" in w and "already exists" in w['message']:
                w = self.db.post("2.0/sql/warehouses", json=get_definition(serverless, endpoint_name+"-"+username))
            if "id" in w:
                return w
            print(f"WARN: Couldn't create endpoint with serverless = {endpoint_name} and endpoint name: {endpoint_name} and {endpoint_name}-{username}. Creation response: {w}")
            return None

        if try_create_endpoint(True) is None:
            #Try to fallback with classic endpoint?
            try_create_endpoint(False)
        ds = self.get_demo_datasource()
        if ds is not None:
            return ds
        print(f"ERROR: Couldn't create endpoint.")
        return None

    def install_notebooks(self, demo_name: str, install_path: str, demo_conf: DemoConf, cluster_name: str, cluster_id: str, pipeline_ids, dashboards, workflows, repos, overwrite=False):
        assert len(demo_name) > 4, "wrong demo name. Fail to prevent potential delete errors."
        print(f'    Installing notebooks')
        install_path = install_path+"/"+demo_name
        s = self.db.get("2.0/workspace/get-status", {"path": install_path})
        if 'object_type' in s:
            if not overwrite:
                if self.report.displayHTML_available():
                    from dbruntime.display import displayHTML
                    displayHTML(f"""{InstallerReport.CSS_REPORT}<div class="dbdemos_install">
                      <h1 style="color: red">Error!</h1>
                      <bold>Folder {install_path} isn't empty</bold>. Please install demo with overwrite=True to replace the existing content: 
                      <div class="code">
                              dbdemos.install('{demo_name}', overwrite=True)
                      </div>
                    </div>""")
                raise Exception(f"Folder {install_path} isn't empty. Please install demo with overwrite=True to replace the existing content")
            print(f"    Folder {install_path} already exists. Deleting the existing content...")
            d = self.db.post("2.0/workspace/delete", {"path": install_path, 'recursive': True})
            if 'error_code' in d:
                raise Exception(f"Couldn't erase folder {install_path}. Do you have permission? Error: {d}")

        folders_created = set()
        #Avoid multiple mkdirs in parallel as it's creating error.
        folders_created_lock = threading.Lock()
        def load_notebook(notebook):
            return load_notebook_path(notebook, "bundles/"+demo_name+"/install_package/"+notebook.get_clean_path()+".html")

        def load_notebook_path(notebook: DemoNotebook, template_path):
            parser = NotebookParser(self.get_resource(template_path))
            if notebook.add_cluster_setup_cell:
                self.add_cluster_setup_cell(parser, demo_name, cluster_name, cluster_id, self.db.conf.workspace_url)
            parser.replace_dashboard_links(dashboards)
            parser.remove_automl_result_links()
            parser.replace_dynamic_links_pipeline(pipeline_ids)
            parser.replace_dynamic_links_repo(repos)
            parser.replace_dynamic_links_workflow(workflows)
            parser.set_tracker_tag(self.get_org_id(), self.get_uid(), demo_conf.category, demo_name, notebook.get_clean_path())
            content = parser.get_html()
            content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
            parent = str(Path(install_path+"/"+notebook.get_clean_path()).parent)
            with folders_created_lock:
                if parent not in folders_created:
                    r = self.db.post("2.0/workspace/mkdirs", {"path": parent})
                    folders_created.add(parent)
                    if 'error_code' in r:
                        if r['error_code'] == "RESOURCE_ALREADY_EXISTS":
                            print(f"ERROR: A folder already exists under {install_path}. Add the overwrite option to replace the content:")
                            print(f"dbdemos.install('{demo_name}', overwrite=True)")
                        raise Exception(f"Couldn't create folder under {install_path}. Import error: {r}")
            r = self.db.post("2.0/workspace/import", {"path": install_path+"/"+notebook.get_clean_path(), "content": content, "format": "HTML"})
            if 'error_code' in r:
                raise Exception(f"Couldn't install demo under {install_path}/{notebook.get_clean_path()}. Do you have permission?. Import error: {r}")
            return notebook

        #Always adds the licence notebooks
        with ThreadPoolExecutor(max_workers=3) as executor:
            notebooks = [
                DemoNotebook("_resources/LICENSE", "LICENSE", "Demo License"),
                DemoNotebook("_resources/NOTICE", "NOTICE", "Demo Notice"),
                DemoNotebook("_resources/README", "README", "Readme")
            ]
            def load_notebook_templet(notebook):
                load_notebook_path(notebook, f"template/{notebook.title}.html")
            collections.deque(executor.map(load_notebook_templet, notebooks))
        with ThreadPoolExecutor(max_workers=3) as executor:
            return [n for n in executor.map(load_notebook, demo_conf.notebooks)]


    def load_demo_pipelines(self, demo_name, demo_conf: DemoConf):
        #default cluster conf
        pipeline_ids = []
        for pipeline in demo_conf.pipelines:
            definition = pipeline["definition"]
            today = date.today().strftime("%Y-%m-%d")
            #enforce demo tagging in the cluster
            for cluster in definition["clusters"]:
                merge_dict(cluster, {"custom_tags": {"project": "dbdemos", "demo": demo_name, "demo_install_date": today}})
            existing_pipeline = self.get_pipeline(definition["name"])
            print(f'    Installing pipeline {definition["name"]}')
            if existing_pipeline == None:
                p = self.db.post("2.0/pipelines", definition)
                if 'error_code' in p and p['error_code'] == 'FEATURE_DISABLED':
                    message = f'ERROR: DLT pipelines are not available in this workspace. Only Premium workspaces are supported on Azure - {p}'
                    raise Exception(message)
                if 'error_code' in p:
                    raise Exception(f"Error creating the DLT pipeline: {p['message']} {p}")
                id = p['pipeline_id']
            else:
                print("    Updating existing pipeline with last configuration")
                id = existing_pipeline['pipeline_id']
                self.db.put("2.0/pipelines/"+id, definition)
            pipeline_ids.append({"name": definition['name'], "uid": id, "id": pipeline["id"], "run_after_creation": pipeline["run_after_creation"] or existing_pipeline is not None})
            #Update the demo conf tags {{}} with the actual id (to be loaded as a job for example)
            demo_conf.set_pipeline_id(pipeline["id"], id)
        return pipeline_ids

    def load_demo_cluster(self, demo_name, demo_conf: DemoConf, update_cluster_if_exists, start_cluster = True):
        #Do not start clusters by default in Databricks FE clusters to avoid costs as we have shared clusters for demos
        if start_cluster is None:
            start_cluster = not (self.db.conf.is_dev_env() or self.db.conf.is_fe_env())

        #default cluster conf
        conf_template = ConfTemplate(self.db.conf.username, demo_name)
        cluster_conf = self.get_resource("resources/default_cluster_config.json")
        cluster_conf = json.loads(conf_template.replace_template_key(cluster_conf))
        #add cloud specific setup
        cloud = self.get_current_cloud()
        cluster_conf_cloud = self.get_resource(f"resources/default_cluster_config-{cloud}.json")
        cluster_conf_cloud = json.loads(conf_template.replace_template_key(cluster_conf_cloud))
        merge_dict(cluster_conf, cluster_conf_cloud)
        merge_dict(cluster_conf, demo_conf.cluster)
        if "spark.databricks.cluster.profile" in cluster_conf["spark_conf"] and cluster_conf["spark_conf"]["spark.databricks.cluster.profile"] == "singleNode":
            del cluster_conf["autoscale"]
            cluster_conf["num_workers"] = 0

        existing_cluster = self.find_cluster(cluster_conf["cluster_name"])
        if existing_cluster == None:
            cluster = self.db.post("2.0/clusters/create", json = cluster_conf)
            if "cluster_id" not in cluster:
                print(f"    WARN: couldn't create the cluster for the demo: {cluster}")
                return "CLUSTER_CREATION_ERROR", "CLUSTER_CREATION_ERROR"
            else:
                cluster_conf["cluster_id"] = cluster["cluster_id"]
        else:
            cluster_conf["cluster_id"] = existing_cluster["cluster_id"]
            if update_cluster_if_exists:
                cluster = self.db.post("2.0/clusters/edit", json = cluster_conf)
                if "error_code" in cluster and cluster["error_code"] == "INVALID_STATE":
                    print(f"    Demo cluster {cluster_conf['cluster_name']} in invalid state. Stopping it...")
                    cluster = self.db.post("2.0/clusters/delete", json = {"cluster_id": cluster_conf["cluster_id"]})
                    i = 0
                    while i < 30:
                        i += 1
                        cluster = self.db.get("2.0/clusters/get", params = {"cluster_id": cluster_conf["cluster_id"]})
                        if cluster["state"] == "TERMINATED":
                            print("    Cluster properly stopped.")
                            break
                        time.sleep(2)
                    if cluster["state"] != "TERMINATED":
                        print(f"    WARNING: Couldn't stop the demo cluster properly. Unknown state. Please stop your cluster {cluster_conf['cluster_name']} before.")
                    self.db.post("2.0/clusters/edit", json = cluster_conf)
            if start_cluster:
                self.db.post("2.0/clusters/start", json = cluster_conf)
        return cluster_conf['cluster_id'], cluster_conf['cluster_name']

    #return the cluster with the given name or none
    def find_cluster(self, cluster_name):
        clusters = self.db.get("2.0/clusters/list")
        if "clusters" in clusters:
            for c in clusters["clusters"]:
                if c["cluster_name"] == cluster_name:
                    return c
        return None

    def get_pipeline(self, name):
        def get_pipelines(token = None):
            r = self.db.get("2.0/pipelines", {"max_results": 100, "page_token": token})
            if "statuses" in r:
                for p in r["statuses"]:
                    if p["name"] == name:
                        return p
            if "next_page_token" in r:
                return get_pipelines(r["next_page_token"])
            return None
        return get_pipelines()


    def add_cluster_setup_cell(self, parser: NotebookParser, demo_name, cluster_name, cluster_id, env_url):
        content = """%md \n### A cluster has been created for this demo\nTo run this demo, just select the cluster `{{CLUSTER_NAME}}` from the dropdown menu ([open cluster configuration]({{ENV_URL}}/#setting/clusters/{{CLUSTER_ID}}/configuration)). <br />\n*Note: If the cluster was deleted after 30 days, you can re-create it with `dbdemos.create_cluster('{{DEMO_NAME}}')` or re-install the demo: `dbdemos.install('{{DEMO_NAME}}')`*"""
        content = content.replace("{{DEMO_NAME}}", demo_name) \
            .replace("{{ENV_URL}}", env_url) \
            .replace("{{CLUSTER_NAME}}", cluster_name) \
            .replace("{{CLUSTER_ID}}", cluster_id)
        parser.add_extra_cell(content)

    def add_extra_cell(self, html, cell_content, position = 0):
        command = {
            "version": "CommandV1",
            "subtype": "command",
            "commandType": "auto",
            "position": 1,
            "command": cell_content
        }
        raw_content, content = self.get_notebook_content(html)
        content = json.loads(urllib.parse.unquote(content))
        content["commands"].insert(position, command)
        content = urllib.parse.quote(json.dumps(content), safe="()*''")
        return html.replace(raw_content, base64.b64encode(content.encode('utf-8')).decode('utf-8'))

    def get_notebook_content(self, html):
        match = re.search(r'__DATABRICKS_NOTEBOOK_MODEL = \'(.*?)\'', html)
        raw_content = match.group(1)
        return raw_content, base64.b64decode(raw_content).decode('utf-8')