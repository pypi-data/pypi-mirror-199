#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# author        : JV-conseil
# credits       : JV-conseil
# copyright     : Copyright (c) 2019-2023 JV-conseil
#                 All rights reserved
# ====================================================

import logging

from allowed_ghosts.main import AllowedGhosts
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

" Logger "
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    process_name = "Allowed Ghosts"
    help = "Regenerate list"

    def launch_message(self, *args, **kwargs) -> str:
        "Startup message"
        launch = ""
        try:
            launch = "You have initiated {} command".format(self.process_name)
            dsh = "-" * len(launch)
            launch = "\n{d}\n{s}\n{d}\n".format(d=dsh, s=launch)
            for k, v in kwargs.items():
                launch += "- {}: {}\n".format(k, v)
            self.stdout.write(self.style.SUCCESS(launch))
        except Exception as e:
            logger.exception(e)
        return launch

    def run_processes(self, *args, **kwargs):
        "Processes to run"
        try:
            AllowedGhosts().run()
        except Exception as e:
            logger.exception(e)

    def handle(self, *args, **kwargs):
        "Processes to run"
        try:
            start = timezone.now()

            " Launch "
            self.launch_message(*args, **kwargs)

            " Processes to run "
            self.run_processes(self, *args, **kwargs)

            " Message "
            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully run %s in %s"
                    % (self.process_name, timezone.now() - start)
                )
            )
        except Exception as e:
            logger.exception(e)
            raise CommandError("Error while running %s" % self.process_name)
