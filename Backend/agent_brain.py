import os
import re
import time
from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from sandbox_engine import UltraSandbox

# Load environment variables
load_dotenv()

# --- 1. Define the Agent State ---
class AgentState(TypedDict):
    task: str           # The user's request
    code: str           # The generated python code
    logs: List[str]     # Execution logs (Success/Error)
    attempts: int       # Iteration counter
    status: str         # 'start', 'success', 'error'

# --- 2. The Multi-Model Fallback System ---
# Prioritized based on your available models list
MODELS_TO_TRY = [
    "gemini-2.5-flash",        # Best balance of speed/intelligence
    #"gemini-flash-latest",     # Stable fallback
    "gemini-pro-latest",       # Legacy stable
    "gemini-2.0-flash-lite"  
      "gemma-3-1b-it"  # Ultra fast fallback
]

def get_ai_response(system_instruction: str, user_prompt: str):
    """Tries multiple AI models until one succeeds."""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    for model_name in MODELS_TO_TRY:
        print(f"🔄 Attempting to use model: {model_name}...")
        try:
            # Initialize Model (Transport argument removed to prevent warnings)
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=0,
                google_api_key=api_key,
                convert_system_message_to_human=True
            )
            
            # Invoke
            response = llm.invoke([
                SystemMessage(content=system_instruction), 
                HumanMessage(content=user_prompt)
            ])
            
            print(f"✅ Success with {model_name}")
            return response
            
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                print(f"⚠️ Quota exceeded for {model_name}. Switching...")
            elif "404" in error_str or "NOT_FOUND" in error_str:
                print(f"⚠️ Model {model_name} not found. Switching...")
            else:
                print(f"❌ Error with {model_name}: {error_str}")
            
            # Short pause before retry
            time.sleep(1)
            continue

    raise Exception("All AI Models failed. Please check your API Key or Quota.")

# --- 3. Node: The Architect (Writes Code) ---
def write_code(state: AgentState):
    attempt = state["attempts"] + 1
    print(f"\n🤖 [BRAIN] Generating Solution (Attempt {attempt})...")
    
    # Dynamic context based on previous failures
    error_context = ""
    if state["logs"] and "Error" in state["logs"][-1]:
        error_context = f"""
        ⚠️ PREVIOUS CODE FAILED.
        ERROR MESSAGE: {state['logs'][-1]}
        
        INSTRUCTION: Fix the error above. Do not repeat the same mistake.
        Ensure you ONLY use Standard Python Libraries (os, sys, math, random, json, re, time).
        """

    system_instruction = """
    You are CodeOps ULTRA, an elite Autonomous Engineering Agent.
    Your code runs inside a headless Docker Container (Linux/Debian).
    
    RULES:
    1. Write COMPLETE, RUNNABLE Python scripts.
    2. Do NOT use GUI libraries (tkinter, pygame) - the container has no screen.
    3. If asked for a web server, use standard libraries or ensure ports are printed.
    4. OUTPUT FORMAT: Return ONLY the raw code inside markdown code blocks.
    5. Do NOT write Dockerfiles or explanations outside the code block.
    """

    user_prompt = f"""
    TASK: {state['task']}
    
    {error_context}
    
    Generate the Python solution now.
    """
    
    try:
        # Call the Robust Multi-Model Function
        response = get_ai_response(system_instruction, user_prompt)
        
        # --- CRITICAL FIX: Handle Content Types (String vs List) ---
        content = response.content
        
        # If content is a list (common in Gemini), join it into a string
        if isinstance(content, list):
            # Join text parts, ignore non-text parts
            content = " ".join([str(item) for item in content])
        
        # Ensure it is a string for Regex
        content = str(content)

        # --- REGEX PARSING ---
        match = re.search(r"```python(.*?)```", content, re.DOTALL)
        if match:
            code = match.group(1).strip()
        else:
            match_generic = re.search(r"```(.*?)```", content, re.DOTALL)
            if match_generic:
                code = match_generic.group(1).strip()
            else:
                code = content.strip()

        return {"code": code, "attempts": attempt}

    except Exception as e:
        error_msg = f"CRITICAL BRAIN FAILURE: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            "code": "", 
            "logs": state["logs"] + [error_msg], 
            "status": "error", 
            "attempts": attempt
        }

# --- 4. Node: The Tester (Runs in Docker) ---
def test_code(state: AgentState):
    print("🧪 [SANDBOX] Spawning Secure Container...")
    
    if not state["code"]:
        return {"logs": state["logs"] + ["Error: AI returned empty code."], "status": "error"}

    sandbox = UltraSandbox()
    try:
        # 1. Start Container
        sandbox.start()
        
        # 2. Run Code
        result = sandbox.run_code(state["code"])
        
        # 3. Analyze Result
        output = result['output'].strip()
        exit_code = result['exit_code']

        if exit_code == 0:
            print(f"✅ [SUCCESS] Output:\n{output}")
            return {
                "logs": state["logs"] + [f"Execution Successful.\nOutput:\n{output}"], 
                "status": "success"
            }
        else:
            print(f"❌ [FAILED] Error:\n{output}")
            return {
                "logs": state["logs"] + [f"Runtime Error:\n{output}"], 
                "status": "error"
            }

    except Exception as e:
        print(f"💥 [CRITICAL] Sandbox Failure: {e}")
        return {"logs": state["logs"] + [f"System Error: {str(e)}"], "status": "error"}
        
    finally:
        # Always clean up the container
        sandbox.stop()

# --- 5. The Judge (Decides Next Step) ---
def router(state: AgentState):
    if state["status"] == "success":
        print("🎉 Task Completed Successfully.")
        return END
    
    if state["attempts"] >= 3:
        print("⚠️ Max Attempts Reached. Aborting.")
        return END
        
    print("🔄 Retrying with new strategy...")
    return "write_code"

# --- 6. Build the Graph ---
workflow = StateGraph(AgentState)

workflow.add_node("write_code", write_code)
workflow.add_node("test_code", test_code)

workflow.set_entry_point("write_code")
workflow.add_edge("write_code", "test_code")
workflow.add_conditional_edges(
    "test_code", 
    router, 
    {
        "write_code": "write_code", 
        END: END
    }
)

app = workflow.compile()

# --- Entry Point ---
def solve(task: str):
    print(f"\n🚀 STARTING MISSION: {task}")
    return app.invoke({
        "task": task, 
        "attempts": 0, 
        "logs": [], 
        "status": "start", 
        "code": ""
    })