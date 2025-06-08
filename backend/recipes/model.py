from datetime import datetime
from typing import Optional, Literal, Any, Generator

from pydantic import BaseModel, model_validator, Field

from localization import load_translation


class MicrolabRecipeOption(BaseModel):
    text: str = Field(
        description='Text to display to the user for this option',
    )
    next: int = Field(
        description='Which step to jump to and execute if option is selected',
    )


class MicrolabRecipeTask(BaseModel):
    baseTask: Literal[
        'heat',
        'cool',
        'maintainCool',
        'maintainHeat',
        'maintain',
        'pump',
        'stir'
    ] = Field(
        description='Which task to execute; one of: heat, cool, maintainCool, maintainHeat, maintain, pump, stir'
    )
    parameters: dict[str, Any] = Field(
        description='Parameters for the task'
    )


class MicrolabRecipeStep(BaseModel):
    message: str = Field(
        default='',
        description='Message to display to the user while the step is executing'
    )
    next: Optional[int] = Field(
        default=None,
        description='Which step to execute next'
    )
    icon: Optional[Literal[
        'reaction_complete',
        'cooling',
        'crystalisation',
        'dispensing',
        'dry',
        'filter',
        'heating',
        'human_task',
        'inspect',
        'load_syringe',
        'maintain_cool',
        'maintain_heat',
        'reaction_chamber',
        'rinse',
        'set_up_cooling',
        'set_up_heating',
        'stirring',
        'temperature'
    ]] = Field(
        default=None,
        description=(
            'Which icon to display for this step; one of: '
            'reaction_complete, cooling, crystalisation, dispensing, dry, filter, heating, '
            'human_task, inspect, load_syringe, maintain_cool, maintain_heat, reaction_chamber, '
            'rinse, set_up_cooling, set_up_heating, stirring, temperature'
        )
    )
    baseTask: Optional[Literal[
        'heat',
        'cool',
        'maintainCool',
        'maintainHeat',
        'maintain',
        'pump',
        'stir'
    ]] = Field(
        default=None,
        description='Which task to execute; one of: heat, cool, maintainCool, maintainHeat, maintain, pump, stir'
    )
    parameters: Optional[dict[str, Any]] = Field(
        default=None,
        description='Parameters for the baseTask defined in the step'
    )
    options: Optional[list[MicrolabRecipeOption]] = Field(
        default=None,
        description='List of selectable options presented to the user for this step'
    )
    tasks: list[MicrolabRecipeTask] = Field(
        default_factory=list,
        description='List of tasks to execute during this step'
    )
    done: Optional[bool] = Field(
        default=None,
        description='Is true when this step is the final step of this recipe'
    )

    @model_validator(mode='after')
    def step_has_one_of_next_or_options(self):
        t = load_translation()
        if self.done:
            return self

        has_next = bool(self.next)
        has_opts = bool(self.options)

        if not has_next and not has_opts:
            raise ValueError(t['need-value-next-options'])
        if has_next and has_opts:
            raise ValueError(t['error-next-options-configuration'])
        return self


class MicrolabRecipeMaterial(BaseModel):
    description: str = Field(
        description='Description of the material presented to the user'
    )


class MicrolabRecipe(BaseModel):
    fileName: str = Field(
        description='Name of the file for this recipe on disk'
    )
    title: str = Field(
        description='Name of the recipe'
    )
    materials: list[MicrolabRecipeMaterial] = Field(
        default_factory=list,
        description='List of required materials for this recipe'
    )
    steps: list[MicrolabRecipeStep] = Field(
        description='List of steps this recipe will follow during execution'
    )

    @model_validator(mode='after')
    def validate_step_and_option_indices(self):
        t = load_translation()
        length = len(self.steps)

        for index, step in enumerate(self.steps):
            # Check that step.next is within range
            if step.next is not None and (step.next < 0 or step.next >= length):
                raise ValueError(
                    t['error-step-outside-range'].format(step.next, index)
                )

            # Check that each option.next is within range
            if step.options:
                for option in step.options:
                    if option.next < 0 or option.next >= length:
                        raise ValueError(
                            t['error-step-option-outside-range'].format(option.next, option.text, index)
                        )

        return self

    @model_validator(mode='after')
    def recipe_can_always_finish(self):
        """
        Validate that every step has a possible path to 
        reaching a step that is marked as 'done'
        """
        t = load_translation()

        def can_reach_final_step(idx: int, visited: set[int]) -> bool:
            if idx in visited:
                return False
            visited.add(idx)

            step: MicrolabRecipeStep = self.steps[idx]
            if step.done:
                return True

            if step.next is not None and can_reach_final_step(step.next, visited):
                return True

            if step.options:
                for opt in step.options:
                    if opt.next is not None and can_reach_final_step(opt.next, visited):
                        return True

            return False

        for idx in range(len(self.steps)):
            if not can_reach_final_step(idx, set()):
                raise ValueError(t['error-cant-reach-final-step'].format(index=idx))

        return self

    def get_step(self, n: int) -> MicrolabRecipeStep:
        """
        Returns step at index n
         :param n:
              The step number to get.
        """
        return self.steps[n]


class RecipeTaskRunnable(BaseModel):
    fn: Generator[Optional[float], Any, Any] = Field(
        description='Generator returned by executing the command function. '
                    'Yields duration in seconds to wait before re‐invocation or None when done.'
    )
    parameters: dict[str, Any] = Field(
        description='Parameters that were passed into the command function.'
    )
    is_done: bool = Field(
        description='Flag indicating whether the recipe is complete.'
    )
    next_time: datetime = Field(
        description='Timestamp for when this command should run next.'
    )
    exception: Optional[str] = Field(
        default=None,
        description='Stringified exception message, if the command raised an error.'
    )