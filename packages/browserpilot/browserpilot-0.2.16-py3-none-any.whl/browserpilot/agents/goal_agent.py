"""GoalAgent class."""
import logging
from bs4 import BeautifulSoup
from .gpt_selenium_agent import GPTSeleniumAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""Set up all the prompt variables."""

DONE_TOKEN = "<DONE!>"

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

# If the beginning prompt does not route you to Google, then this prompt is used.
PROMPT_FOR_REST_OF_INSTRUCTIONS = """You are given a command to do a task using a web browser.

Your command is: "{command}".

You can ONLY do the following actions.
- Find an element on the page by referencing its text: 'Find the anchor element that contains the text "<text>".' This will store the element in memory.
- Click elements on an HTML page. Once you have found an element, you can click it by saying "Click" the element you found.
- Type things and press keys like enter or tab, e.g., "Type 'hello' and press enter."
- "Wait for `n` seconds." where `n` is a single digit int.
- Scroll the page by saying "Scroll down" or "Scroll up".
- Take a screenshot of the page, or an element on the page. 
- Save some text to a file `filename`.
- Declare that we are done by saying "<DONE!>"

Here is an example:
Find the input element with title "Search".
Type "hello world" and press enter.
Find the anchor element that contains the text "Wikipedia - Hello World".
Wait for 2 seconds.

Below is a stylized version of the webpage you are on, including only the buttons, links, and input/text areas.

{html}

Remember, your goal is: "{command}". You may ONLY take actions on the HTML above. In NO MORE THAN 3-5 new lines, what is the next step?

"""


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
        self, prompt, model=None, temperature=0, max_tokens=1024, use_cache=True
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

    def _feed_instruction_to_agent(self, instruction):
        """Feed the instruction to the Selenium agent. This is an important
        function because it will help us iteratively generate instructions
        based on the environment and then feed them to the agent."""
        self.browsing_agent.set_instructions(instruction)
        self.browsing_agent.run()

    def __preprocess_html_for_prompt(self) -> str:
        """Preprocess the HTML. Returns a string."""
        soup = self.browsing_agent._remove_blacklisted_elements_and_attributes()
        elements = soup.find_all()
        import pdb

        pdb.set_trace()
        for element in elements:
            # Remove every attribute except input placeholders,
            # textarea placeholders, textarea text, input text, and hrefs.
            # Make a copy of the element's attributes so we can delete
            # them without messing up the iteration.
            attributes = element.attrs.copy()
            for attribute in attributes:
                if attribute not in ["placeholder", "value"]:
                    del element[attribute]

        import pdb

        pdb.set_trace()
        # Join the elements into a string delimited by newlines.
        elements = "\n".join([str(element) for element in elements])
        return elements

    def _get_first_instruction(self) -> str:
        """Get the first instruction."""
        prompt = PROMPT_FOR_FIRST_INSTRUCTION.format(command=self.command)
        first_instruction = self._get_completion(prompt=prompt, model=self.model)
        return first_instruction

    def _get_next_instruction(self) -> str:
        """Get the next instruction."""
        elements = self.__preprocess_html_for_prompt()
        import pdb

        pdb.set_trace()
        prompt = PROMPT_FOR_REST_OF_INSTRUCTIONS.format(
            command=self.command, html=elements
        )
        next_instruction = self._get_completion(prompt=prompt, model=self.model)
        return next_instruction

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
            next_instruction = self._get_next_instruction()
            logger.info(next_instruction)
            if DONE_TOKEN in next_instruction:
                break

            # Perform the next instruction.
            self._feed_instruction_to_agent(next_instruction)

            step += 1
