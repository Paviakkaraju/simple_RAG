from pages.get_pages import get_internal_links
from pages.scrape_page import extract_text_from_url, parse_and_chunk, fetch_webpage
from pages.preprocess_text import preprocess_text
from embeddings.generate_embeddings import embed_chunks
from embeddings.store_embeddings import get_chroma_collection, store_embedded_chunks

base_url = "https://codework.ai"
all_links = get_internal_links(base_url)

# cleaned_dict = {}
result = {}

# for link in all_links:
#     raw_text = extract_text_from_url(link)
#     clean_text = preprocess_text(raw_text)
#     cleaned_dict[link] = clean_text
#     print(f"Text from {link}:")
#     print(len(clean_text))
#     print()


# for link in all_links:
#     print(f"Processing {link}")
#     html = fetch_webpage(link)
#     chunks = parse_and_chunk(html,link)
#     result[link] = chunks
#     print(chunks)
#     print()

# for link in all_links:
#     print(f"Processing {link}")
#     html = fetch_webpage(link)
#     chunks = parse_and_chunk(html,link)
#     embedded_chunks = embed_chunks(chunks)
    
#     for chunk in embedded_chunks[:3]:
#         print(chunk['metadata']['section'])
#         print(chunk['text'][:200], '...\n')
#         print()

base_url = "https://codework.ai"
all_links = get_internal_links(base_url)

collection, client = get_chroma_collection()

for link in all_links:
    print(f"Processing {link}")
    html = fetch_webpage(link)
    chunks = parse_and_chunk(html, link)
    embedded_chunks = embed_chunks(chunks)
    store_embedded_chunks(embedded_chunks, collection)

