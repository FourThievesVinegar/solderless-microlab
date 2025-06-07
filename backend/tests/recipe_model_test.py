from datetime import datetime
from typing import Any, Generator, Optional

import pytest

from recipes.model import (
    MicrolabRecipeOption,
    MicrolabRecipeStep,
    MicrolabRecipeMaterial,
    MicrolabRecipe,
    RecipeTaskRunnable,
)


def test_step_requires_either_next_or_options() -> None:
    """
    A non-final step must have either 'next' or 'options', but not both.
    """
    # Missing both next and options, MicrolabRecipeStep.done=False -> ValueError
    with pytest.raises(ValueError, match='must have a valid value for either "next" or "options"'):
        MicrolabRecipeStep(message='Test step', next=None, options=None, done=False)

    # Providing both next and options -> ValueError
    option = MicrolabRecipeOption(text='opt', next=0)
    with pytest.raises(ValueError, match='cannot have both "next" and "options" configured'):
        MicrolabRecipeStep(
            message='Test step',
            next=1,
            options=[option],
            done=False
        )


def test_step_allows_next_or_options_separately() -> None:
    """
    A non-final step is valid if exactly one of 'next' or 'options' is provided.
    """
    # Only next provided
    step_with_next = MicrolabRecipeStep(
        message='Go to next',
        next=1,
        options=None,
        done=False
    )
    assert step_with_next.next == 1
    assert step_with_next.options is None

    # Only options provided
    option = MicrolabRecipeOption(text='goto0', next=0)
    step_with_options = MicrolabRecipeStep(
        message='Choose option',
        next=None,
        options=[option],
        done=False
    )
    assert step_with_options.options == [option]
    assert step_with_options.next is None


def test_is_final_step_skips_next_options_validation() -> None:
    """
    A step marked MicrolabRecipeStep.done=True should not raise even if 'next' and 'options' are both None.
    """
    final_step = MicrolabRecipeStep(
        message='Done',
        next=None,
        options=None,
        done=True
    )
    assert final_step.done is True
    # Even if both next and options are missing, no exception is raised.


def test_recipe_step_index_out_of_range() -> None:
    """
    If a step.next index is outside [0, len(steps)-1], a ValueError is raised.
    """
    # Create one valid final step at index 1
    step1 = MicrolabRecipeStep(message='Step 1', next=None, options=None, done=True)

    # Create step0_bad so that next=2 (invalid, since we only have indices 0 and 1)
    step0_bad = MicrolabRecipeStep(
        message='Step 0',
        next=2,  # <-- out of range
        options=None,
        done=False  # still not final, which triggers the index‐check in MicrolabRecipe
    )

    # Building the recipe with step0_bad should raise the “out of range” error.
    with pytest.raises(ValueError, match=r'"2" after step 0 is outside the range of possible steps'):
        MicrolabRecipe(
            fileName='r.json',
            title='InvalidNextIndex',
            materials=[],
            steps=[step0_bad, step1]
        )


def test_recipe_option_index_out_of_range() -> None:
    """
    If an option.next index is outside [0, len(steps)-1], a ValueError is raised.
    """
    # Create a valid final step at index 1.
    step1 = MicrolabRecipeStep(message='Final', next=None, options=None, done=True)
    # Create a step0 with one option pointing to index=2 (invalid).
    bad_option = MicrolabRecipeOption(text='to2', next=2)
    step0_bad_opt = MicrolabRecipeStep(message='Step 0', next=None, options=[bad_option], done=False)

    with pytest.raises(ValueError,
                       match=r'The configured next step "2" for option "to2" in step 0 is outside the range of possible steps'):
        MicrolabRecipe(
            fileName='r2.json',
            title='InvalidOptionIndex',
            materials=[],
            steps=[step0_bad_opt, step1]
        )


def test_recipe_cant_reach_final_step() -> None:
    """
    A recipe where some step cannot reach a final step should raise ValueError.
    """
    # Step 0 points to step 1. Step 1 loops to itself and is not final -> unreachable final.
    step0 = MicrolabRecipeStep(message='Go to 1', next=1, options=None, done=False)
    step1 = MicrolabRecipeStep(message='Loop here', next=1, options=None, done=False)
    with pytest.raises(ValueError, match=r'The recipe is not valid as step 0 cannot reach a final step'):
        MicrolabRecipe(
            fileName='loop.json',
            title='LoopRecipe',
            materials=[],
            steps=[step0, step1]
        )


def test_valid_recipe_allows_convergence_to_final() -> None:
    """
    A recipe where every step has at least one path to a final step should construct successfully.
    """
    # Step 0 -> step 1. Step 1 is final.
    step0 = MicrolabRecipeStep(message='Go to 1', next=1, options=None, done=False)
    step1 = MicrolabRecipeStep(message='Done', next=None, options=None, done=True)
    recipe = MicrolabRecipe(
        fileName='good.json',
        title='GoodRecipe',
        materials=[MicrolabRecipeMaterial(description='Water')],
        steps=[step0, step1]
    )
    # Ensure get_step returns correct objects
    assert recipe.get_step(0) is step0
    assert recipe.get_step(1) is step1


def test_recipe_options_branching_reachability() -> None:
    """
    Options can also create valid paths to a final step.
    """
    # Step 0 has two options: to step1 (final) and to step2 which also leads to step1.
    opt_to1 = MicrolabRecipeOption(text='to1', next=1)
    opt_to2 = MicrolabRecipeOption(text='to2', next=2)
    step0 = MicrolabRecipeStep(message='Choose', next=None, options=[opt_to1, opt_to2], done=False)
    step1 = MicrolabRecipeStep(message='Final A', next=None, options=None, done=True)
    step2 = MicrolabRecipeStep(message='Go to 1', next=1, options=None, done=False)
    recipe = MicrolabRecipe(
        fileName='branch.json',
        title='BranchRecipe',
        materials=[],
        steps=[step0, step1, step2]
    )
    # All steps should be reachable to final
    assert recipe.get_step(0) is step0
    assert recipe.get_step(1).done
    assert not recipe.get_step(2).done


def dummy_gen() -> Generator[Optional[float], Any, Any]:
    """
    A no‐op generator whose annotated yield type is Optional[float].
    It never actually yields (so iterating over it produces an empty sequence).
    """
    if False:
        yield 1.0
    yield None


def test_task_runnable_model_assignment() -> None:
    """
    Ensure RecipeTaskRunnable accepts correct types and raises if mis‐typed.
    """
    now = datetime.utcnow()
    gen_instance = dummy_gen()  # type: Generator[Optional[float], Any, Any]

    runnable = RecipeTaskRunnable(
        fn=gen_instance,
        parameters={'param1': 42},
        is_done=False,
        next_time=now,
        exception=None
    )

    assert list(runnable.fn) == [None], 'The generator should yield no values for this dummy'
    assert runnable.parameters == {'param1': 42}
    assert runnable.is_done is False
    assert runnable.next_time == now

    # Passing wrong type for next_time -> should raise a ValidationError
    with pytest.raises(Exception):
        RecipeTaskRunnable(
            fn=dummy_gen(),
            parameters={},
            is_done=True,
            next_time='not a datetime',  # incorrect type
            exception=None
        )


# if __name__ == '__main__':
#     import sys
#     sys.exit(pytest.main([__file__]))
