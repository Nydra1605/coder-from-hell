### Business Analyst Agent

## RICE vs. Kano: A Synthesized Analysis

This project is a Python script that uses Google's Gemini API to compare the RICE scoring model and the Kano model for product prioritization. It's designed to go beyond a simple search query by using a "Synthesizer" agent to verify, cross-reference, and augment information from multiple web sources, ensuring a high-quality, well-structured, and factual output.

### How It Works

The script operates in a multi-stage process:

1.  **Initial Search and Generation**: The script uses the `Google Search` tool to find relevant information about the RICE and Kano models. It then uses the `gemini-2.5-flash` model to generate an initial response grounded in the search results.
2.  **Citations**: The `add_citations` function processes the grounding metadata from the initial response to correctly place citations within the text and format a list of sources.
3.  **Synthesis and Verification**: A second, more detailed prompt is sent to the `gemini-2.5-flash` model. This "Synthesizer" agent is instructed to:
      * Cross-reference the initial findings with the provided sources.
      * Identify key themes and contradictions.
      * Synthesize the core differences between the RICE and Kano models.
      * Augment the information with additional relevant details.
      * Generate a clear, concise output, including tables if they help clarify the comparison.
4.  **Output**: The final, synthesized content and the formatted citations are saved to a file named `synthesized_output.txt`.

### Key Technical Choices

  * **LLM**: `gemini-2.5-flash` is used for its speed, efficiency, and robust tool-use capabilities, allowing for seamless integration with Google Search.
  * **Grounding**: The project heavily relies on the `Google Search` tool for grounding. This ensures that the generated content is based on up-to-date, verifiable information from external sources rather than the model's pre-trained data.

### Setup and Execution

To run this project, follow these steps:

1.  **Prerequisites**: Ensure you have Python installed on your system.
2.  **Install the SDK**: Install the necessary library by running the following command in your terminal:
    ```bash
    pip install google-generativeai
    ```

3.  **Run the Project**: Execute the script from your terminal:
    ```bash
    python gemini.py
    ```

The final output will be saved in a file named `output.txt`.