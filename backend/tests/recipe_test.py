from recipes.model import MicrolabRecipe
import pytest
from pydantic import ValidationError

@pytest.fixture
def basic_recipe():
    return {
        "fileName": "aspirin.json",
        "title": "aspirin",
        "materials": [
            {"description": "2.0g salicylic acid"},
            {"description": "XX mL acetic anhydride"},
            {"description": "XX mL H2SO4"}
        ],
        "steps": [
            {
                "nr": 0,
                "message": "Place 2.0 g salicylic acid in chamber",
                "options": [{"text": "Done", "next": 1}],
                "icon": "reaction_chamber"
            },
            {
                "nr": 1,
                "message": "Place XX mL acetic anhydride into Pump X",
                "options": [{"text": "Done", "next": 2}],
                "icon": "load_syringe"
            },
            {
                "nr": 2,
                "message": "Place XX mL H2SO4 into Pump Y",
                "options": [{"text": "Done", "next": 3}],
                "icon": "load_syringe"
            },
            {
                "nr": 3,
                "message": "Dispensing acetic anhydride...",
                "next": 4,
                "tasks": [{
                    "baseTask": "pump",
                    "parameters": {"pump": "X", "volume": 5}
                }],
                "icon": "dispensing"
            },
            {
                "nr": 4,
                "message": "Dispensing H2SO4...",
                "next": 5,
                "tasks": [{
                    "baseTask": "pump",
                    "parameters": {"pump": "Y", "volume": 0.1}
                }],
                "icon": "dispensing"
            },
            {
                "nr": 5,
                "message": "Stirring...",
                "next": 6,
                "tasks": [{
                    "baseTask": "stir",
                    "parameters": {"time": 30}
                }]
            },
            {
                "nr": 6,
                "message": "Heating solution...",
                "next": 7,
                "tasks": [{
                    "baseTask": "heat",
                    "parameters": {"temp": 100}
                }],
                "icon": "temperature"
            },
            {
                "nr": 7,
                "message": "Waiting for 10 minutes.",
                "next": 8,
                "tasks": [{
                    "baseTask": "maintainHeat",
                    "parameters": {"time": 600, "temp": 100, "tolerance": 2}
                }],
                "icon": "temperature"
            },
            {
                "nr": 8,
                "message": "Cooling solution...",
                "next": 9,
                "tasks": [{
                    "baseTask": "cool",
                    "parameters": {"temp": 22}
                }],
                "icon": "temperature"
            },
            {
                "nr": 9,
                "message": "Crystallizing solution...",
                "next": 10,
                "tasks": [{
                    "baseTask": "cool",
                    "parameters": {"temp": 5}
                }],
                "icon": "temperature"
            },
            {
                "nr": 10,
                "message": "Waiting for 10 minutes.",
                "next": 11,
                "tasks": [{
                    "baseTask": "maintainCool",
                    "parameters": {"time": 600, "temp": 5, "tolerance": 2}
                }],
                "icon": "temperature"
            },
            {
                "nr": 11,
                "message": "Place 50 mL deionized water into Pump X",
                "options": [{"text": "Done", "next": 12}],
                "icon": "load_syringe"
            },
            {
                "nr": 12,
                "message": "Dispensing deionized water...",
                "next": 13,
                "tasks": [{
                    "baseTask": "pump",
                    "parameters": {"pump": "X", "volume": 50}
                }],
                "icon": "load_syringe"
            },
            {
                "nr": 13,
                "message": "Waiting for 20 minutes.",
                "next": 14,
                "tasks": [{
                    "baseTask": "maintainCool",
                    "parameters": {"time": 1200, "temp": 5, "tolerance": 2}
                }]
            },
            {
                "nr": 14,
                "message": "Reaction complete. Dry and rinse the product.",
                "is_final": True,
                "icon": "reaction_complete"
            }
        ]
    }

def test_works_with_valid_recipe_data(basic_recipe):
    MicrolabRecipe.model_validate(basic_recipe)

def test_raises_when_invalid_next_step_in_step(basic_recipe):
    basic_recipe["steps"][3]["next"] = -2
    with pytest.raises(ValidationError, match='is outside the range of possible steps'):
      MicrolabRecipe.model_validate(basic_recipe)

def test_raises_when_invalid_next_step_in_options(basic_recipe):
    basic_recipe["steps"][2]["options"] = [{"next": -2, "text": "test"}]
    with pytest.raises(ValidationError, match='is outside the range of possible steps'):
      MicrolabRecipe.model_validate(basic_recipe)

def test_raises_when_simple_infinite_loop(basic_recipe):
    basic_recipe["steps"][2]["next"] = 1
    basic_recipe["steps"][2]["options"] = None
    with pytest.raises(ValidationError, match='cannot reach a final step'):
      MicrolabRecipe.model_validate(basic_recipe)

def test_raises_when_last_step_is_unreachable(basic_recipe):
    basic_recipe["steps"][13]["next"] = 2
    with pytest.raises(ValidationError, match='cannot reach a final step'):
      MicrolabRecipe.model_validate(basic_recipe)

def test_raises_when_step_has_both_options_and_next(basic_recipe):
    basic_recipe["steps"][1]["next"] = 3
    with pytest.raises(ValidationError, match='Step cannot have both "next" and "options" configured'):
      MicrolabRecipe.model_validate(basic_recipe)

def test_raises_when_last_step_has_neither_options_or_next(basic_recipe):
    basic_recipe["steps"][1]["options"] = []
    with pytest.raises(ValidationError, match='Step must have a valid value for either "next" or "options"'):
      MicrolabRecipe.model_validate(basic_recipe)


# if __name__ == '__main__':
#     import sys
#     sys.exit(pytest.main([__file__]))
