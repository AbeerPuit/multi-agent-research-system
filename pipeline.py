from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

def run_research_pipeline_stream(topic: str):
    state = {}

    # STEP 1: SEARCH
    yield {"step": "search", "status": "running", "message": "Searching web..."}

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent reliable and detailed information about: {topic}")]
    })

    state["search_results"] = search_result['messages'][-1].content

    yield {
        "step": "search",
        "status": "done",
        "data": state["search_results"]
    }

    #  STEP 2: READER
    yield {"step": "reader", "status": "running", "message": "Scraping best source..."}

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on search results about '{topic}', pick best URL and scrape it.\n\n"
            f"{state['search_results'][:800]}"
        )]
    })

    state["scraped_content"] = reader_result['messages'][-1].content

    yield {
        "step": "reader",
        "status": "done",
        "data": state["scraped_content"]
    }

    #  STEP 3: WRITER 
    yield {"step": "writer", "status": "running", "message": "Generating report..."}

    research_combined = f"SEARCH RESULTS:\n{state['search_results']}"

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    yield {
        "step": "writer",
        "status": "done",
        "data": state["report"]
    }

    # STEP 4: CRITIC 
    yield {"step": "critic", "status": "running", "message": "Reviewing report..."}

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    yield {
        "step": "critic",
        "status": "done",
        "data": state["feedback"]
    }

    # COMPLETE
    yield {
        "step": "complete",
        "status": "done",
        "data": state
    }