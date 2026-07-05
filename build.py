from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")

name = "employee-management"
version = "1.0"

@init
def initialize(project):
    project.build_depends_on("flask")
