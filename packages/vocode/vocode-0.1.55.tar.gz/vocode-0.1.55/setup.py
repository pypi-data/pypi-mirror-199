# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vocode',
 'vocode.streaming',
 'vocode.streaming.input_device',
 'vocode.streaming.input_device.streaming',
 'vocode.streaming.models',
 'vocode.streaming.output_device',
 'vocode.streaming.telephony',
 'vocode.streaming.user_implemented_agent',
 'vocode.turn_based',
 'vocode.turn_based.agent',
 'vocode.turn_based.input_device',
 'vocode.turn_based.output_device',
 'vocode.turn_based.synthesizer',
 'vocode.turn_based.transcriber']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp==3.8.4',
 'aiosignal==1.3.1',
 'anyio==3.6.2',
 'async-timeout==4.0.2',
 'attrs==22.2.0',
 'azure-cognitiveservices-speech==1.25.0',
 'certifi==2022.12.7',
 'cffi==1.15.1',
 'charset-normalizer==3.0.1',
 'click==8.1.3',
 'dataclasses-json==0.5.7',
 'decorator==5.1.1',
 'fastapi==0.92.0',
 'frozenlist==1.3.3',
 'h11==0.14.0',
 'idna==3.4',
 'langchain==0.0.117',
 'marshmallow-enum==1.5.1',
 'marshmallow==3.19.0',
 'mccabe==0.7.0',
 'multidict==6.0.4',
 'mypy-extensions==1.0.0',
 'numpy==1.24.2',
 'openai==0.27.2',
 'packaging==23.0',
 'pathspec==0.11.0',
 'platformdirs==3.1.0',
 'ply==3.11',
 'pycodestyle==2.10.0',
 'pycparser==2.21',
 'pydantic>=1.9.0',
 'pyflakes>=2.5.0',
 'pyjwt==2.6.0',
 'python-dotenv==0.21.1',
 'python-multipart==0.0.6',
 'pytz==2022.7.1',
 'pyyaml==6.0',
 'requests==2.28.2',
 'six==1.16.0',
 'sniffio==1.3.0',
 'sqlalchemy==1.4.47',
 'starlette==0.25.0',
 'tenacity==8.2.2',
 'tomli==2.0.1',
 'tqdm==4.65.0',
 'typing-extensions>=3.10.0.2',
 'typing-inspect==0.8.0',
 'urllib3==1.26.14',
 'uvicorn==0.20.0',
 'websockets==10.4',
 'yarl==1.8.2']

extras_require = \
{'io': ['sounddevice==0.4.6', 'pyaudio==0.2.13', 'pydub==0.25.1']}

setup_kwargs = {
    'name': 'vocode',
    'version': '0.1.55',
    'description': 'The all-in-one voice SDK',
    'long_description': '# vocode Python SDK\n\n```\npip install vocode\n```\n\n```python\nimport asyncio\nimport signal\nimport vocode\n\nvocode.api_key = "YOUR_API_KEY"\n\nfrom vocode.conversation import Conversation\nfrom vocode.helpers import create_microphone_input_and_speaker_output\nfrom vocode.models.transcriber import DeepgramTranscriberConfig\nfrom vocode.models.agent import ChatGPTAgentConfig\nfrom vocode.models.synthesizer import AzureSynthesizerConfig\n\nif __name__ == "__main__":\n    microphone_input, speaker_output = create_microphone_input_and_speaker_output(\n        use_default_devices=True\n    )\n\n    conversation = Conversation(\n        input_device=microphone_input,\n        output_device=speaker_output,\n        transcriber_config=DeepgramTranscriberConfig.from_input_device(microphone_input),\n        agent_config=ChatGPTAgentConfig(\n          initial_message=BaseMessage(text="Hello!"),\n          prompt_preamble="The AI is having a pleasant conversation about life."\n        ),\n        synthesizer_config=AzureSynthesizerConfig.from_output_device(speaker_output)\n    )\n    # This allows you to stop the conversation with a KeyboardInterrupt\n    signal.signal(signal.SIGINT, lambda _0, _1: conversation.deactivate())\n    asyncio.run(conversation.start())\n```\n',
    'author': 'Ajay Raj',
    'author_email': 'ajay@vocode.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
