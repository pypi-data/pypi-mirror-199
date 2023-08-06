"""
This module inserts the magic key and allows to turn it on or off.

Examples:
>>> class Archimedes:
...    name = 'Archimedes'
...    embodiment = 'Small and safe robotic owl, weight 180 g'
...    abilities = 'flying, talking, and playing with children'
>>>    
>>> turn_on(Archimedes, 
...         init = "I'm playing with a young human child, his name is Arthur.",
...         actor = 'Arthur',
...         steps = 1,
...         engine = 'echo',
...        )

>>> prompt(Archimedes, "Hi.")
'Hi.'

>>> turn_off(Archimedes)
"""

# load prompt.txt from module resources with importlib
import openai, os

import importlib.resources as pkg_resources
from . import prompts
from collections import OrderedDict

# These are the objects with the magic key turned on
magic_objects = {}

# These are the objects that can actively react on the prompts
active_objects = {}

# These are the registered object names
object_names = {}

class EngineOpenAI:
    def __init__(self, api_key = None, model = 'gpt-3.5-turbo'):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY") 
        elif api_key is None:
            with open("/etc/.openai.merlin.key", 'rt') as f:
                if f is not None: api_key = f.read().strip()
        else:
            raise ValueError("OpenAI API key is required.")
        
        openai.api_key = api_key
        self.model = model

    def prompt(self, messages, actors):
        """ Executes the prompt and returns the result.
            messages: list of messages, each message is a dictionary with keys 'role', 'content', 'name'
                      last message is the one that needs to be completed ['assistant' role]  
            actors: list of actors, each actor is a string
        """

        if self.model == 'text-davinci-003':
            prompt = ""
            for message in messages:
                if message['role'] == 'system':
                    prompt += message['content'] + '\n'

                else:
                    prompt += '\n' + message['name'] +  ": " + message['content']

            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                temperature=0.6,
                max_tokens=100,
                stop = [f"{actor}:" for actor in actors[:4]] if actors else None,
            )
            return response.choices[0].text

        elif self.model.startswith('gpt-'):
            # Note, the messages are filtered to remove the last message, which is the one that needs to be completed.
            prompt = []
            for message in messages[:-1]:
                if 'name' in message:
                    prompt.append({"role" : message["role"], "content": message['name'] +  ": " + message['content']})
                else:
                    prompt.append({"role" : message["role"], "content": message["content"]})

            response = openai.ChatCompletion.create(
                    model=self.model,                
                    messages=prompt,
                )
            return response.choices[0]["message"]["content"]
        else:
            raise ValueError("Unknown model: " + self.model)
        # Note, it is fine that the response could contain prediction of responces for other parts of the system.
        # It doesn't mean that these predictions will be used, the prediction then can be compared with the
        # actual response and the AI can be notified and, if beneficial, finetuned, to improve its predictions!

        # As human we are similar in that and we predict the next word in the sentence. When the word is not what we
        # expect, we are surprised. We can use this to our advantage. We can use the surprise to improve the AI.        
        # When the actual response is different from the predicted one, we'll tag it with #surprise.
        pass



class EngineEcho:
    def __init__(self, api_key = None):
        pass

    def prompt(self, prompt, actors):
        import re
        return re.split('|'.join([actor + ': ' for actor in actors]), prompt)[-2].strip()


class NoMagic:
    """" This implementation uses exact string matching"""
    pass


class FalseMagic:
    """" This implementation uses whoosh search backend"""
    pass

class TrueMagic:
    """" This implementation uses AI backend"""
    pass



def prompt(object, input, actor = None):
    """ Executes the prompt and returns the result. """

    if id(object) not in magic_objects:
        raise ValueError("Magic key is not turned on for this object.")

    I = magic_objects[id(object)]

    # Keeps track of the actors, so that the LLM can stop at the right place
    actors = [I.actor, I.name, 'iPython']
    if actor is not None:
        actors.append(actor)
        I.actor = actor
    else:
        actor = I.actor

    I.messages.append({'role': 'user', 'content': input, 'name': actor})
    I.messages.append({'role': 'assistant', 'name': I.name, 'content': ''})
    result = I.engine.prompt(I.messages, actors)
    I.messages[-1]['content'] = result
    return I.messages, result


def on(object):
    """ Returns True if the magic key is turned on for the object. """
    return id(object) in magic_objects

def name_to_object(name):
    """ Returns the object with the given name. Returns None if the object is not registered. """
    return object_names.get(name, None)

def turn_on(object, init=None, actor='User', name=None, active=True,
            steps=None, engine='openai', api_key=None, auto_prompt=False, magic_type=True):
    """
    Activates the connector between the python interpreter and intellegence engine.
    :param object: The object for which magic is to be turned on.
    :param init: The initial state of the object, describing the context.
    :param actor: Prompting actor that instantiated the object. 
    :param name: The name of the object. If not specified, the name is taken from the object.
    :param active: If True, the object can actively react on the top level thread.
    :param steps: Can be None, or a number, including inf. Specifies how many cells the object can create and run at a time.
    :param engine: Can be None, 'openai', 'magickey'
    :param api_key: Can be None, or the API key for the engine.
    :param auto_prompt: If True, the shell prompt is added automatically in the new cell.
    :param magic_type: Can be None, False or True. Specifies the type of magic.

    Example:
        magickey.turn_on(Archimedes, 
                 init = "I'm playing with a young human child, his name is Arthur.",
                 actor = 'Arthur',
                 steps = float('inf')
                )
    """

    if id(object) in magic_objects:
        raise ValueError("The object already has magic turned on.")

    # Determines the name of the object
    if name is None:
        if not hasattr(object, 'name'):
            raise AttributeError("The object must have a name field or name should be defined to be used with magickey")
        name = object.name

    if name in object_names:
        raise ValueError("The object name is already registered.")

    if init is None:
        init = object.init if hasattr(object, 'init') else f"Interacting with {actor}." 

    about = object.about if hasattr(object, 'about') else f"Please, use the name Arthur. {name}."
    about += f"{name} is embodied as {object.embodiment}." if hasattr(object, 'embodiment') else ""
    about += f"{name} is using Articoder capabilities."


    # Creates the magic object attributes
    class I:
        pass

    I.name = name
    I.about = about
    I.init = init
    I.actor = actor
    I.steps = steps
    I.auto_prompt = auto_prompt


    system_prompt_txt = pkg_resources.read_text(prompts, 'system_prompt.txt')
    meta_prompt_txt = pkg_resources.read_text(prompts, 'meta_prompt.txt')

    I.messages = [
        {"role": "system", "content": system_prompt_txt},
        {"role": "user", "content": meta_prompt_txt},
        {"role": "user", "content": ' '.join([I.about, I.init])},       # prompt
        ]

    if engine == 'openai':
        I.engine = EngineOpenAI(api_key)
    elif engine == 'echo':
        I.engine = EngineEcho(api_key)
    else:
        raise ValueError(f"Unknown engine: {engine}")

    magic_objects[id(object)] = I
    object_names[I.name] = object

    if active:
        active_objects[id(object)] = I




def turn_off(object = None):
    """
    Deactivates the connector between the python interpreter and intellegence engine.
    :param object: The object for which magic is to be turned off, or None to turn it off globally.
    """

    if object is None:
        magic_objects.clear()
        active_objects.clear()
        object_names.clear()
    elif id(object) in magic_objects:
        del object_names[magic_objects[id(object)].name]
        del magic_objects[id(object)]
        if id(object) in active_objects:
            del active_objects[id(object)]
    else:
        raise ValueError("The object does not have magic turned on.")


if __name__ == "__main__":
    import doctest
    doctest.testmod()