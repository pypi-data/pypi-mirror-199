from typing import Dict, List, Optional, Any
from honeyhive.api.models.generations import GenerateQuery, GenerationResponse, ListGenerationResponse, GenerationLoggingQuery
from honeyhive.sdk.init import honeyhive_client
import pandas as pd

def generate(
    project: str,
    input: Dict[str, str],
    prompts: Optional[List[str]] = None,
    model_id: Optional[str] = None,
    best_of: Optional[int] = None,
    metric: Optional[str] = None,
    sampling: Optional[str] = None,
    user_properties: Optional[Dict[str, Any]] = None,
    source: Optional[str] = None,
) -> GenerationResponse:
    """Generate completions"""
    client = honeyhive_client()
    return client.generate(
        generation=GenerateQuery(
            task=project,
            input=input,
            prompts=prompts,
            model_id=model_id,
            best_of=best_of,
            metric=metric,
            sampling=sampling,
            user_properties=user_properties,
            source=source,
        )
    )

def get_generations(
    project: Optional[str] = None
) -> pd.DataFrame:
    """Get all generations"""
    client = honeyhive_client()
    generations_list = client.get_generations(task=project)
    import pandas as pd
    df = pd.DataFrame(generations_list)
    df.columns = df.iloc[0].apply(lambda x: x[0])
    df = df.applymap(lambda x: x[1] if isinstance(x, tuple) else x)

    return df

__all__ = [
    "generate",
    "get_generations"
]