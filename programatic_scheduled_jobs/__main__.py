import yaml
import os
import math
import time
from kubernetes import client, config, watch

JOB_NAME = "scraper-malt"
NAMESPACE = "mongo-namespace"
IMAGE = "swanndolia/scraper-malt"
KUBE_CONFIG_PATH = os.path.expanduser('~/.kube/config')


def create_job_object(args):
    container = client.V1Container(
        name=JOB_NAME,
        image=IMAGE,
        volume_mounts=[client.V1VolumeMount(
            name="dshm", mount_path="/dev/shm")],
        command=["python3", "main.py"],
        args=args)
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={'name': JOB_NAME}),
        spec=client.V1PodSpec(restart_policy='OnFailure', containers=[container], volumes=[client.V1Volume(name="dshm", empty_dir={"medium": "Memory"})]))
    return(client.V1JobSpec(template=template))


def create_job(api_instance, job):
    api_response = api_instance.create_namespaced_job(
        body=job,
        namespace=NAMESPACE)
    print("Job created. status='%s'" % str(api_response.status))


if(__name__ == "__main__"):
    config.load_kube_config(KUBE_CONFIG_PATH)
    batch_v1 = client.BatchV1Api()

    with open(os.path.dirname(__file__) + '/techno.txt') as f:
        lines = f.readlines()
        start = 0
        end = 8
        for i in range(math.ceil(len(lines) / 8)):
            spec = create_job_object(lines[start:end])
            job = client.V1Job(
                api_version='batch/v1',
                kind='Job',
                metadata=client.V1ObjectMeta(name=JOB_NAME + "-" + str(start)),
                spec=spec)
            create_job(batch_v1, job)
            start += 8
            end += 8
