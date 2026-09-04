# modules/dictionary.py
# Campus Buddy - Dictionary Module

import httpx

API_URL = "https://api.datamuse.com/words"


async def lookup_word(word):
    word = word.strip().lower()

    if not word:
        return "❌ Please enter a word."

    try:
        async with httpx.AsyncClient(timeout=15) as client:

            # Get definition
            response = await client.get(
                API_URL,
                params={
                    "sp": word,
                    "md": "d",
                    "max": 1
                }
            )

            if response.status_code != 200:
                return "❌ Dictionary service is unavailable."

            data = response.json()

            if not data:
                return f"❌ No definition found for: {word}"

            result = data[0]

            found_word = result.get("word", word)
            definitions = result.get("defs", [])

            message = (
                f"📖 <b>{found_word.upper()}</b>\n\n"
            )

            if definitions:
                message += "📚 <b>Definitions</b>\n\n"

                for i, definition in enumerate(
                    definitions[:5], 1
                ):
                    parts = definition.split("\t", 1)

                    if len(parts) == 2:
                        part_of_speech = parts[0]
                        meaning = parts[1].strip()
                    else:
                        part_of_speech = ""
                        meaning = definition.strip()

                    if part_of_speech == "n":
                        icon = "🔵"
                        pos = "Noun"

                    elif part_of_speech == "v":
                        icon = "🟢"
                        pos = "Verb"

                    elif part_of_speech == "adj":
                        icon = "🟡"
                        pos = "Adjective"

                    elif part_of_speech == "adv":
                        icon = "🟣"
                        pos = "Adverb"

                    else:
                        icon = "🔹"
                        pos = "Meaning"

                    message += (
                        f"{i}. {icon} <b>{pos}</b>\n"
                        f"   {meaning}\n\n"
                    )

            # Get synonyms while client is still open
            synonym_response = await client.get(
                API_URL,
                params={
                    "rel_syn": word,
                    "max": 8
                }
            )

            if synonym_response.status_code == 200:
                synonym_data = synonym_response.json()

                synonyms = [
                    item.get("word")
                    for item in synonym_data
                    if item.get("word")
                ]

                if synonyms:
                    message += (
                        "🔄 <b>Synonyms</b>\n"
                        + ", ".join(synonyms)
                        + "\n\n"
                    )

            message += "🤖 <i>Campus Buddy Dictionary</i>"

            return message

    except httpx.TimeoutException:
        return (
            "⏱️ <b>Dictionary request timed out.</b>\n\n"
            "Please try again."
        )

    except httpx.RequestError:
        return (
            "❌ <b>Could not connect to dictionary service.</b>\n\n"
            "Check your internet connection."
        )

    except Exception as e:
        print(f"Dictionary error: {e}")

        return (
            "❌ <b>Dictionary error.</b>\n\n"
            "Please try another word."
        )


def dictionary_help():
    return (
        "📖 <b>DICTIONARY</b>\n\n"
        "Enter an English word and Campus Buddy "
        "will show:\n\n"
        "🔹 Definition\n"
        "📚 Part of speech\n"
        "🔄 Synonyms\n\n"
        "Example:\n"
        "<code>programming</code>"
    )
