#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# author        : JV-conseil
# credits       : JV-conseil
# copyright     : Copyright (c) 2019-2023 JV-conseil
#                 All rights reserved
# ====================================================

import glob
import logging
import os
import re
from functools import cached_property, lru_cache
from pathlib import Path
from string import Template

import joblib
from unidecode import unidecode

from .constants import UNAVAILABLE_GHOSTS

" Logger "
logger = logging.getLogger(__name__)


class AllowedGhosts:
    "Daily inspiration for ALLOWED_HOSTS values"

    def __init__(
        self,
        file_format=["*.txt"],
    ) -> int:
        root = Path(__file__).resolve().parent
        self.file_format = file_format
        self.file_dump = os.path.join(root, "README.md")
        self.filter = ["editar"]
        self.hostname_template = "app-$ghost.cloud.sdu.dk"
        self.src = os.path.join(root, "src")
        self._joblib_cache = os.path.join(root, "_cache.joblib")

    @cached_property
    def lines(self, *args, **kwargs) -> list:
        "lines"
        output = []
        try:
            os.chdir(self.src)

            for file, ext in [
                (file, ext) for ext in self.file_format for file in glob.glob(ext)
            ]:
                with open(file) as f:
                    output = f.readlines()
        except Exception as e:
            logger.exception(e)
        logger.debug("lines: %s", output)
        return output

    @staticmethod
    @lru_cache
    def clean_txt(txt: str) -> str:
        "clean_txt"
        output = ""
        try:
            txt = txt.lower()
            txt = unidecode(txt)
            txt = re.sub(r"[0-9]+ - ", " ", txt)
            txt = re.sub(r"[^a-z,;(.-]+", " ", txt)
            txt, *_ = re.split(r"[^a-z ]", txt)
            txt = re.sub(r"\s+", " ", txt)
            txt = txt.strip()
            if txt:
                output = txt
        except Exception as e:
            logger.exception(e)
        logger.debug("clean_txt: %s --> %s", txt, output)
        return output

    @lru_cache
    def exclude(self, txt: str) -> str:
        "exclude"
        output = txt
        try:
            if any(ex in txt for ex in self.filter):
                output = ""
        except Exception as e:
            logger.exception(e)
        logger.debug("exclude: %s --> %s", txt, output)
        return output

    @lru_cache
    def to_hostname(self, txt: str) -> str:
        "to_hostname"
        output = ""
        try:
            txt = re.sub(r"[^a-z]+", "-", txt)
            if txt:
                output = Template(self.hostname_template).substitute(ghost=txt)
        except Exception as e:
            logger.exception(e)
        logger.debug("to_hostname: %s --> %s", txt, output)
        return output

    @lru_cache
    def parser(self, txt: str) -> str:
        "parser"
        output = ""
        try:
            for do in [self.clean_txt, self.exclude, self.to_hostname]:
                txt = do(txt)
            if txt:
                output = txt
        except Exception as e:
            logger.exception(e)
        logger.debug("parser: %s --> %s", txt, output)
        return output

    @staticmethod
    def to_markdown(data: list, *args, **kwargs) -> str:
        "to_markdown"
        output = ""
        try:
            if data:
                _data = [f"1. {gh}" for gh in data]
                _data = ["# Allowed Ghosts 👻", ""] + _data + [""]
                output = "\n".join(_data)
        except Exception as e:
            logger.exception(e)
        logger.debug("to_markdown: %s", output)
        return output

    def dump_markdown(self, data: list, *args, **kwargs) -> str:
        "dump_markdown"
        output = ""
        try:
            output = self.to_markdown(data)
            with open(self.file_dump, "wt", encoding="UTF-8") as file:
                file.write(output)
                file.close()
        except Exception as e:
            logger.exception(e)
        logger.debug("dump_markdown: %s", output)
        return output

    def run(self, *args, **kwargs) -> list:
        "run"
        output = []
        try:
            for line in self.lines:
                ghost = self.parser(line)
                if "guerra" in ghost:
                    print(
                        ghost,
                        self.to_hostname(ghost),
                        self.to_hostname(ghost) in UNAVAILABLE_GHOSTS,
                    )
                if not ghost or ghost in output or ghost in UNAVAILABLE_GHOSTS:
                    continue
                output += [ghost]
            if output:
                joblib.dump(output, self._joblib_cache, compress=True)
                self.dump_markdown(output)
        except Exception as e:
            logger.exception(e)
        # logger.debug("run: %s", output)
        return output

    @cached_property
    def list(self, *args, **kwargs) -> list:
        "list"
        output = []
        try:
            output = joblib.load(self._joblib_cache)
        except FileNotFoundError:
            output = self.run()
        except Exception as e:
            logger.exception(e)
        # logger.debug("run: %s", output)
        return output

    def __call__(self, *args, **kwargs) -> int:
        return self.list


ALLOWED_GHOSTS = AllowedGhosts().list
