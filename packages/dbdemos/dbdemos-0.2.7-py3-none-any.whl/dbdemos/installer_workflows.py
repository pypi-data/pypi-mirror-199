from .conf import DemoConf, merge_dict, ConfTemplate
import json
import time

class InstallerWorkflow:
    def __init__(self, installer):
        self.installer = installer
        self.db = installer.db

    #Start the init job if it exists
    def install_workflows(self, demo_conf: DemoConf):
        workflows = []
        if len(demo_conf.workflows) > 0:
            print(f"    Loading demo workflows")
            #We have an init jon
            for workflow in demo_conf.workflows:
                definition = workflow['definition']
                job_name = definition["settings"]["name"]
                #add cloud specific setup
                job_id, run_id = self.create_or_replace_job(demo_conf.name, definition, job_name, workflow['start_on_install'])
                print(f"    Demo workflow available: {self.installer.db.conf.workspace_url}/#job/{job_id}/run/{run_id}")
                workflows.append({"uid": job_id, "run_id": run_id, "id": workflow['id']})
        return workflows

    #Start the init job if it exists
    def start_demo_init_job(self, demo_conf: DemoConf):
        if "settings" in demo_conf.init_job:
            job_name = demo_conf.init_job["settings"]["name"]
            print(f"    Searching for existing demo initialisation job {job_name}")
            #We have an init json
            job_id, run_id = self.create_or_replace_job(demo_conf.name, demo_conf.init_job, job_name, True)
            return job_id, run_id
        return None, None


    def create_or_replace_job(self, demo_name: str, definition: dict,  job_name: str, run_now: bool):
        cloud = self.installer.get_current_cloud()
        conf_template = ConfTemplate(self.db.conf.username, demo_name)
        cluster_conf = self.installer.get_resource("resources/default_cluster_job_config.json")
        cluster_conf = json.loads(conf_template.replace_template_key(cluster_conf))
        cluster_conf_cloud = json.loads(self.installer.get_resource(f"resources/default_cluster_config-{cloud}.json"))
        merge_dict(cluster_conf, cluster_conf_cloud)
        definition = self.replace_warehouse_id(definition)
        for cluster in definition["settings"]["job_clusters"]:
            if "new_cluster" in cluster:
                merge_dict(cluster["new_cluster"], cluster_conf)
                #Let's make sure we add our dev pool for faster startup
                if self.db.conf.is_dev_env():
                    cluster["new_cluster"]["instance_pool_id"] = "0213-111033-rowed79-pool-zb80houq"
                    if "node_type_id" in cluster["new_cluster"]: del cluster["new_cluster"]["node_type_id"]
                    if "enable_elastic_disk" in cluster["new_cluster"]: del cluster["new_cluster"]["enable_elastic_disk"]
                    if "aws_attributes" in cluster["new_cluster"]: del cluster["new_cluster"]["aws_attributes"]
        existing_job = self.installer.db.find_job(job_name)
        if existing_job is not None:
            job_id = existing_job["job_id"]
            self.installer.db.post("/2.1/jobs/runs/cancel-all", {"job_id": job_id})
            self.wait_for_run_completion(job_id)
            print("    Updating existing job")
            r = self.installer.db.post("2.1/jobs/reset", {"job_id": job_id, "new_settings": definition["settings"]})
            if "error_code" in r:
                raise Exception(
                    f'ERROR setting up init job, do you have permission? please check job definition {r}, {definition["settings"]}')
        else:
            print("    Creating a new job for demo initialization (data & table setup).")
            r_jobs = self.installer.db.post("2.1/jobs/create", definition["settings"])
            if "error_code" in r_jobs:
                raise Exception(f'error setting up job, please check job definition {r_jobs}, {definition["settings"]}')
            job_id = r_jobs["job_id"]
        if run_now:
            j = self.installer.db.post("2.1/jobs/run-now", {"job_id": job_id})
            return job_id, j['run_id']
        return job_id, None

    def replace_warehouse_id(self, definition):
        # Jobs need a warehouse ID. Let's replace it with the one created. TODO: should be in the template?
        if "{{SHARED_WAREHOUSE_ID}}" in json.dumps(definition):
            endpoint = self.installer.get_or_create_endpoint(self.db.conf.name)
            if endpoint is None:
                print(
                    "ERROR: couldn't create or get a SQL endpoint for dbdemos. Do you have permission? Your workflow won't be able to execute the task.")
                #TODO: quick & dirty, need to improve
                definition = json.loads(json.dumps(definition).replace(""", "warehouse_id": "{{SHARED_WAREHOUSE_ID}}"}""", ""))
            else:
                definition = json.loads(json.dumps(definition).replace("{{SHARED_WAREHOUSE_ID}}", endpoint['warehouse_id']))
        return definition

    def wait_for_run_completion(self, job_id, max_retry=10):
        def is_still_running(job_id):
            runs = self.installer.db.get("2.1/jobs/runs/list", {"job_id": job_id, "active_only": "true"})
            return "runs" in runs and len(runs["runs"]) > 0
        i = 0
        while i <= max_retry and is_still_running(job_id):
            print(f"      A run is still running for job {job_id}, waiting for termination...")
            time.sleep(5)