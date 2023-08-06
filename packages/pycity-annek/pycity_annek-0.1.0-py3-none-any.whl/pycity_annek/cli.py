""" Core module with cli """
import click, requests, sys, time, shutil, os
import xml.etree.ElementTree as xml
from requests.auth import HTTPBasicAuth


@click.group()
def pycity():
    """
    pycity is a CLI for making TeamCity API requests\n
    TC_USER = 'Your TeamCity username'\n
    TC_TOKEN = 'Your token'\n
    TC_SERVER = 'https://builds.example.com'\n

    Example Usage: pycity start-build EXAMPLE_BUILD_ID
    """


@pycity.command("check-env", short_help="Check required environment variables")
def check_env():
    """Prints out the current necessary environment variables"""
    tc_user = os.getenv("TC_USER")
    tc_token = os.getenv("TC_TOKEN")
    tc_server = os.getenv("TC_SERVER")
    print(f"Your environment has {tc_user} for the variable TC_USER")
    print(f"Your environment has {tc_token} for the variable TC_TOKEN")
    print(f"Your environment as {tc_server} for the variable TC_SERVER")


@pycity.command("start-build", short_help="Start build with default parameters")
@click.argument("configuration-identifier")
def start_build(configuration_identifier):
    """Starts a build with default parameters and returns the Build ID"""
    tc_user = os.getenv("TC_USER")
    tc_token = os.getenv("TC_TOKEN")
    tc_server = os.getenv("TC_SERVER")
    common_path = "httpAuth/app/rest"
    conf_id = configuration_identifier
    url = "{}/{}/buildQueue".format(tc_server, common_path)
    try:
        print("Starting a build with conf_id={}, POST url={}".format(conf_id, url))
        response = requests.post(
            url,
            auth=HTTPBasicAuth(tc_user, tc_token),
            data='<build><buildType id="{}"/></build>'.format(conf_id),
            headers={"Content-Type": "application/xml"},
        )
        print(f"Server http response is {response}")
        if "404" in str(response.content):
            print(f"Received 404, please check your configuration ID")
            sys.exit(1)
        xml_response = xml.fromstring(response.content)
        del response
    except requests.exceptions.RequestException:
        print("HTTP Request {} failed".format(url))
        exit(1)

    # get build id
    build_id = xml_response.attrib["id"]
    print("build_id={}".format(build_id))
    return build_id


@pycity.command("check-build-status", short_help="Check the status of a build")
@click.argument("build-identifier")
def check_build_status(build_identifier):
    """Checks the status of a build"""
    tc_user = os.getenv("TC_USER")
    tc_token = os.getenv("TC_TOKEN")
    tc_server = os.getenv("TC_SERVER")
    common_path = "httpAuth/app/rest"
    build_id = build_identifier
    url = "{}/{}/buildQueue".format(tc_server, common_path)
    url += "/id:{}".format(build_id)
    state = None
    status = None
    wait_time = 10
    try:
        print("Getting build status, build_id={}, POST url={}".format(build_id, url))
        response = requests.get(
            url,
            auth=HTTPBasicAuth(tc_user, tc_token),
            headers={"Content-Type": "application/xml"},
        )
        xml_response = xml.fromstring(response.content)
        del response
        state = xml_response.attrib["state"]
        if state == "queued":
            print("Another teamcity build already running or current build was queued.")
        else:
            status = xml_response.attrib["status"]
            print("Teamcity build status = {}, state = {}".format(status, state))
            if status == "UNKNOWN":
                print("Teamcity build was cancelled")
                exit(1)
            elif status == "SUCCESS":
                print("Teamcity build succeeded")
                exit(0)
    except requests.exceptions.RequestException:
        print("HTTP Request {} failed".format(url))
        exit(1)
