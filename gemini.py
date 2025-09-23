from google import genai
from google.genai import types

# Configure the client
client = genai.Client(api_key="")

# Define the grounding tool
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# Configure generation settings
config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

def add_citations(response):
    text = response.text
    supports = response.candidates[0].grounding_metadata.grounding_supports
    chunks = response.candidates[0].grounding_metadata.grounding_chunks

    # Store citation data to be formatted later
    citations = []
    citation_map = {} # To map chunk index to citation number

    # Sort supports by end_index in descending order to avoid shifting issues when inserting.
    sorted_supports = sorted(supports, key=lambda s: s.segment.end_index, reverse=True)

    citation_counter = 1
    for support in sorted_supports:
        end_index = support.segment.end_index
        if support.grounding_chunk_indices:
            citation_numbers = []
            for i in support.grounding_chunk_indices:
                if i not in citation_map:
                    if i < len(chunks):
                        uri = chunks[i].web.uri
                        citations.append({'number': citation_counter, 'uri': uri})
                        citation_map[i] = citation_counter
                        citation_counter += 1
                citation_numbers.append(f"[{citation_map[i]}]")
            
            citation_string = "".join(citation_numbers)
            text = text[:end_index] + citation_string + text[end_index:]

    return text, citations

def synthesize_and_verify(original_query, response, citations):
    system_prompt = f"""You are a research synthesis assistant. Your task is to verify, synthesize and augment information.
    
ORIGINAL QUERY: {original_query}
INITIAL FINDINGS: {response.text}
SOURCES CONSULTED: {citations}

YOUR TASK:
1. Cross-reference the information from the initial findings with the sources cited.
2. Identify consistent themes and any contradictions.
3. Synthesize key points to clearly define the RICE model and explain its core differences from the Kano model.
4. Augment the data with any additional relevant information from the sources.
5. Generate tables or any other visual aids if they help clarify differences or comparisons.
5. Provide the citations.

Structure the output such that it delivers the synthesized information and concisely and explains the differences clearly.

Be concise and factual."""

    system_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=system_prompt
    )
    text = system_response.text
    return text

def format_citations(citations):
    if not citations:
        return ""
    
    # Sort citations by number
    sorted_citations = sorted(citations, key=lambda c: c['number'])
    
    citation_list_str = "\n\nCitations:\n"
    for cit in sorted_citations:
        citation_list_str += f"{cit['number']}. {cit['uri']}\n"
        
    return citation_list_str

def main():
    original_query = "What is the RICE scoring model for prioritization, and how is it different from the Kano model"
    
    # Make the request
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=original_query,
        config=config,
    )

    text_with_placeholders, citation_data = add_citations(response)
    formatted_citations = format_citations(citation_data)
    
    synthesized_output = synthesize_and_verify(original_query, response, formatted_citations)
    
    # Write the output to a text file
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(synthesized_output)
        f.write("\n\n" + formatted_citations)

    print("Output successfully saved to output.txt")

if __name__ == "__main__":
    main()

