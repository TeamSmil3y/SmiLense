#from nlp.nlp import model
from more_itertools import sliced
from timeit import default_timer as timer
import nlp.google_gemini as google_gemini



prompt = (
    "Give me an analysis of the following license file matching exactly this format and the correct answer, do under no circumstances answer in a different format (the following list contains the keys and a selection of values of which you may pick any ONE that fits the license) and add nothing, seperate by comma:"
    "commercial_use: allowed or notallowed or notmentioned; "
    "open_source: yes or no or notmentioned; "
    "attribution: required or notrequired or notmentioned; "
    "redistribution: allowed or notallowed or notmentioned; "
    "profit: allowed or notallowed or notmentioned; "
)


def extract_key_points_2(raw: str):
    # list all the important key points from the LICENSE file

    additional = ""

    try:
        chat = google_gemini.model.start_chat()

        chat.send_message(
            prompt
        )


        r = chat.send_message(
            raw.strip()
        ).text

        print(r)

        additional = chat.send_message(
            "Is there any unexpected additions to the license? Answer shortly or with 'There are no additions.'"
        ).text ## Needs to be implemented for chunking as well


        res = {i.split(":")[0].strip():i.split(":")[1].strip() for i in r.replace(".", "").split("\n")[-1].split(", ") if i}
        res["additional"] = additional.strip()


        return res


    except Exception as e:
        print(f'EXCEPTION WHILE GENERATING KEY POINTS: {e}')
        return

