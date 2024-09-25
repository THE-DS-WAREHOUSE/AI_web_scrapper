from langchain_ollama import OllamaLLM  # this time we worked with Ollama, however you can use
# ChatGPT (not free to use), Gemmini or Gemma if you want
# here is a link to all the LLM free models that you have access using langchain
# https://github.com/ollama/ollama
# make sure to properly install Ollama from here https://ollama.com/download with required OS
# and then for windows you can use commands
# ollama, "ollama pull (model version)" and "ollama run (model version)" on cmd to properly pull and verify installation
# make sure to verify every model requirements based on your PC components
from langchain_core.prompts import ChatPromptTemplate  # this let us create a Template

template = (  # template to use (you can change it but be careful with {parameters}
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {"
    "parse_description}."
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other "
    "text."
)

model = OllamaLLM(model="llama3.1")  # initialize the model (make sure to write the name properly)


def parse_with_AI(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)  # this is to create a prompt
    chain = prompt | model  # this creates the chain between prompt and model

    parsed_results = []  # we save the response from the model here

    for i, chunk in enumerate(dom_chunks, start=1):  # for every chunk
        response = chain.invoke(  # invoke the prompt and the model
            {"dom_content": chunk, "parse_description": parse_description}  # with this parameters
        )
        print(f"Parsed batch: {i} of {len(dom_chunks)}")  # this is to control model stages
        parsed_results.append(response)  # append results

    return "\n".join(parsed_results)  # join results
