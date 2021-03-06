"""
MIT License

Sugaroid Artificial Intelligence
Chatbot Core
Copyright (c) 2020-2021 Srevin Saju
Copyright (c) 2021 The Sugaroid Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

from chatterbot.logic import LogicAdapter
from nltk import word_tokenize, pos_tag

from sugaroid.version import VERSION
from sugaroid.brain.constants import BYE, ONE_WORD, DISCLAIMER, HI_WORDS, HI_RESPONSES
from sugaroid.brain.myname import MyNameAdapter
from sugaroid.brain.ooo import Emotion
from sugaroid.brain.postprocessor import random_response
from sugaroid.brain.preprocessors import normalize
from sugaroid.sugaroid import SugaroidStatement


class OneWordAdapter(LogicAdapter):
    """
    Logical adapter for processing data with one words
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.normalized = None
        self.intersect = None
        self.tokenized = None

    def can_process(self, statement):
        self.normalized = normalize(str(statement).lower())

        if len(self.normalized) == 1:
            return True
        elif len(self.normalized) == 2:
            self.tokenized = pos_tag(self.normalized)
            if self.tokenized[1][1] == ".":
                return True
            else:
                return False
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        emotion = Emotion.seriously
        confidence = 0.60
        response = random_response(ONE_WORD)
        short = str(statement).lower()
        if "ver" in short:
            response = VERSION
            confidence = 0.99
        elif "name" in short:
            response = "What name? You should probably use better english"

        elif ("help404" in short) or ("help" in short and "404" in short):
            import sugaroid
            import chatterbot

            help_files = []
            for i in self.chatbot.globals["adapters"]:
                help_files.append(
                    "{}: {}".format(
                        i.split(".")[-1].strip(), eval(i).__doc__.strip()
                    ).strip()
                )
            response = "hmm. Sure. \n {}".format("\n ".join(help_files))
            confidence = 0.99

        elif "help" in short:
            response = (
                "The help is not very easily provided. "
                "If you are serious of what you are asking, "
                "type help404"
            )
            confidence = 0.99
        elif "disclaimer" in short:
            response = DISCLAIMER
            confidence = 0.99
        elif "license" in short:
            lic = """```
                                            MIT License

                                  Sugaroid Artificial Intelligence
                                            Chatbot Core
                                   Copyright (c) 2020-2021 Srevin Saju
Copyright (c) 2021 The Sugaroid Project

            Permission is hereby granted, free of charge, to any person obtaining a copy
            of this software and associated documentation files (the "Software"), to deal
            in the Software without restriction, including without limitation the rights
            to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
            copies of the Software, and to permit persons to whom the Software is
            furnished to do so, subject to the following conditions:

            The above copyright notice and this permission notice shall be included in all
            copies or substantial portions of the Software.

            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
            IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
            FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
            AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
            LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
            OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
            SOFTWARE.```
            """
            response = lic
            confidence = 0.99
        elif short in HI_WORDS:
            response = random_response(HI_RESPONSES)
            confidence = 0.99
        selected_statement = SugaroidStatement(response, chatbot=True)
        selected_statement.confidence = confidence
        selected_statement.emotion = emotion
        selected_statement.adapter = None
        return selected_statement
