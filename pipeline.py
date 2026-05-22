"""Small CLI entrypoint to run the research pipeline outside Streamlit.

This module exposes `run_research_pipeline(topic)` which executes the
same four-step pipeline used by the Streamlit app and prints progress
to stdout. It is useful for local testing or automation.
"""

from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str) -> dict:
    """Execute the research pipeline and return a dictionary of results.

    The return value contains keys: 'search_result', 'scraped_content',
    'report', and 'feedback'. Each value is the corresponding textual
    output produced by that pipeline stage.
    """

    state = {}
    
    # Step 1: Search Agent
    print("\n"+"="*50)
    print("step 1 : Search agent is working...")
    print("="*50)
    
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent,reliable and detailed information about: {topic}")],
    })
    state["search_result"] = search_result['messages'][-1].content
    
    print("\n search result: \n", state["search_result"])
    
    # Step 2: Reader Agent
    print("\n"+"="*50)
    print("step 2 : Reader agent is scraping information...")
    print("="*50)
    
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_result'][:800]}"
        )]
    })
    state["scraped_content"] = reader_result['messages'][-1].content
    
    print("\n scraped content: \n", state["scraped_content"])
    
    # Step 3: Writer Chain
    print("\n"+"="*50)
    print("step 3 : Writer is generating the report...")
    print("="*50)
    
    research_combined = (
        f"SEARCH RESULTS : \n {state['search_result']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n",state['report'])
    
    #critic report 
    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)