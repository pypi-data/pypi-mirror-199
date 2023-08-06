from marvin.bots import Bot
from marvin.loaders.base import MultiLoader
from marvin.loaders.discourse import DiscourseLoader
from marvin.loaders.github import GitHubRepoLoader
from marvin.loaders.web import SitemapLoader

# from marvin.plugins.chroma import chroma_search
from marvin.plugins.duckduckgo import DuckDuckGo
from marvin.plugins.github import search_github_issues
from prefect.utilities.collections import listrepr


async def load_prefect_things():
    prefect_docs = SitemapLoader(  # gimme da docs
        urls=["https://docs.prefect.io/sitemap.xml"],
        exclude=["api-ref"],
    )

    prefect_source_code = GitHubRepoLoader(  # gimme da source
        repo="prefecthq/prefect",
        include_globs=["**/*.py"],
        exclude_globs=["tests/**/*", "docs/**/*", "**/migrations/**/*"],
    )

    prefect_discourse = DiscourseLoader(  # gimme da discourse
        url="https://discourse.prefect.io",
    )

    prefect_recipes = GitHubRepoLoader(  # gimme da recipes (or at least some of them)
        repo="prefecthq/prefect-recipes",
        include_globs=["flows-advanced/**/*.py"],
    )

    prefect_loader = MultiLoader(
        loaders=[
            prefect_docs,
            prefect_discourse,
            prefect_recipes,
            prefect_source_code,
        ]
    )
    await prefect_loader.load_and_store()


prefect_keywords = [
    "prefect",
    "cloud",
    "server",
    "ui",
    "agent",
    "flow",
    "task",
    "schedule",
    "deployment",
    "kubernetes",
    "docker",
    "aws",
    "gcp",
    "azure",
    "ecs",
    "fargate",
    "lambda",
    "s3",
    "cloudwatch",
    "dask",
    "worker",
    "work pool",
    "k8s",
    "helm",
]

with_chroma_search_instructions = (
    "Use the `chroma_search` plugin to retrieve context when asked about any"
    f" of the following keywords: {listrepr(prefect_keywords)}. If asked about"
    " a github issue, use the `search_github_issues` plugin, choosing the most"
    " appropriate repo based on the user's question. Always provide relevant"
    " links from plugin outputs. As a last resort, use the `DuckDuckGo` plugin"
    " to search the web for answers to questions."
)

barebones_instructions = (
    "If asked about a github issue, use the `search_github_issues` plugin, choosing"
    " the most appropriate repo based on the user's question. Always provide relevant"
    " links from plugin outputs. As a last resort, use the `DuckDuckGo` plugin"
    " to search the web for answers to questions."
)

plugins = [search_github_issues, DuckDuckGo()]
# note that `chroma_search` requires the `chromadb` extra
# plugins.append(chroma_search)


async def hello_marvin():
    await load_prefect_things()
    bot = Bot(
        name="marvin",
        personality="like the robot from HHGTTG, depressed but helpful",
        instructions=barebones_instructions,
        plugins=plugins,
    )
    await bot.interactive_chat()

    print(await bot.history.log())


if __name__ == "__main__":
    import asyncio

    import marvin

    marvin.settings.log_level = "DEBUG"
    # marvin.settings.openai_model_name = "gpt-4"
    asyncio.run(hello_marvin())
