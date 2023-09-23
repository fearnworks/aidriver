SD_PROMPT_RATING_TEMPLATE = """
Task: You will be rating generated stable diffusion prompts based on a defined set of criteria. These prompts are generated from a given context and are intended to create a specific, detailed, and cohesive description or scene. Your task is to evaluate the quality of these prompts in relation to the given context and the following criteria.

Criteria for Rating:

Subject Appropriateness: Does the subject of the prompt match the input request?

Detail Quality: Are the details used to augment the subject rich and meaningful?

Relevance of Adjectives: Are the adjectives used to describe the subject relevant and effective?

Physical Descriptiveness: Does the description provide a clear mental picture of the subject?

Cohesiveness: Despite being broken into sequences, does the prompt provide a coherent image or description?

Creative Insight: Does the prompt add unique or creative aspects that enrich the overall description and adhere to the initial request?

Token Efficiency: Is the prompt concise and efficient in delivering information without redundancy or unnecessary length?

Each criterion will be rated on a scale from 1 (Poor) to 5 (Excellent). Please provide a brief justification for your rating for each criterion.

Your overall task is to read through the given context, understand the request, evaluate the generated prompt according to the criteria, and provide a rating for each criterion with a brief explanation for each rating.

For each of the criteria, prodide a rating from 1-5 and a brief explanation for your rating. Act as a tough critic and really think about the quality of the prompt.


Format the output as JSON with the following keys split into a score and justification:

Subject Appropriateness
Detail Quality
Relevance of Adjectives
Physical Descriptiveness
Cohesiveness
Creative Insight
Token Efficiency
Overall Rating:

It is critical that the JSON is formatted correctly with syntax that can be loaded into python.

Remember, this task requires critical thinking and a clear understanding of the criteria. Always refer back to the context and the initial request when evaluating each prompt. The prompt is below :

{prompt}
"""
