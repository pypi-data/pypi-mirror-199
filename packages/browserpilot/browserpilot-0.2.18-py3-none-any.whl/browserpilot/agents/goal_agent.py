"""GoalAgent class."""
import logging
from typing import Dict
from bs4.element import Tag
from .gpt_selenium_agent import GPTSeleniumAgent, By

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""Set up all the prompt variables."""

# Beginning prompt.
PROMPT_FOR_FIRST_INSTRUCTION = """You are given a command to do a task using a web browser.

Let's reason step by step about what sequence of actions you have would to take in order to accomplish a task.

If no direction about which webpage to start on is given, you MUST (1) extract the relevant keywords from the command to search in Google and (2) begin with the lines

Go to google.com
Find the input element with title "Search".
Type <keywords> and press enter.

where <keywords> are the extracted keywords.

If direction about the webpage is given, simply return "Go to <url>."

Return your answers directly, succinctly, and without prefaces or suffixes. Let's start with the first step ONLY. What is the first step for the following command? Don't narrate what you are doing in your answer.
Command: "{command}"
Answer:"""

# Thank you to Nat Friedman for inspiration for this prompt.
# Source: https://github.com/nat/natbot/blob/main/natbot.py

DONE_TOKEN = "<DONE!>"
PROMPT_FOR_REST_OF_INSTRUCTIONS = """You are an agent controlling a browser. You are given:
1. an objective that you are trying to achieve
2. a simplified text description of what's visible in the browser window (more on that below)
You can issue these commands: 
- SCROLL UP|DOWN - Either  scroll up or scroll down one page.
- CLICK X - Click on the element with id X. You can only click on links, buttons, and inputs.
- TYPE X "TEXT" - Type the specified text into the input with id X.
- TYPESUBMIT X "TEXT" - Same as TYPE above, except it presses ENTER to submit the form.
- WAIT n - Wait for `n` seconds where `n` is an int.
- SCREENSHOT - Take a screenshot of the page.
- <DONE!> - Declare that we are done with the task!

The format of the browser content is highly simplified; all formatting elements are stripped.
Interactive elements such as links, inputs, buttons are represented like this:
		<link id=1>text</link>
		<button id=2>text</button>
		<input id=3>text</input>
Images are rendered as their alt text like this:
		<img id=4 alt=""/>

Based on your given objective, issue whatever command you believe will get you closest to achieving your goal.
==================================================
The current browser content and objective are below. Reply with your next command to the browser.
CURRENT BROWSER CONTENT:
--------------
{html}
------------------
OBJECTIVE: {command}
YOUR COMMAND:"""


class GoalAgent:
    def __init__(
        self,
        command=None,
        chromedriver_path=None,
        max_steps=100,
        enable_memory=False,
        model="gpt-3.5-turbo",
        debug=False,
    ):
        """Initialize the agent. It uses GPTSeleniumAgent to do the actual
        actions.

        Args:
            command (str): The instructions to compile.
            chromedriver_path (str): The path to the chromedriver.
            max_steps (int): The maximum number of times to ask for the next
                instruction. Used to prevent infinite loops.
            enable_memory (bool): Whether to enable memory.
            model (str): The model to use.
        """
        assert (
            chromedriver_path is not None
        ), "Please provide a path to the chromedriver."

        """Instance variables."""
        # Vars for the command.
        self.command = command
        self.model = model
        self.max_steps = max_steps
        self.enable_memory = enable_memory
        self.debug = debug

        # Accounting for the current state of the web browser.
        self.browser_element_mapping = {}

        # Vars for GPTSeleniumAgent.
        self.chromedriver_path = chromedriver_path
        _blank_instruction = ""
        self.browsing_agent = GPTSeleniumAgent(
            _blank_instruction,
            self.chromedriver_path,
            enable_memory=self.enable_memory,
            close_after_completion=False,
            debug=self.debug,
        )

    """Helper functions."""

    def _get_completion(
        self, prompt, model=None, temperature=0, max_tokens=1024, stop=["```"], use_cache=True
    ) -> str:
        """Get the completion from OpenAI."""
        # So this is kind of hacky, but just use the get_completion function
        # from the GPTSeleniumAgent's InstructionCompiler. I just want to
        # keep the number of times I rewrite the same code to a minimum.
        return self.browsing_agent.instruction_compiler.get_completion(
            prompt=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            use_cache=use_cache,
        )

    def _feed_instruction_to_agent(self, instruction, is_code=False):
        """Feed the instruction to the Selenium agent. This is an important
        function because it will help us iteratively generate instructions
        based on the environment and then feed them to the agent.
        
        If `is_code`, then the instruction is a Python code snippet. Otherwise,
        it is a natural language instruction."""
        if is_code:
            instruction = {
                "instructions": "",
                "compiled": instruction,
            }
        self.browsing_agent.set_instructions(instruction)
        self.browsing_agent.run()

    def __preprocess_html_for_prompt(self) -> Dict:
        """Preprocess the HTML. Returns a string."""
        # Get all of inputs, textareas, anchors, buttons, and imgs using
        # self.browsing_agent.driver, the Selenium driver.
        inputs = self.browsing_agent.driver.find_elements(by=By.TAG_NAME, value="input")
        textareas = self.browsing_agent.driver.find_elements(by=By.TAG_NAME, value="textarea")
        anchors = self.browsing_agent.driver.find_elements(by=By.TAG_NAME, value="a")
        buttons = self.browsing_agent.driver.find_elements(by=By.TAG_NAME, value="button")
        imgs = self.browsing_agent.driver.find_elements(by=By.TAG_NAME, value="img")
        # Also get the divs that have a role of button or textbox.
        divs = self.browsing_agent.driver.find_elements(by=By.TAG_NAME, value="div")
        divs = [div for div in divs if div.get_attribute("role") in ["button", "textbox"]]
        # Combine all of the elements.
        elements = inputs + textareas + anchors + buttons + imgs + divs
        
        mapping = {}
        curr_idx = 1
        for element in elements:
            # If the element is not visible, then don't include it.
            if not element.is_displayed():
                continue
            old_element = element.get_attribute("outerHTML")

            # Select the attributes to keep.
            attrs = {}
            attrs_to_keep = ["alt", "name", "title", "type"]
            for attr in attrs_to_keep:
                if element.get_attribute(attr):
                    attrs[attr] = str(element.get_attribute(attr))
            
            if element.tag_name == "input":
                # If the element is an input, then add the value.
                input_value = str(element.get_attribute("value"))
                if input_value:
                    attrs["value"] = input_value
            
            # Get the text from the element and strip whitespace.
            text = element.get_attribute("innerText").replace("\n", " ")

            # Create the new element.
            bs_tag = Tag(name=element.tag_name, attrs=attrs)
            bs_tag["id"] = str(curr_idx)
            bs_tag.string = text
            new_element = str(bs_tag)

            # If the img has no alt text, then don't include it.
            # In the future, we could try to use computer vision to caption.
            if element.tag_name == "img" and not element.get_attribute("alt"):
                continue

            # If div or anchor has no text, then don't include it.
            if element.tag_name in ["div", "a"] and not text:
                continue

            mapping[str(curr_idx)] = {"original": old_element, "transformed": new_element} 
            curr_idx += 1
            
        return mapping

    def _get_first_instruction(self) -> str:
        """Get the first instruction."""
        prompt = PROMPT_FOR_FIRST_INSTRUCTION.format(command=self.command)
        first_instruction = self._get_completion(prompt=prompt, model=self.model)
        return first_instruction

    def _get_domain_specific_response(self) -> str:
        """Get the next instruction for our current GoalAgent prompt."""
        mapping: Dict = self.__preprocess_html_for_prompt()
        self.browser_element_mapping = mapping

        elements = "\n".join([mapping[key]["transformed"] for key in mapping.keys()])
        prompt = PROMPT_FOR_REST_OF_INSTRUCTIONS.format(
            html=elements, command=self.command
        )
        next_instruction = self._get_completion(prompt=prompt, model=self.model)
        next_instruction = next_instruction.strip()
        return next_instruction

    def _get_compiled_instruction(self, natbot_instruction) -> str:
        """Given a response to the Natbot-inspired prompt, get the next
        instruction to feed to the GPTSeleniumAgent."""

        def get_code_for_selecting_element(element):
            prompt_select_ele = """Write a Selenium xpath selector to uniquely select the following element.
            Please default to using double quotes in your xpath selector. If you use single quotes, then
            you will need to escape them.

            {element}
            ```"""
            prompt = prompt_select_ele.format(element=element)
            xpath = self._get_completion(prompt, model="gpt-3.5-turbo", stop=["```"])
            return "element = env.find_element(by='xpath', value='{}')".format(xpath)

        curr_mapping = self.browser_element_mapping
        
        # Commands that return immediately.
        if natbot_instruction.startswith("SCROLL"):
            direction = natbot_instruction.split("SCROLL")[1].strip()
            return f"env.scroll('{direction}')"
        elif natbot_instruction.startswith(DONE_TOKEN):
            return natbot_instruction
        elif natbot_instruction.startswith("WAIT"):
            num_secs = int(natbot_instruction.split("WAIT")[1].strip())
            return f"env.wait({num_secs})"
        elif natbot_instruction.startswith("SCREENSHOT"):
            code_response = """element = env.find_element("xpath", "//html")
            env.screenshot(element, "screenshot.png")"""
        elif natbot_instruction.startswith("CLICK"):
            ele_id = natbot_instruction.split("CLICK")[1].strip()
            element = curr_mapping[ele_id]["original"]
            select_code = get_code_for_selecting_element(element)
            code_response = f"{select_code}\nenv.click(element)"
            return code_response
        elif natbot_instruction.startswith("TYPE"):
            args = natbot_instruction.split("CLICK")[1].strip()
            ele_id, text = args.split(" ")
            element = curr_mapping[ele_id]["original"]
            select_code = get_code_for_selecting_element(element)
            code_response = f"{select_code}\nenv.send_keys(element, '{text}')"
        elif natbot_instruction.startswith("TYPESUBMIT"):
            args = natbot_instruction.split("CLICK")[1].strip()
            ele_id, text = args.split(" ")
            element = curr_mapping[ele_id]["original"]
            select_code = get_code_for_selecting_element(element)
            code_response = f"{select_code}\nenv.send_keys(element, '{text}')"
            code_response += "\nenv.send_keys(element, Keys.ENTER)"
        else:
            raise ValueError(f"Invalid command: {natbot_instruction}")
        
        logger.info("Code response: {}".format(code_response))
        return code_response

    """Public functions."""

    def run(self):
        """Run the agent."""
        # Get the first instruction: either to go to a webpage or to search
        # Google. Then perform it.
        first_instruction = self._get_first_instruction()
        logger.info(first_instruction)
        self._feed_instruction_to_agent(first_instruction)

        # Iteratively get the next instruction and perform it.
        step = 0
        while step < self.max_steps:
            # Get the next instruction.
            natbot_instruction = self._get_domain_specific_response()
            next_instruction = self._get_compiled_instruction(natbot_instruction)
            logger.info(f"Next instruction: {next_instruction}")
            if DONE_TOKEN in next_instruction:
                logger.info("Done!")
                break

            # Perform the next instruction.
            self._feed_instruction_to_agent(next_instruction, is_code=True)

            step += 1
