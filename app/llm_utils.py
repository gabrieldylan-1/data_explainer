def create_prompt(query, schema, data):
    return f"""
        You are analyzing crime statistics data.
      
        Context:
        - The data comes from a law enforcement database
        - Focus on identifying significant patterns and trends
        - Provide clear, actionable insights

        Query:
        {query}

        Schema:
        {schema}

        Data:
        {data}
    """


def generate_response(client, prompt):
    response = client.chat.completions.create(
        model='grok-beta',
        messages=[
            {
                'role': 'system',
                'content': 'You are a crime statistics analyst providing clear, factual insights.'
            },
            {'role': 'user', 'content': prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )

    explanation = response.choices[0].message.content
    return explanation