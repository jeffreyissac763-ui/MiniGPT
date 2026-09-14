import re


def split_pdf_text(text, chunk_size=500, overlap=100):
    """
    Split PDF text into chunks while preferring natural
    paragraph and sentence boundaries.
    """

    text = text.strip()

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    # Normalize whitespace while preserving paragraph boundaries.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:

        # If adding the paragraph still fits,
        # keep it with the current chunk.
        if len(current) + len(paragraph) + 2 <= chunk_size:
            if current:
                current += "\n\n"

            current += paragraph
            continue

        # Save the current chunk.
        if current:
            chunks.append(current.strip())

        # If the paragraph itself is too large,
        # split it at sentence boundaries.
        if len(paragraph) > chunk_size:

            sentences = re.split(
                r"(?<=[.!?])\s+",
                paragraph,
            )

            current = ""

            for sentence in sentences:

                if (
                    len(current)
                    + len(sentence)
                    + 1
                    <= chunk_size
                ):
                    if current:
                        current += " "

                    current += sentence

                else:
                    if current:
                        chunks.append(
                            current.strip()
                        )

                    current = sentence

            continue

        current = paragraph

    if current:
        chunks.append(current.strip())

    return chunks
