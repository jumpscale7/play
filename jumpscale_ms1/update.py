#fabric install script (not using jumpscale)

from fabric.api import *

@task
def js():
    """
    update jumpscale
    """
    run("jscode update -a jumpscale -r jp_jumpscale,jp_serverapps,jumpscale_core")


