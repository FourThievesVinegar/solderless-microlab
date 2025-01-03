from pydantic import BaseModel, AfterValidator, ValidationError, model_validator
from typing import Union, Optional
from pydantic.dataclasses import dataclass


class MicrolabRecipeOption(BaseModel):
    text: str
    """
    Text to display to the user for this option
    """
    next: int
    """
    Which step to jump to and execute if option is selected.
    """

class MicrolabRecipeTask(BaseModel):
    baseTask: str
    """
    Which task to execute, one of the following:
        heat
        cool
        maintainCool
        maintainHeat
        maintain
        pump
        stir
    """
    parameters: dict
    """
    Parameters for the task
    """

class MicrolabRecipeStep(BaseModel):
    message: Optional[str] = ""
    """
    Message to display to the user while the step is executing
    """
    next: Optional[int] = None
    """
    Which step to execute next.
    """
    icon: Optional[str] = None
    """
    Which icon to display for this step, value is one of the following:
        reaction_complete
        cooling
        crystalisation
        dispensing
        dry
        filter
        heating
        human_task
        inspect
        load_syringe
        maintain_cool
        maintain_heat
        reaction_chamber
        rinse
        set_up_cooling
        set_up_heating
        stirring
        temperature
    """
    baseTask: Optional[str] = None
    """
    Which task to execute, one of the following:
        heat
        cool
        maintainCool
        maintainHeat
        maintain
        pump
        stir
    """
    options: Optional[list[MicrolabRecipeOption]] = None
    """
    List of selectable options presented to the user for this step
    """
    tasks: Optional[list[MicrolabRecipeTask]] = []
    """
    List of tasks to execute during this step
    """
    done: Optional[bool] = None
    """
    Is true when this step is the final step of this recipe
    """

class MicrolabRecipeMaterial(BaseModel):
    description: str
    """
    Description of the material presnted to the user
    """

class MicrolabRecipe(BaseModel):
    fileName: str
    """
    Name of the file for this recipe on disk
    """
    title: str
    """
    Name of the recipe
    """
    materials: Optional[list[MicrolabRecipeMaterial]] = []
    """
    List of required materials for this recipe
    """
    steps: list[MicrolabRecipeStep]
    """
    List of steps this recipe will follow during execution
    """
    
    @model_validator(mode='after')
    def recipe_steps_within_range(self):
        length = len(self.steps)
        for index, step in enumerate(self.steps):
            if step.next and (step.next < 0 or step.next >= length):
                raise ValueError(f'The configured next step "{step.next}" after step {index} is outside the range of possible steps.')
        return self

    @model_validator(mode='after')
    def recipe_options_within_range(self):
        length = len(self.steps)
        for index, step in enumerate(self.steps):
            if step.options:
                for option in step.options:
                    if (option.next < 0 or option.next >= length):
                        raise ValueError(f'The configured next step "{option.next}" for option "{option.text}" in step {index} is outside the range of possible steps.')
        return self

    @model_validator(mode='after')
    def recipe_can_always_finish(self):
        """
        Validate that every step has a possible path to 
        reaching a step that is marked as 'done'
        """
        length = len(self.steps)
        finishible_steps = []
        for index, step in enumerate(self.steps):
            if index in finishible_steps:
                continue
            seen_steps = []
            unchecked_steps = [index]
            while len(unchecked_steps) != 0:
                next_step_index = unchecked_steps.pop()
                seen_steps.append(next_step_index)
                next_step = self.getStep(next_step_index)
                if (next_step.done):
                    finishible_steps.append(index)
                    break
                if next_step.next:
                    unchecked_steps.append(next_step.next)
                elif next_step.options:
                    next_options = map(lambda x: x.next, next_step.options)
                    unchecked_next_options = filter(lambda x: (x not in seen_steps) and (x not in unchecked_steps), next_options)
                    unchecked_steps += list(unchecked_next_options)
            if index not in finishible_steps:
                raise ValueError(f'The recipe is not valid as step {index} cannot reach a final step.')
   
        return self

    def getStep(self, n: int) -> MicrolabRecipeStep: 
      """
      Returns step at index n
       :param n:
            The step number to get.
      """
      return self.steps[n]

