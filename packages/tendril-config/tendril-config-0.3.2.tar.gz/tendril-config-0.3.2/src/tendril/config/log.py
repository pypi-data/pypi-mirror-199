# Copyright (C) 2022 Chintalagiri Shashank
#
# This file is part of EBS API Server.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Logging Configuration Options
=============================
"""


from tendril.utils.config import ConfigOption

import logging
logger = logging.getLogger(__name__)

depends = ['tendril.config.core']


config_elements_log = [
    ConfigOption(
        'LOG_LEVEL', "'INFO'",
        "The logging level to use.",
        parser=logging.getLevelName
    ),
    ConfigOption(
        'JSON_LOGS', "''",
        "Whether to use JSON logging.",
        parser=bool
    ),
    ConfigOption(
        'LOG_PATH', "os.path.join('/var/log', 'tendril', '{}.log'.format(INSTANCE_NAME))",
        "Full path (including filename) to write logs to.",
    ),
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_elements(config_elements_log,
                          doc="Tendril Server Logging Configuration")
    from tendril.utils import log
    log.apply_config(manager)

