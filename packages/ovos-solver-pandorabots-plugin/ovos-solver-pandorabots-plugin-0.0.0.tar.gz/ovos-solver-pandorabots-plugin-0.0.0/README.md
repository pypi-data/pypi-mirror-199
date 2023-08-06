# <img src='https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/robot.svg' card_color='#40DBB0' width='50' height='50' style='vertical-align:bottom'/> Pandorabots
 
Give Mycroft some sass with Pandorabots

Over 100 chatbots from https://github.com/OpenJarbas/all_the_chatbots

## Examples 
* "Do you like ice cream"
* "Do you like dogs"
* "I have a jump rope"


## Usage

Spoken answers api w

```python
from ovos_solver_pandorabots_plugin import PandoraBotsSolver

d = PandoraBotsSolver()
sentence = d.spoken_answer("hello")
print(sentence)
# Hi there!

sentence = d.spoken_answer("Do you like ice cream", {"lang": "pt-pt"})
print(sentence)
# O que queres mesmo saber?
```
