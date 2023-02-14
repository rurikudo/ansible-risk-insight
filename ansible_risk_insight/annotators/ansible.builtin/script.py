# -*- mode:python; coding:utf-8 -*-

# Copyright (c) 2023 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ansible_risk_insight.models import RiskAnnotation, TaskCall, DefaultRiskType, CommandExecDetail
from ansible_risk_insight.annotators.module_annotator_base import ModuleAnnotator, ModuleAnnotatorResult


class ScriptAnnotator(ModuleAnnotator):
    fqcn: str = "ansible.builtin.script"
    enabled: bool = True

    def run(self, task: TaskCall) -> ModuleAnnotatorResult:
        if task.args.get("type") == "simple":
            cmd = task.args.get("raw")
        else:
            cmd = None
            if cmd is None:
                cmd = task.args.get("cmd")
            if cmd is None:
                cmd = task.args.get("argv")

        annotation = RiskAnnotation.init(
            risk_type=DefaultRiskType.CMD_EXEC,
            detail=CommandExecDetail(command=cmd),
        )
        return ModuleAnnotatorResult(annotations=[annotation])
