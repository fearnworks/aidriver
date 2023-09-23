from loguru import logger

from langchain.output_parsers import ResponseSchema, StructuredOutputParser


class SDPromptRating:
    subject_appropriateness_schema = ResponseSchema(
        name="Subject Appropriateness",
        description="Rating and justification for Subject Appropriateness.",
    )
    detail_quality_schema = ResponseSchema(
        name="Detail Quality",
        description="Rating and justification for Detail Quality.",
    )
    relevance_of_adjectives_schema = ResponseSchema(
        name="Relevance of Adjectives",
        description="Rating and justification for Relevance of Adjectives.",
    )
    physical_descriptiveness_schema = ResponseSchema(
        name="Physical Descriptiveness",
        description="Rating and justification for Physical Descriptiveness.",
    )
    cohesiveness_schema = ResponseSchema(
        name="Cohesiveness", description="Rating and justification for Cohesiveness."
    )
    creative_insight_schema = ResponseSchema(
        name="Creative Insight",
        description="Rating and justification for Creative Insight.",
    )
    token_efficiency_schema = ResponseSchema(
        name="Token Efficiency",
        description="Rating and justification for Token Efficiency.",
    )
    overall_rating_schema = ResponseSchema(
        name="Overall Rating",
        description="Rating and justification for Overall Rating.",
    )

    response_schemas = [
        subject_appropriateness_schema,
        detail_quality_schema,
        relevance_of_adjectives_schema,
        physical_descriptiveness_schema,
        cohesiveness_schema,
        creative_insight_schema,
        token_efficiency_schema,
        overall_rating_schema,
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    @classmethod
    def parse(cls, response_content):
        try:
            return cls.output_parser.parse(response_content)
        except Exception as err:
            logger.error(f"Failed to parse JSON from response content: {err}")
            raise err
