export enum MicrolabStatus {
  NO_BACKEND_RESPONSE = 'Waiting for control service',
  COMPLETE = 'complete',
  ERROR = 'error',
  USER_INPUT = 'user_input',
  IDLE = 'idle',
  RUNNING = 'running',
  RECIPE_UNSUPPORTED = 'recipe_unsupported',
}

export type MicrolabStatusResponse = {
  message?: string
  options?: string[]
  recipe?: string
  status: MicrolabStatus
  step: number
  stepCompletionTime?: string
  hardwareError?: string
  icon?: string
  temp?: number
}

export type RecipeDetailsType = {
  materials: RecipeMaterial[]
  steps: RecipeStep[]
}
export type RecipeMaterial = {
  description: string
}
export type RecipeStep = {
  parameters: any
  message: string
  tasks: any[]
}
