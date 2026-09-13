def split_text(text, chunk_size=500, overlap=100):
    sections = [
        section.strip()
        for section in text.split("\n\n")
        if section.strip()
    ]

    chunks = []

    i = 0

    while i < len(sections):
        current = sections[i]

        # If this looks like a heading, combine it
        # with all following text until the next heading.
        if (
            len(current) < 60
            and (
                current.endswith("(AI)")
                or current.endswith("(ML)")
                or current.endswith("(LLMs)")
                or current.endswith("(RAG)")
                or current in [
                    "Deep Learning",
                    "Embeddings",
                    "Vector Databases",
                ]
            )
        ):
            topic = current
            content = []

            i += 1

            while i < len(sections):
                next_section = sections[i]

                if (
                    len(next_section) < 60
                    and (
                        next_section.endswith("(AI)")
                        or next_section.endswith("(ML)")
                        or next_section.endswith("(LLMs)")
                        or next_section.endswith("(RAG)")
                        or next_section in [
                            "Deep Learning",
                            "Embeddings",
                            "Vector Databases",
                        ]
                    )
                ):
                    break

                content.append(next_section)
                i += 1

            combined = topic + "\n\n" + "\n\n".join(content)

            # Keep the complete topic together when possible.
            if len(combined) <= chunk_size:
                chunks.append(combined)
            else:
                chunks.append(combined)

            continue

        chunks.append(current)
        i += 1

    return chunks
