# Education Purpose Only.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# coding=utf-8
# Copyright (c) 2019, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utilities for using and training tokenizers (char, wordpiece, sentencepiece)"""

from transformers import RobertaTokenizer
from ..tokenizer import Tokenizer, CommandToken, TypeToken
import os
"""define some default command tokens for the tokenizer to use"""


class ROBERTATokenizer(Tokenizer):

    def __init__(self, tokenizer_model_type="roberta-base", cache_dir=None):
        self.text_tokenizer = RobertaTokenizer.from_pretrained(
            tokenizer_model_type, cache_dir=cache_dir)
        self.text_tokenizer.max_len = int(1e12)
