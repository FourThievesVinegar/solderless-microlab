# Split out to avoid circular requirements as both celery and __init__ depend on these values and base depends
# on both of these packages
import config

package = config.recipesPackage
currentRecipe = None
