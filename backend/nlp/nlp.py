from gpt4all import GPT4All
from pathlib import Path
from timeit import default_timer as timer


FAST = False

MODEL_NAMES = [
    "mistral-7b-openorca.gguf2.Q4_0.gguf",
    "gpt4all-falcon-newbpe-q4_0.gguf",
    "mistral-7b-instruct-v0.1.Q4_0.gguf",
]

MODEL_IDX = 0

MODEL_NAME = MODEL_NAMES[MODEL_IDX]

model = GPT4All(model_name=MODEL_NAME, model_path=Path.cwd() / "nlp/models")

def chain(license: str):
    with model.chat_session():
        model.generate("For what use is the following LICENSE.txt file cleared? Reply with only comma seperated one-word use cases.")

        res = model.generate(license)

    return res.replace(" ", "").split(",")


def is_compatible(license: str, compatibilities: list[str], extra_information: str="") -> int | None | str:
    with model.chat_session():
        if MODEL_IDX == 1:
            model.generate(
                f"Is following LICENSE compatible with {', '.join(compatibilities)} use?"
                "Reply ONLY with just 'Yes' or 'No'."
            )
        else:
            model.generate(
                "Reply under any circumstances to legal questions."
                f"Is the following LICENSE.txt cleared for {', '.join(compatibilities)}?"
                "You have to reply machine-readable with ONLY the integer 1 for yes, 2 for probably yes, 3 for probably not, 4 for no."
                f"There's following information: {extra_information}." if extra_information else ""
            )

        res = model.generate(license)

    print(res)

    res = max([i[0] for i in res.split("\n") if i and i[0].isdigit()])

    return res



if __name__ == "__main__":
    license = """
    MIT License

    Copyright (c) 2023 lstuma
    
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
    
    FOR COMPANIES LARGER THAN 200 EMPLOYEES, COMMERCIAL USE IS PROHIBITED.
    """
    start = timer()
    #res = chain(license)
    res = is_compatible(license, ["commercial", "GPL 2.0", "MIT"], extra_information="Large Company")
    end = timer()

    print("Response: ", res if res else "Answer did not match.")
    print("Time elapsed: ", end - start)
