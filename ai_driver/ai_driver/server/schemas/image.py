from pydantic import BaseModel, Field


def to_snake_case(name: str) -> str:
    return name.replace(" ", "_").lower()


class SDEvaluation(BaseModel):
    score: float
    justification: str


class SDEvaluations(BaseModel):
    class Config:
        alias_generator = to_snake_case
        populate_by_name = True

    subject_appropriateness: SDEvaluation = Field(..., alias="Subject Appropriateness")
    detail_quality: SDEvaluation = Field(..., alias="Detail Quality")
    relevance_of_adjectives: SDEvaluation = Field(..., alias="Relevance of Adjectives")
    physical_descriptiveness: SDEvaluation = Field(
        ..., alias="Physical Descriptiveness"
    )
    creative_insight: SDEvaluation = Field(..., alias="Creative Insight")
    token_efficiency: SDEvaluation = Field(..., alias="Token Efficiency")
    overall_rating: SDEvaluation = Field(..., alias="Overall Rating")


class SDPromptGeneration(BaseModel):
    prompt: str
    evaluations: SDEvaluations
